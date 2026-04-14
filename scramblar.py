"""
    by Abdelrahman Hamada Hefny
"""

import random
import re
import unicodedata
from random import choice

"""
A list of basic Arabic script homoglyphs for every Arabic letter in unicode values of their isolated forms.
Only homoglyphs that satisfy Arabic typography/orthography rules and conventions are included here.
The use of these homoglyphs should be safe for text readability.
Sublists are in the order: isolated, initial, middle, final.
"""
homoglyphs_arabic_strict = {
    "ا": [[], ["\u0671"], [], []],
    "أ": [["\u0672", "\u0675"], ["\u0672", "\u0675"], ["\u0672", "\u0675"], ["\u0672", "\u0675"]],
    "إ": [["\u0673"], ["\u0673"], ["\u0673"], ["\u0673"]],
    "ت": [["\u067a"], ["\u067a"], ["\u067a"], ["\u067a"]],
    "ث": [["\u067d"], ["\u067d"], ["\u067d"], ["\u067d"]],
    "ف": [[], ['\u06A7'], ['\u06A7'], []],
    "ق": [["\u0608"], [], [], []],
    "ع": [["\u060f"], [], [], []],
    "ة": [["\u06c3"], ["\u06c3"], ["\u06c3"], ["\u06c3"]],
    "ك": [["\u06a9", "\u06aa"], ["\u06a9", "\u06aa"], ["\u06a9", "\u06aa"], ["\u06a9", "\u06aa"]],
    "ه": [["\u06be", "\u06c1", "\u06d5"], ["\u06be"], ["\u06be", "\u06c1"], ["\u06c1", "\u06d5"]],
    "ي": [["\u06d0", "\u06cd"], ["\u06d0", "\u067b", "\u06cc"], ["\u06d0", "\u067b", "\u06cc"], ["\u06d0", "\u06cd"]],
    "ى": [["\u06cc", "\u06d2"], ["\u066e"], ["\u066e"], ["\u06cc", "\u06d2"]],
    "ئ": [["\u06d3", "\u0678"], ["\u0678"], ["\u0678"], ["\u06d3", "\u0678"]],
    "ؤ": [["\u0676"], ["\u0676"], ["\u0676"], ["\u0676"]],
}

