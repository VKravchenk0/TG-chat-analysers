import pickle
import time
from datetime import timedelta

import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

from src.utils.file_name_utils import get_language_percentage_result_abs_file_name
from src.utils.text_utils import remove_formatting, squash_sequential_message_from_same_person


def get_lang_detector(nlp, name):
    return LanguageDetector()


nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def percentage(part, whole):
    return 100 * float(part)/float(whole)


def extract_lang_and_date(index_message_tuple):
    index = index_message_tuple[0]
    message = index_message_tuple[1]
    dt = message["thread_start_date"] # to understand thread_start_date - see squash_sequential_message_from_same_person function
    week_start = dt - timedelta(days=dt.weekday())
    result = {
        'lang': message["detected_lang"],
        'date': dt,
        'beginning_of_week': week_start,
        'beginning_of_week_str': week_start.strftime("%d/%m/%Y"),
    }
    return result


def count_lang_percentage_and_save_to_file(data, file_name, user_stop_list):
    print("count_lang_percentage_and_save_to_file -> start")
    print(f"original messages length: {len(data['messages'])}")
    messages = filter_only_text_messages(data)
    messages1 = filter_users_by_stop_list(messages, user_stop_list)
    messages = remove_formatting(messages1)
    messages = squash_sequential_message_from_same_person(messages)
    messages = detect_language(messages)
    messages = remove_messages_in_irrelevant_languages(messages)
    data["messages"] = messages
    number_of_messages_by_weeks = count_number_of_messages_by_time_period(data)
    lang_percentage_by_weeks = count_percentages(number_of_messages_by_weeks)
    result = convert_to_result_dto(lang_percentage_by_weeks)
    pickle.dump(result, open(get_language_percentage_result_abs_file_name(file_name), "wb"))
    print("count_lang_percentage_and_save_to_file -> end")


def count_number_of_messages_by_time_period(data):
    minimized_messages = list(map(extract_lang_and_date, enumerate(data["messages"])))
    number_of_messages_by_weeks = {}
    for m in minimized_messages:
        if m['beginning_of_week_str'] not in number_of_messages_by_weeks:
            number_of_messages_by_weeks[m['beginning_of_week_str']] = {'uk': 0, 'ru': 0}
        number_of_messages_by_weeks[m['beginning_of_week_str']][m['lang']] = \
            number_of_messages_by_weeks[m['beginning_of_week_str']][m['lang']] + 1
    return number_of_messages_by_weeks


def count_percentages(number_of_messages_by_weeks):
    messages_percentage = {}
    for week_start, messages_counts in number_of_messages_by_weeks.items():
        if week_start not in messages_percentage:
            messages_percentage[week_start] = {'uk': 0.0, 'ru': 0.0}
        total_number_of_messages_per_week = messages_counts['uk'] + messages_counts['ru']
        uk_percentage = percentage(messages_counts['uk'], total_number_of_messages_per_week)
        ru_percentage = percentage(messages_counts['ru'], total_number_of_messages_per_week)
        messages_percentage[week_start]['uk'] = uk_percentage
        messages_percentage[week_start]['ru'] = ru_percentage
        print(
            f"Week: {week_start}. Total number of messages: {total_number_of_messages_per_week}. Uk: {messages_counts['uk']}. Ru: {messages_counts['ru']}. Uk percentage: {uk_percentage}. Ru percentage: {ru_percentage}")
    return messages_percentage


def convert_to_result_dto(messages_percentage):
    result = {
        'week_start': [],
        'uk_percentage': [],
        'ru_percentage': []
    }
    for week_start, language_percentages in messages_percentage.items():
        result['week_start'].append(week_start)
        result['uk_percentage'].append(language_percentages['uk'])
        result['ru_percentage'].append(language_percentages['ru'])
    return result


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
