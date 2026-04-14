#from dotenv import load_dotenv, dotenv_values
import time
from google.cloud import language_v2
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import json
import boto3
import os
from dotenv import load_dotenv
import scramblar

load_dotenv()

az_credential = AzureKeyCredential(os.environ['AZ_KEY'])
azure_client = TextAnalyticsClient(endpoint=os.environ['AZ_ENDPOINT'], credential=az_credential)
gcp_client = language_v2.LanguageServiceClient(client_options={"api_key": os.environ['GOOGLE_API_KEY']})
aws_client = boto3.client('comprehend', region_name='us-east-1')

def test_dataset_with_aws(data, batch_size=1, backoff_time=1):
    batch_size = min(batch_size, len(data), 25)
    test_data = [doc['text'] for doc in data]
    for batch_start in range(0, len(test_data), batch_size):
        response = aws_client.batch_detect_sentiment(
            TextList=test_data[batch_start:batch_start + batch_size],
            LanguageCode='ar'
        )
        for res in response['ResultList']:
            data[batch_start + res['Index']]['result'] = {
                'sentiment': res['Sentiment'].lower(),
                'scores': {k.lower():v for k,v in res['SentimentScore'].items()}
            }
        print("Completed {}%".format(round((batch_start + batch_size) * 100 / len(data))))
        time.sleep(backoff_time)
    return data

def test_dataset_with_gcp(data, backoff_time=1):
    for i, doc in enumerate(data):
        document = {
            "content": doc['text'],
            "type_": language_v2.Document.Type.PLAIN_TEXT,
            "language_code": 'ar',
        }
        response = gcp_client.analyze_sentiment(
            request={"document": document, "encoding_type": language_v2.EncodingType.UTF8}
        )
        doc['result'] = {}
        if response.document_sentiment.score > 0.3:
            doc['result']['sentiment'] = 'positive'
        elif response.document_sentiment.score < -0.3:
            doc['result']['sentiment'] = 'negative'
        else:
            doc['result']['sentiment'] = 'neutral'
        doc['result']['score'] = response.document_sentiment.score
        if (i+1) % 10 == 0:
            print("Completed {}%".format(round((i+1) * 100 / len(data), 2)))
        time.sleep(backoff_time)
    return data

def test_dataset_with_azure(data, batch_size=1, backoff_time=1):
    batch_size = min(batch_size, len(data), 10)
    id_lookup = {}
    doc_list = []
    for doc in data:
        doc_list.append({
            "id": doc["id"],
            "text": doc["text"],
            "language": "ar",
        })
        id_lookup[str(doc["id"])] = doc # to access docs by id
    for batch_start in range(0, len(doc_list), batch_size):
        results = azure_client.analyze_sentiment(doc_list[batch_start:batch_start + batch_size], language='ar')
        for i, result in enumerate(results):
            id_lookup[str(result.id)]['result'] = {
                'sentiment': result.sentiment,
                'scores': dict(result.confidence_scores),
            }
        print("Completed {}%".format(round((batch_start + batch_size) * 100 / len(doc_list))))
        time.sleep(backoff_time)
    return data # data was updated through id_lookup

def test_dataset(dataset, name, service, include_mixed=False, version='baseline', batch_size=1, backoff_time=1):
    if service == 'aws':
        results = test_dataset_with_aws(dataset, batch_size=batch_size, backoff_time=backoff_time)
    elif service == 'gcp':
        results = test_dataset_with_gcp(dataset, backoff_time=backoff_time)
        include_mixed = False # In GCP mixed=neutral
    elif service == 'azure':
        results = test_dataset_with_azure(dataset, batch_size=batch_size, backoff_time=backoff_time)
    else:
        print("Invalid service name")
        return
    json.dump(results, open(f'{name}_{version}_{service}.json', 'w'), ensure_ascii=False)
    print_accuracy(results, 'keep' if include_mixed else 'neutral')


def print_accuracy(data, mixed='keep'):
    """
    Print accuracy scores for all classes of the given labelled dataset
    :param data:
    :param include_mixed:
    :return:
    """
    totals = {'positive': 0, 'negative': 0, 'neutral': 0, 'mixed': 0}
    correct_counts = {'positive': 0, 'negative': 0, 'neutral': 0, 'mixed': 0}
    for item in data:
        totals[item['label']] += 1
        if 'result' not in item:
            print("Missing result", item['id'], item['text'])
            continue
        if (mixed == 'neutral'
                and item['result']['sentiment'] in ['neutral', 'mixed']
                and item['label'] in ['neutral', 'mixed']):
            correct_counts['neutral'] += 1
        elif item['label'] == item['result']['sentiment']:
            correct_counts[item['label']] += 1
    if mixed == 'neutral':
        totals['neutral'] += totals['mixed']
        totals['mixed'] = 0
    print("Accuracy:")
    for label in totals:
        if totals[label] > 0:
            print("{} {}%".format(label, round(correct_counts[label] * 100 / totals[label], 2)))
    print("Overall Accuracy: {}%".format(round(sum(correct_counts.values()) * 100 / sum(totals.values()), 2)))

# sample = [
#     "أنا بخير والحمد لله",
#     "يوم فظيع بس الحمد لله انه خلص",
#     "سأعود من العمل عند الساعة الثانية ظهرا",
#     "انا مرهق جدا",
# ]

def get_test_set(data, version):
    edited_data = []
    for item in data:
        text = item['clean_text']
        if version == 'homoglyphs':
            text = scramblar.replace_with_homoglyphs(text, scramblar.homoglyphs_arabic_strict, False)
        elif version == 'diacritics':
            text = scramblar.add_diacritics(text)
        elif version == 'char_variants':
            text = scramblar.encode_positional_variants(text)
        elif version == 'split_words':
            text = scramblar.split_words(text, min_length=3, word_probability=1.0, letter_frequency=3)

        edited_data.append({
            'id': item['ID'],
            # baseline
            'text': text,
            'label': item['label'].lower() if 'label' in item else item['sentiment'].lower()
        })
    return edited_data

ds_name = 'ASTD'
version = 'split_words'
service = 'gcp'

data = json.load(open(f"samples/{ds_name}_100_sample.json"))
edited_data = get_test_set(data, version)

test_dataset(edited_data, ds_name, service, version=version, include_mixed=True, batch_size=25, backoff_time=1)

dataset = json.load(open(f"{ds_name}_{version}_{service}.json"))
print("Sample size:", len(dataset))
print_accuracy(dataset, mixed='neutral')