"""
A list of Arabic script homoglyphs for every Arabic letter in unicode values of their isolated forms.
These homoglyphs may have unusual shapes or extra dots, and may harm readability.
Sublists are in the order: isolated, initial, middle, final.
"""
homoglyphs_arabic_extended = {
    "ا": [[], [], [], []],
    "أ": [[], [], [], []],
    "إ": [[], [], [], []],
    "ب": [['\u067E', '\u0680', '\u08A0', '\u0755'], ['\u067E', '\u0680', '\u08A0', '\u0755'], ['\u067E', '\u0680', '\u08A0', '\u0755'], ['\u067E', '\u0680', '\u08A0', '\u0755']],
    "ت": [['\u067C'], ['\u067C'], ['\u067C'], ['\u067C']],
    "ث": [['\u067F'], ['\u067F'], ['\u067F'], ['\u067F']],
    "ج": [['\u0684', '\u0686', '\u0687'], ['\u0684', '\u0686', '\u0687'], ['\u0684', '\u0686', '\u0687'], ['\u0684', '\u0686', '\u0687']],
    "ح": [[], [], [], []],
    "خ": [['\u0681', '\u0682', '\u0685'], ['\u0681', '\u0682', '\u0685'], ['\u0681', '\u0682', '\u0685'], ['\u0681', '\u0682', '\u0685']],
    "د": [['\u0689', '\u068A', '\u068D'], ['\u0689', '\u068A', '\u068D'], ['\u0689', '\u068A', '\u068D'], ['\u0689', '\u068A', '\u068D']],
    "ذ": [['\u068C', '\u068E', '\u068F', '\u0690', "\u06EE"], ['\u068C', '\u068E', '\u068F', '\u0690', "\u06EE"], ['\u068C', '\u068E', '\u068F', '\u0690', "\u06EE"], ['\u068C', '\u068E', '\u068F', '\u0690', "\u06EE"]],
    "ر": [["\u0693", "\u0694", "\u0695"], ["\u0693", "\u0694", "\u0695"], ["\u0693", "\u0694", "\u0695"], ["\u0693", "\u0694", "\u0695"]],
    "ز": [["\u0692", "\u0696", "\u0697", "\u0698", "\u0699", "\u06EF"], ["\u0692", "\u0696", "\u0697", "\u0698", "\u0699", "\u06EF"], ["\u0692", "\u0696", "\u0697", "\u0698", "\u0699", "\u06EF"], ["\u0692", "\u0696", "\u0697", "\u0698", "\u0699", "\u06EF"]],
    "س": [['\u069B'], ['\u069B'], ['\u069B'], ['\u069B']],
    "ش": [['\u06FA', '\u069C', '\u077E'], ['\u06FA', '\u069C', '\u077E'], ['\u06FA', '\u069C', '\u077E'], ['\u06FA', '\u069C', '\u077E']],
    "ص": [['\u069D'], ['\u069D'], ['\u069D'], ['\u069D']],
    "ض": [['\u069E', '\u06FB'], ['\u069E', '\u06FB'], ['\u069E', '\u06FB'], ['\u069E', '\u06FB']],
    "ط": [['\u0679'], ['\u0679'], ['\u0679'], ['\u0679']],
    "ظ": [['\u069F', '\u08A3'], ['\u069F', '\u08A3'], ['\u069F', '\u08A3'], ['\u069F', '\u08A3']],
    "ف": [['\u06A3', '\u06A4', '\u08A4'], ['\u06A3', '\u06A4', '\u06A7', '\u08A4'], ['\u06A3', '\u06A4', '\u06A7', '\u08A4'], ['\u06A3', '\u06A4', '\u08A4']],
    "ق": [['\u06A8', '\u08A5'], ['\u08A5'], ['\u08A5'], ['\u06A8', '\u08A5']],
    "ع": [['\u08B3'], [], [], []],
    "غ": [['\u06A0', '\u06FC', '\u075D', '\u075E', '\u075F'], ['\u06A0', '\u06FC', '\u075D', '\u075E', '\u075F'], ['\u06A0', '\u06FC', '\u075D', '\u075E', '\u075F'], ['\u06A0', '\u06FC', '\u075D', '\u075E', '\u075F']],
    "ة": [[], [], [], []],
    "ك": [['\u063B', '\u063C', '\u06AB', '\u06AF', '\u06B0', '\u06AC', '\u06AE'], ['\u063B', '\u063C', '\u06AB', '\u06AF', '\u06B0', '\u06AC', '\u06AE'], ['\u063B', '\u063C', '\u06AB', '\u06AF', '\u06B0', '\u06AC', '\u06AE'], ['\u063B', '\u063C', '\u06AB', '\u06AF', '\u06B0', '\u06AC', '\u06AE']],
    "ل": [['\u076A', '\u08A6', '\u06B5', '\u06B8'], ['\u076A', '\u08A6', '\u06B5', '\u06B8'], ['\u076A', '\u08A6', '\u06B5', '\u06B8'], ['\u076A', '\u08A6', '\u06B5', '\u06B8']],
    "م": [['\u0765', '\u0766'], ['\u0765', '\u0766'], ['\u0765', '\u0766'], ['\u0765', '\u0766']],
    "ن": [['\u06B9', '\u06BC', '\u0767', '\u0769'], ['\u06B9', '\u06BC', '\u0769'], ['\u06B9', '\u06BC', '\u0769'], ['\u06B9', '\u06BC', '\u0767', '\u0769']],
    "ه": [['\u06FF'], ['\u06FF'], ['\u06FF'], []],
    "ى": [['\u063D', '\u063E', '\u063F', '\u06CE', '\u06D1'], [], [], ['\u063D', '\u063E', '\u063F', '\u06CE', '\u06D1']],
    "ئ": [[], [], [], []],
    "و": [[ '\u08AB'], ['\u08AB'], ['\u08AB'], ['\u08AB']],
    "ؤ": [[], [], [], []]
}

