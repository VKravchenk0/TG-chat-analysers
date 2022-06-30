import json
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import pandas as pd
from time import sleep

def get_lang_detector(nlp, name):
    return LanguageDetector()

nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)
# text = 'This is an english text.'
# text = "Er lebt mit seinen Eltern und seiner Schwester in Berlin."
text = "Привіт, світ"

doc = nlp(text)
print(doc._.language)


def is_message_relevant(message):
    if "type" not in message or message["type"] is None or message["type"] != "message":
        return False
    if "forwarded_from" in message:
        return False
    if "text" not in message or message["text"] is None or (isinstance(message["text"], str) and message["text"].strip() == ""):
        return False
    return True


def remove_formatting(original_text):
    result_text_list = []
    for text_element in original_text:
        if isinstance(text_element, str):
            result_text_list.append(text_element)
        else:
            if (text_element["type"] != "mention"):
                result_text_list.append(text_element["text"])

    return ''.join(result_text_list)


def transform_text(index_message_tuple):
    index = index_message_tuple[0]
    message = index_message_tuple[1]
    print(f"\rTransforming text: {index}", end='', flush=True)
    original_text = message["text"]
    if isinstance(original_text, str):
        message["text_normalized"] = message["text"]
        return message
    else:
        message_with_removed_formatting = remove_formatting(original_text)
        message["text_normalized"] = message_with_removed_formatting
        return message


def detect_lang(index_message_tuple):
    index = index_message_tuple[0]
    message = index_message_tuple[1]
    print(f"\rTransforming text: {index}", end='', flush=True)
    doc1 = nlp(message["text_normalized"])
    message["detected_lang"] = doc1._.language["language"]
    message["detected_lang_score"] = doc1._.language["score"]
    return message


with open('resources/result.json') as json_file:
    data = json.load(json_file)
    df = pd.DataFrame(data["messages"])
    print(f"original messages length: {len(data['messages'])}")
    messages = list(filter(is_message_relevant, data["messages"]))
    print(f"filtered messages length: {len(messages)}")
    mapped_messages = list(map(transform_text, enumerate(messages)))
    messages_with_detected_languages = list(map(detect_lang, enumerate(messages)))
    df1 = pd.DataFrame(messages_with_detected_languages, columns=["detected_lang", "detected_lang_score", "text_normalized"])
    print(df1['detected_lang'].unique())
    # df1.loc[df1['detected_lang'] == 'uk'].sort_values('detected_lang_score') || print(item, sep=' ', end='', flush=True)
    print("hello")
