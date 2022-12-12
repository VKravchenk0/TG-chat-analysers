import pickle
import time

import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

from src.data_processors.counters import SimpleLanguagePercentageCounter, WeightedLanguagePercentageCounter, LanguagePercentageCounterType
from src.utils.file_name_utils import get_language_percentage_result_abs_file_name
from src.utils.text_utils import remove_formatting


def get_lang_detector(nlp, name):
    return LanguageDetector()


nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def count_lang_percentage_and_save_to_file(data, chat_info, file_name, user_stop_list, counter_type):
    result = count_lang_percentage(data, chat_info, counter_type, user_stop_list)
    pickle.dump(result, open(get_language_percentage_result_abs_file_name(file_name), "wb"))
    print("count_lang_percentage_and_save_to_file -> end")


def count_lang_percentage(data, chat_info, counter_type, user_stop_list=[]):
    print("count_lang_percentage_and_save_to_file -> start")
    print(f"original messages length: {len(data['messages'])}")
    messages = clean_data(data, user_stop_list)
    messages = detect_language(messages)
    messages = remove_messages_in_irrelevant_languages(messages)
    result = count_language_percentages(messages, counter_type)
    chat_info["name"] = data["name"]
    result["chat_info"] = chat_info
    return result


def count_language_percentages(messages, counter_type: LanguagePercentageCounterType):
    if counter_type == LanguagePercentageCounterType.WEIGHTED:
        return WeightedLanguagePercentageCounter().count_language_percentages(messages)
    elif counter_type == LanguagePercentageCounterType.SIMPLE:
        return SimpleLanguagePercentageCounter().count_language_percentages(messages)
    else:
        raise NotImplementedError(f"Processing not implemented for counter type: {counter_type}")


def clean_data(data, user_stop_list):
    messages = filter_only_text_messages(data)
    messages = filter_users_by_stop_list(messages, user_stop_list)
    messages = remove_formatting(messages)
    return messages


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


def filter_users_by_stop_list(messages, user_stop_list):
    messages = list(filter(lambda m: user_is_not_in_stop_list(m, user_stop_list), messages))
    print(f"Removed users from stop list. Messages left: {len(messages)}")
    return messages


def user_is_not_in_stop_list(message, user_stop_list):
    user_is_in_stop_list = message['from_id'] in user_stop_list
    return not user_is_in_stop_list


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