"""
A list of unicode homoglyphs for Arabic letters from outside the Arabic script.
The use of these homoglyphs is easier to detect and filter by automated filtering algorithms. # Is it less effective ??
Sublists are in the order: isolated, initial, middle, final.
"""
homoglyphs_universal = {
    "ا": [["l", "I", "|", '\u01C0', '\u0406'], [], [], ["\u0196", '\uA647', '\u053C', '\u14AA']],
    "إ": [['\u013C', '\u012E'], [], [], []],
    "آ": [['\u012A', '\u012B', '\u0128', '\u0129'], [], [], ['\u1FD1', '\u1FD6']],
    "ب": [[], [], ['\u071D\u0742'], []], # Syriac Yud with one dot below
    "ت": [[], [], ['\u071D\u0743'], []],
    "ث": [[], [], ['\u071D\u0745'], []],
    "ن": [[], [], ['\u071D\u0741'], []],
    "ي": [[], [], ['\u071D\u0744'], []],
    "ج": [[], ['\u0712\u0742'], ['\u0712\u0742'], []],
    "ح": [['\uA787', '\u0547'], ['\u05D1', '\u0712'], ['\u0712'], []],
    "خ": [[], ['\u0712\u0741'], ['\u0712\u0741'], []],
    "د": [['\u0716'], [], [], ['\u05D1', '\u0716']],
    "ذ": [['\u072A', '\u0716\u0741'], [], [], ['\u072A', '\u0716\u0741']],
    "س": [[], [], [], []],
    'ف': [[], ['\u14C5', '\u0726\u0741'], ['\u14C5', '\u0726\u0741'], []],
    "ق": [[], ['\u14C6', '\u0726\u0743'], ['\u14C6', '\u0726\u0743'], []],
    "ة": [['\u020D', '\u0151', '\u014D', '\u04E7', '\u0718\u0743'],[],[],['\u072C\u0743', '\u14CF']],
    "ل": [["J", '\u148D'], ['\u14A7'], [], []],
    "م": [[], ['\u0729'], ['\u0729'], []],
    "ك": [[], ['\u072D'], [], []],
    "ه": [['o', '0', '\u03BF', '\u043E', '\u0585', '\u0718'], ['\u0723'], [], ['\u072C', '\u14C7']],
    "و": [['9'], ['9'], ['9'], ['9']],
    "ﻻ": [['\u0264', '\u05E2', '\uFB20'], [], [], []]
}

"""
A list of Arabic script diacritics that resemble small-sized Arabic letters. 
Mostly used in Quranic writings and some Arabic script languages. 
"""
homoglyphs_diacritical = {
    "ز": [[], [], ['\u0617'], []],
    "س": [[], [], ['\u06DC'], []],
    "ط": [[], [], ['\u0615'], []],
    "م": [[], [], ['\u06E2', '\u06ED', '\u06D8'], []],
    "ن": [[], [], ['\u06E8'], []],
    "ج": [[], [], ['\u06DA'], []],
    "و": [[], [], ['\u08F3'], []],
    "ي": [[], [], ['\u06E7'], []],
}

homoglyphs_misspelled = [
    ['ا', 'أ', 'آ', 'إ'],
    ["ت", "ث", "ب"],
    ["ح", "ج", "خ"],
    ["د", "ذ"],
    ["ر", "ز"],
    ["س", "ش"],
    ["ص", "ض"],
    ["ط", "ظ"],
    ["ع", "غ"],
    ["و", "ؤ"],
    ['ئ', 'ى', 'ي']
]

"""
Arabic alphabet's commonly used equivalent sounds in the English alphabet. 
"""
phonetic_substitues = {
    "ب": "B",
    "ت": "T",
    "ج": "G",
    "د": "D",
    "ر": "R",
    "ز": "Z",
    "س": "S",
    "ف": "F",
    "ك": "K",
    "ل": "L",
    "م": "M",
    "ن": "N",
    "ه": "H",
}

# Unicode values for Arabic diacritics
diacritics = {
    # all diacritics are zero-width
    "tanween_fatha": "\u064B",
    "tanween_damma": "\u064C",
    "tanween_kasra": "\u064D",
    "fatha": "\u064E",
    "damma": "\u064F",
    "kasra": "\u0650",
    "shadda": "\u0651",
    "sukun": "\u0652",
    "madda": "\u0653",
    "hamza_above": "\u0654",
    "hamza_below": "\u0655",
    "high_tiple_dots": "\u06DB",  # Quranic sign
}

