import json
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import pandas as pd
import time
from datetime import datetime


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
        messages1 = filter_users_by_stop_list(messages)
        messages = remove_formatting(messages1)
        messages = squash_sequential_message_from_same_person(messages)
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


def filter_users_by_stop_list(messages):
    messages = list(filter(user_is_not_in_stop_list, messages))
    print(f"Removed users from stop list. Messages left: {len(messages)}")
    return messages


def user_is_not_in_stop_list(message):
    # user_is_in_stop_list = message['from_id'] in ['user168370994', 'user309233391', 'user56326953', 'user397363139'] # bro
    user_is_in_stop_list = message['from_id'] in ['user399811652', 'user437195022', 'user409446481', 'user336123529', 'user258526776', 'user1841958063'] # bike
    return not user_is_in_stop_list


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
        return message
    else:
        message_with_removed_formatting = remove_formatting_from_text(original_text)
        message["text"] = message_with_removed_formatting
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


def squash_sequential_message_from_same_person(messages):
    print(f"Number of messages before squashing: {len(messages)}")
    result = []
    for m in messages:
        message_date = datetime.fromisoformat(m["date"])
        if result and messages_from_the_same_sender(result[-1], m):
            last_message_in_result_list = result[-1]
            time_diff = (message_date - last_message_in_result_list["thread_start_date"]).total_seconds()
            # print(f"Messages with ids {m['id']} and {last_message_in_result_list['id']} have time difference of {time_diff} seconds")
            if time_diff < 120:
                # print("Squashing messages")
                last_message_in_result_list["thread_start_date"] = message_date
                last_message_in_result_list["text"] = result[-1]["text"] + '\n' + m["text"]
                continue

        append_message_to_result_list(m, message_date, result)
    print(f"Number of messages after squashing: {len(result)}")
    return result


def messages_from_the_same_sender(m1, m2):
    return m1['from_id'] == m2['from_id']


def append_message_to_result_list(m, message_date, result):
    m["thread_start_date"] = message_date
    result.append(m)


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
    doc1 = nlp(message["text"])
    message["detected_lang"] = doc1._.language["language"]
    message["detected_lang_score"] = doc1._.language["score"]
    return message


def remove_messages_in_irrelevant_languages(messages_with_detected_languages):
    ua_ru_messages = list(filter(lambda m: m["detected_lang"] in ['uk', 'ru'], messages_with_detected_languages))
    return ua_ru_messages
