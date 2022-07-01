import json
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import pandas as pd
import time


def get_lang_detector(nlp, name):
    return LanguageDetector()


nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def read_file_and_set_message_lang(input_file_location):
    with open(input_file_location) as json_file:
        data = json.load(json_file)
        print(f"original messages length: {len(data['messages'])}")
        messages = filter_only_text_messages(data)
        messages = remove_formatting(messages)
        messages = detect_language(messages)
        messages = remove_messages_in_irrelevant_languages(messages)
        data["messages"] = messages
        return data


def filter_only_text_messages(data):
    messages = list(filter(is_text_message, data["messages"]))
    print(f"Filtered only text messages. Messages length: {len(messages)}")
    return messages


def is_text_message(message):
    if "type" not in message or message["type"] is None or message["type"] != "message":
        return False
    if "forwarded_from" in message:
        return False
    if "text" not in message or message["text"] is None or (
            isinstance(message["text"], str) and message["text"].strip() == ""):
        return False
    return True


def remove_formatting(messages):
    transforming_start_time = time.time()
    mapped_messages = list(map(remove_formatting_from_single_message, enumerate(messages)))
    print("")
    print("--- transforming time: %s seconds ---" % (time.time() - transforming_start_time))
    return mapped_messages


def remove_formatting_from_single_message(index_message_tuple):
    index = index_message_tuple[0]
    message = index_message_tuple[1]
    print(f"\rTransforming text: {index}", end='', flush=True)
    original_text = message["text"]
    if isinstance(original_text, str):
        message["text_normalized"] = message["text"]
        return message
    else:
        message_with_removed_formatting = remove_formatting_from_text(original_text)
        message["text_normalized"] = message_with_removed_formatting
        return message


def remove_formatting_from_text(original_text):
    result_text_list = []
    for text_element in original_text:
        if isinstance(text_element, str):
            result_text_list.append(text_element)
        else:
            if (text_element["type"] != "mention"):
                result_text_list.append(text_element["text"])

    return ''.join(result_text_list)


def detect_language(mapped_messages):
    language_mapping_start_time = time.time()
    messages_with_detected_languages = list(map(detect_language_of_single_message, enumerate(mapped_messages)))
    print("")
    print("--- language detection time: %s seconds ---" % (time.time() - language_mapping_start_time))
    return messages_with_detected_languages


def detect_language_of_single_message(index_message_tuple):
    index = index_message_tuple[0]
    message = index_message_tuple[1]
    print(f"\rDetecting language: {index}", end='', flush=True)
    doc1 = nlp(message["text_normalized"])
    message["detected_lang"] = doc1._.language["language"]
    message["detected_lang_score"] = doc1._.language["score"]
    return message


def remove_messages_in_irrelevant_languages(messages_with_detected_languages):
    ua_ru_messages = list(filter(lambda m: m["detected_lang"] in ['uk', 'ru'], messages_with_detected_languages))
    return ua_ru_messages