combining_diacritics = {
    'circumflex_accent': '\u0302',
    'tilde': '\u0303',
    'macron': '\u0304',
    'overline': '\u0305',
    'breve': '\u0306',
    'ring_above': '\u030A',
    'caron': '\u030C',
    'ring_below': '\u0325',
    'macron_below': '\u0331',
    'low_line': '\u0332',
    'double_tilde': '\u0360',
    'double_macron': '\u035E',
    'double_macron_below': '\u035F',
}

tone_dots = {
    # zero-width dots
    "one_above": "\u08EA",
    "two_above": "\u08EB",
    # "one_below": "\u08ED", # appears above letters
    "one_below": "\u065C", # Vowel sign
    "two_below": "\u08EE",
    "three_above": "\u06DB",  # Quranic sign
}

syriac_dots = {
    # supported in some fonts
    "one_above": "\u0741",
    "one_below": "\u0742",
    "two_above": "\u0743",
    "two_below": "\u0744",
    "three_above": "\u0745",
    "three_below": "\u0746",
}

symbol_dots = {
    # used by references in all dotted Arabic characters, but they are not zero-width in most fonts.
    "one_above": "\uFBB2",
    "one_below": "\uFBB3",
    "two_above": "\uFBB4",
    "two_below": "\uFBB5",
    "three_above": "\uFBB6",
    "three_below": "\uFBB7",
}

latin_dots = {
    "two_above": "\u0308", # COMBINING DIAERESIS
    "two_below": "\u0324", # COMBINING DIAERESIS BELOW
    "one_above": "\u0307", # COMBINING DOT ABOVE
    "one_below": "\u0323", # COMBINING DOT BELOWs
    "three_above": "\u1AB4", # COMBINING TRIPLE DOTS
}

dotless_letters = {
    "ب": "\u066E",
    "ت": "\u066E",
    "ث": "\u066E",
    "ج": "ح",
    "خ": "ح",
    "ذ": "د",
    "ز": "ر",
    "ش": "س",
    "ض": "ص",
    "ظ": "ط",
    "غ": "ع",
    "ق": "\u066F",
    "ف": "\u06A1",
    "ن": "\u06BA",
    "ي": "ى",
    "ة": "ه"
}

positional_variants = {
    # Unicode values for positional variants of Arabic characters in the order: isolated, initial, middle, final
    # Note: unicode order is: isolated, final, initial, middle, it suits letters with one/two forms but not the code.
    "ء": ['\uFE80', '\uFE80', '\uFE80', '\uFE80'],  # one form in all cases
    "آ": ['\uFE81', '\uFE81', '\uFE82', '\uFE82'],  # two forms
    "أ": ['\uFE83', '\uFE83', '\uFE84', '\uFE84'],
    "ؤ": ['\uFE85', '\uFE85', '\uFE86', '\uFE86'],
    "إ": ['\uFE87', '\uFE87', '\uFE88', '\uFE88'],
    "ئ": ['\uFE89', '\uFE8B', '\uFE8C', '\uFE8A'],
    "ا": ['\uFE8D', '\uFE8D', '\uFE8E', '\uFE8E'],
    "ب": ['\uFE8F', '\uFE91', '\uFE92', '\uFE90'],
    "ة": ['\uFE93', '\uFE93', '\uFE94', '\uFE94'],
    "ت": ['\uFE95', '\uFE97', '\uFE98', '\uFE96'],
    "ث": ['\uFE99', '\uFE9B', '\uFE9C', '\uFE9A'],
    "ج": ['\uFE9D', '\uFE9F', '\uFEA0', '\uFE9E'],
    "ح": ['\uFEA1', '\uFEA3', '\uFEA4', '\uFEA2'],
    "خ": ['\uFEA5', '\uFEA7', '\uFEA8', '\uFEA6'],
    "د": ['\uFEA9', '\uFEA9', '\uFEAA', '\uFEAA'],
    "ذ": ['\uFEAB', '\uFEAB', '\uFEAC', '\uFEAC'],
    "ر": ['\uFEAD', '\uFEAD', '\uFEAE', '\uFEAE'],
    "ز": ['\uFEAF', '\uFEAF', '\uFEB0', '\uFEB0'],
    "س": ['\uFEB1', '\uFEB3', '\uFEB4', '\uFEB2'],
    "ش": ['\uFEB5', '\uFEB7', '\uFEB8', '\uFEB6'],
    "ص": ['\uFEB9', '\uFEBB', '\uFEBC', '\uFEBA'],
    "ض": ['\uFEBD', '\uFEBF', '\uFEC0', '\uFEBE'],
    "ط": ['\uFEC1', '\uFEC3', '\uFEC4', '\uFEC2'],
    "ظ": ['\uFEC5', '\uFEC7', '\uFEC8', '\uFEC6'],
    "ع": ['\uFEC9', '\uFECB', '\uFECC', '\uFECA'],
    "غ": ['\uFECD', '\uFECF', '\uFED0', '\uFECE'],
    "ف": ['\uFED1', '\uFED3', '\uFED4', '\uFED2'],
    "ق": ['\uFED5', '\uFED7', '\uFED8', '\uFED6'],
    "ك": ['\uFED9', '\uFEDB', '\uFEDC', '\uFEDA'],
    "ل": ['\uFEDD', '\uFEDF', '\uFEE0', '\uFEDE'],
    "م": ['\uFEE1', '\uFEE3', '\uFEE4', '\uFEE2'],
    "ن": ['\uFEE5', '\uFEE7', '\uFEE8', '\uFEE6'],
    "ه": ['\uFEE9', '\uFEEB', '\uFEEC', '\uFEEA'],
    "و": ['\uFEED', '\uFEED', '\uFEEE', '\uFEEE'],
    "ى": ['\uFEEF', '\uFEEF', '\uFEF0', '\uFEF0'],
    "ي": ['\uFEF1', '\uFEF3', '\uFEF4', '\uFEF2'],
    "ﻵ": ['\uFEF5', '\uFEF5', '\uFEF6', '\uFEF6'],  # ligature
    "ﻷ": ['\uFEF7', '\uFEF7', '\uFEF8', '\uFEF8'],  # ligature
    "ﻹ": ['\uFEF9', '\uFEF9', '\uFEFA', '\uFEFA'],  # ligature
    "ﻻ": ['\uFEFB', '\uFEFB', '\uFEFC', '\uFEFC'],  # ligature
}

# sequences of letters that could be replaced with a single ligature character.
# Others can be added with varying font support.
ligatures = {
    "لآ": '\uFEF5',
    "لأ": '\uFEF7',
    "لإ": '\uFEF9',
    "لا": '\uFEFB',
    "الله": "\uFDF2",
}
ligature_values = {v: k for k, v in ligatures.items()}

terminals = ['ء', 'آ', 'إ', 'أ', 'ا', 'د', 'ذ', 'ر', 'ز', 'و', 'ﻵ', 'ﻷ', 'ﻹ', 'ﻻ']
isolated = ['ء']  # never connects to previous or next characters


def is_arabic_letter(ch):
    if 'ء' <= ch <= 'ي' or ch in ['\uFEF5', '\uFEF7', '\uFEF9', '\uFEFB']:
        return True

def find_diacritics(text: str, index: int):
    """find a diacritics substring at the specified index"""
    all_diacritic_values = diacritics.values()
    match = ""
    while index < len(text) and text[index] in all_diacritic_values:
        match += text[index]
        index += 1
    return match

def remove_diacritics(text: str):
    all_diacritic_values = diacritics.values()
    for diacritic in all_diacritic_values:
        text = text.replace(diacritic, '')
    return text

def separate_diacritics(text):
    out_text = ''
    all_diacritics = list(diacritics.values())
    text_diacritics = []
    for c in text:
        if c in all_diacritics and len(text_diacritics) > 0:
            text_diacritics[-1] += c
        else:
            out_text += c
            text_diacritics.append('')
    return out_text, text_diacritics


def encode_ligatures(text: str):
    """Insert ligatures (compound glyphs) to replace their components"""
    for lig in ligatures.keys():
        text = text.replace(lig, ligatures[lig])
    return text

def decode_ligatures(text: str):
    for lig in ligature_values:
        text = text.replace(lig, ligature_values[lig])
    return text

def make_typos(text, probability: float=0.5):
    similar_dict = {}
    for g in homoglyphs_misspelled:
        for letter in g:
            subs = g.copy()
            subs.remove(letter)
            similar_dict[letter] = subs
    out = ''
    for c in text:
        if c in similar_dict and random.random() < probability:
            out += random.choice(similar_dict[c], )
        else:
            out += c
    return out

def encode_positional_variants(text: str, reverse: bool=False, remove_spaces=False):
    """
    Replace each Arabic letter in the given text with a hard-coded positional variant based on its position in the word.
    :param text: input text
    :param reverse: reverse the order of characters and override text direction.
    :param remove_spaces: remove whitespaces from output. Prevents recovery with simple normalization.
    :return: text with hard-coded positional variants
    """
    out = ""
    joint = False  # start with initial form
    text = encode_ligatures(text)
    i = 0
    while i < len(text):
        c = text[i]
        if c in positional_variants.keys():
            # check if this letter has any diacritics
            next_diacritics = find_diacritics(text, i + 1)
            next_char_at = i + 1 + len(next_diacritics)
            if reverse:
                out += next_diacritics
            if joint:
                if (c in terminals) or (next_char_at == len(text)) \
                        or not is_arabic_letter(text[next_char_at]) or text[next_char_at] in isolated:
                    joint = False
                    out += positional_variants[c][3]  # final form
                else:
                    out += positional_variants[c][2]  # medial form
            else:
                if (c in terminals) or (next_char_at == len(text)) \
                        or not is_arabic_letter(text[next_char_at]) or text[next_char_at] in isolated:
                    out += positional_variants[c][0]  # isolated form
                else:
                    joint = True
                    out += positional_variants[c][1]  # initial form
            i += len(next_diacritics)
            if not reverse:
                out += next_diacritics
        else:
            # not a basic Arabic letter
            if not (remove_spaces and c in [' ', '\n', '\t']):
                out += c
        i += 1
    if reverse:
        out = "\u202D" + out[::-1] # Add LTR override and reverse the text
    return out

def get_dotless_form(c, final):
    # use dotless baa for non-final Noon or Yaa
    return "\u066E" if c in ['ن', 'ي'] and not final else dotless_letters[c]

def split_glyphs(text: str, dots: {} = None, dots_position: str = 'after', hamza: str = "keep", joiner: str = None, joiner_position: str = 'after'):
    """
    Split each Arabic letter that has a compound glyph into two or more characters.
    Can be used to split or remove dots and Hamza.
    :param text: input text
    :param dots: a dictionary specifying dot characters to use in each case of dots position and count.
    :param dots_position: a string specifying the position of dots 'before' or 'after' the base glyph.
    :param hamza: a string specifying how to treat characters with hamza above/below.
        Possible values are:
        "keep" to keep them unchanged (default),
        "split" to split each Hamza into a separate character,
        and "remove" to remove any Hamza.
    :param add_joiners: whether to insert elongation characters before and after dots to join dotless letters.
        Most fonts need this enabled for better readability. Has no effect when dots = None
    :return: returns the resulting text with split glyphs.
    """
    split_hamza = { # covert to Unicode Normalization Form NF??
        "أ": "\u0627\u0654",
        "إ": "\u0627\u0655",
        "آ": "\u0627\u0653",
        "ؤ": "\u0648\u0654",
        "ئ": "\u0649\u0654",
    }
    out = ""
    i = 0
    while i < len(text):
        c = text[i]
        if c in dotless_letters.keys():
            # check if this letter has any diacritics
            next_diacritics = find_diacritics(text, i + 1)
            next_char_at = i + 1 + len(next_diacritics)
            # check if it's joined to the next letter
            final = (c in terminals) \
                    or (next_char_at == len(text)) \
                    or not is_arabic_letter(text[next_char_at]) \
                    or text[next_char_at] in isolated
            # add the dotless letter
            if dots_position == 'after':
                # final Jeem dot cannot be simulated
                out += c if c == 'ج' and final else get_dotless_form(c, final)
            if dots is not None:
                if not final and joiner is not None and joiner_position in ['before', 'both']:
                    out += "\u200D" if joiner == 'ZWJ' else 'ـ'
                # add dots
                if c == 'ب' or c == 'ج' and not final:
                    out += dots.get("one_below", '')
                elif c in ["خ", "ذ", "ز", "ض", "ظ", "غ", "ف", "ن"]:
                    out += dots.get("one_above", '')
                elif c in ["ي"]:
                    out += dots.get("two_below", '')
                elif c in ["ت", "ة", "ق"]:
                    out += dots.get("two_above", '')
                elif c in ["ث", "ش"]:
                    out += dots.get("three_above", '')
                if not final and joiner is not None and joiner_position in ['after', 'both']:
                    out += "\u200D" if joiner == 'ZWJ' else 'ـ'
            if dots_position == 'before':
                out += c if c == 'ج' and final else get_dotless_form(c, final)
        # split Hamza above/below
        elif c in split_hamza.keys() and hamza != "keep":
            if hamza == "split":
                out += split_hamza[c]
            else:  # remove
                out += split_hamza[c][0]
        else:
            out += c
        i += 1
    return out

def replace_with_homoglyphs(text: str, homoglyphs: dict, include_original: bool = False, add_joiners: bool = False, enforce_rtl: bool = False, frequency:int = 1):
    """
    Substitute Arabic letters in the given text with their homoglyphs from the provided dictionary.
    Homoglyphs are chosen at random when more than one are available.
    :param text: input string
    :param homoglyphs: A dictionary mapping each letter to its possible homoglyphs in each form.
    :param include_original: include the original character as an option when randomly selecting homoglyphs.
    :return: returns the resulting text with homoglyphs
    """
    out = ""
    text = encode_ligatures(text)
    if enforce_rtl:
        out += "\u202E" # RTL override
    join_prev = False  # start with initial form
    last_replacement = -1
    i = 0
    while i < len(text):
        c = text[i]
        if is_arabic_letter(c):
            # check if this letter has any diacritics
            next_diacritics = find_diacritics(text, i + 1)
            next_char_at = i + 1 + len(next_diacritics)
            join_next = not (
                (c in terminals) or (next_char_at == len(text))
                or not is_arabic_letter(text[next_char_at]) or text[next_char_at] in isolated
            )
            if c in homoglyphs.keys() and (i - last_replacement >= frequency):
                if join_prev:
                    if join_next:
                        choices = homoglyphs[c][2]  # medial form
                    else:
                        choices = homoglyphs[c][3]  # final form
                else:
                    if join_next:
                        choices = homoglyphs[c][1] # initial form
                    else:
                        choices = homoglyphs[c][0] # isolated form
                joiner = ''
                last_replacement = i if len(choices) > 0 else last_replacement
                if include_original or len(choices) == 0:
                    choices = choices + [c]
                else:
                    joiner = 'ـ' if add_joiners else ''
                if join_prev:
                    out += joiner
                out += random.choice(choices)
                if join_next:
                    out += joiner
            else:
                out += c
            i += len(next_diacritics)
            out += next_diacritics
            join_prev = join_next
        else:
            out += c
        i += 1
    return decode_ligatures(out)

def replace_with_homophones(text, add_joiners=True, keep_distance=True, enforce_rtl: bool=False, middle_only: bool=True, frequency:int=2):
    sub_dict = {}
    for c in phonetic_substitues:
        if middle_only:
            sub_dict[c] = [[], [], [phonetic_substitues[c]], []]
        else:
            sub_dict[c] = [[], [], [phonetic_substitues[c]], [phonetic_substitues[c]]]
    return replace_with_homoglyphs(text, sub_dict, add_joiners=add_joiners, frequency=frequency, enforce_rtl=enforce_rtl)

def split_words(text: str, stem_words: bool=True, min_length: int = 3,
                word_probability: float = 0.5, letter_frequency: int=3, longest_split: int=3):
    """
    Split Arabic words in the given text randomly using spaces, dots, or hyphens.
    :param text: The text to split
    :param stem_words: ignore common prefixes and suffixes and split word stems only.
    :param min_length: The minimum length of words to split. Any shorter words will be skipped. Minimum value is 2.
    #:param max_segment_length: The maximum number of consecutive characters in a single word segment
    :param word_probability: Probability of splitting each word satisfying the min-length condition. Default is 0.5.
    :param letter_frequency: how many letters to cover by a single perturbation
    :return: returns the new text after splitting Arabic words.
    """
    text = encode_ligatures(text) # splitting ligatures will harm readability
    out = ""
    current_word = ""
    min_length = max(min_length, 2)
    letter_frequency = max(letter_frequency, 1)
    splitters = [
        s for s in ["ـ ـ", "ـ.ـ", "ـ..ـ", "ـ.", "ـ..", "ـ،", "ـ،ـ"] if len(s) <= longest_split
    ]
    i = 0
    while i < len(text):
        c = text[i]
        if is_arabic_letter(c):
            # build the Arabic word
            next_diacritics = find_diacritics(text, i + 1)
            # add this letter and its diacritics to the current word
            current_word += c + next_diacritics
            i += len(next_diacritics)
        if not is_arabic_letter(c) or i + 1 == len(text):  # reached the end of current word
            split_prob = random.random()
            base_word, word_diacritics = separate_diacritics(current_word)
            # decide whether to split this word
            if len(base_word) > min_length and split_prob <= word_probability:
                # define the range of word stem
                range_start = 0
                range_end = len(base_word) - 1
                if stem_words:
                    for prefix in ["ال", "وال", "لل", "كال", "بال", "فال", "و"]:
                        if base_word.startswith(prefix) and len(base_word) - len(prefix) > 1:
                            range_start = len(prefix)
                            break
                    for suffix in ["ة", "ات", "ين", "ون", "ان", "ه", "هم", "ها", "ك", "كم", "ني", "نا"]:
                        if base_word.endswith(suffix) and len(base_word) - range_start - len(suffix) > 1:
                            range_end = len(base_word) - len(suffix)
                letter_counter = 0
                char_counter = 0
                join_prev = False
                while char_counter < len(current_word) and letter_counter <= range_end:
                    if is_arabic_letter(current_word[char_counter]):
                        if letter_counter > range_start and (letter_counter - range_start) % letter_frequency == 0:
                            # select a separator
                            if not join_prev or base_word[letter_counter] in isolated:
                                sep = ' '  # no join
                            else:
                                sep = random.choice(splitters)
                            current_word = current_word[:char_counter] + sep + current_word[char_counter:]
                            char_counter += len(sep)
                        join_prev = not base_word[letter_counter] in terminals
                        letter_counter += 1
                    char_counter += 1
            out += current_word
            current_word = ""
        if not is_arabic_letter(c):
            out += c
        i += 1
    return decode_ligatures(out) # transform ligatures back to their canonical forms

def insert_random_diacritics(text, add_joiners=True):
    text=encode_ligatures(text)
    choices = list(combining_diacritics.values())
    out = ''
    for i, c in enumerate(text):
        join = (add_joiners and is_arabic_letter(c) and
                c not in terminals and i < len(text) - 2 and
                is_arabic_letter(text[i + 1]) and text[i + 1] not in isolated)
        out += c + 'ـ' + random.choice(choices) + 'ـ' if join else c + random.choice(choices)
    out = decode_ligatures(out)
    return out

"""
التشكيل بناء على تتابع الحروف.
مبنية على الخوارزمية المستخدمة في تطبيق منصور 2012 للكلمات الغير مفسرة
الحركات المضافة غير دقيقة ولكن كافية أحيانا لتشويش نماذج تعلم الآلة 
"""
def add_diacritics(text):
    text = remove_diacritics(text)
    text = unicodedata.normalize('NFC', text) # normalize decomposed characters
    long_vowels = ['ي', 'و', 'ا', 'ى']
    out = ''
    syl = 0
    for i, c in enumerate(text):
        if not is_arabic_letter(c):
            out += c
            syl = 0
            continue
        if c == 'إ':
            out += c + diacritics['kasra'] # only possible diacritic
            syl += 1
            continue
        if i < len(text) - 1:
            if text[i+1] == 'و':
                out += c + diacritics['damma']
                continue
            elif text[i+1] == 'ي':
                out += c + diacritics['kasra']
                continue
            elif text[i+1] in ['ا', 'ى']:
                out += c + diacritics['fatha']
                continue
        syl += 1
        if i < len(text) - 1 and text[i+1] == 'ة':
            out += c + diacritics['fatha'] # only possible diacritic
            continue
        if len(out) > 0 and out[-1] in [diacritics['fatha'], diacritics['damma'], diacritics['kasra']] and c in long_vowels:
            # long vowel
            out += c
            syl = 0
            continue
        if (syl % 2 == 0) or (0 < i < len(text) - 2 and is_arabic_letter(text[i+1]) and text[i + 2] in long_vowels and text[i - 1] in long_vowels):
            out += c + diacritics['sukun']
            continue
        out += c + diacritics['fatha'] # default fallback
    return out

