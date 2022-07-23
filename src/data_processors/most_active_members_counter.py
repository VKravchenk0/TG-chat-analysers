import pickle

from src.utils.file_name_utils import get_most_active_members_result_abs_file_name
from src.utils.text_utils import remove_formatting, squash_sequential_message_from_same_person


def build_username_messages_count_dictionary(data):
    """
    Builds a dictionary with username as a key and number of messages from this user as a value
    :param data: json data with telegram chat export results
    """
    result_dict = {}
    for message in data["messages"]:
        if "from" not in message or message["from"] is None:
            continue

        # from_field = normalize_from_field(message["from"])
        from_field = message["from"]
        if from_field not in result_dict:
            # add a new record
            result_dict[from_field] = 1
        else:
            # increment
            result_dict[from_field] = result_dict[from_field] + 1

    return result_dict


def trim_bottom_members(input, top_members_to_display):
    """
    Returns the last top_members_to_display records from the input dictionary
    """
    input_length = len(input)
    last_n_results = list(input.items())[input_length - top_members_to_display: input_length]
    result = {}
    for item in last_n_results:
        result[item[0]] = item[1]

    return result


def sort_dictionary_by_messages_count(input):
    return dict(sorted(input.items(), key=lambda item: item[1]))


def filter_only_text_messages(data):
    messages = list(filter(is_relevant_message, data["messages"]))
    print(f"Filtered only text messages. Messages length: {len(messages)}")
    return messages


def is_relevant_message(message):
    # if "from" not in message or message["from"] is None:
    #     return False
    # return True
    if "type" not in message or message["type"] is None or message["type"] != "message":
        return False
    if "forwarded_from" in message:
        return False
    if "text" not in message or message["text"] is None or (
            isinstance(message["text"], str) and message["text"].strip() == ""):
        return False
    return True


def count_members_activity_and_save_to_file(data, file_name, processing_params):
    print("count_activity_and_save_to_file -> start")
    print(f"original messages length: {len(data['messages'])}")
    messages = filter_only_text_messages(data)
    messages = remove_formatting(messages)
    messages = squash_sequential_message_from_same_person(messages)
    data["messages"] = messages

    all_members_dict = build_username_messages_count_dictionary(data)

    result_dict = sort_dictionary_by_messages_count(all_members_dict)

    # df1 = pd.DataFrame(all_members_dict)
    # df2 = pd.DataFrame(sorted_dict)
    #
    # df1 = pd.DataFrame(all_members_dict.items())
    # d1 = df1[1].describe()
    #
    # df2 = pd.DataFrame(sorted_dict.items())
    # d2 = df2[1].describe()

    print(f"Before threshold trim step: {result_dict}")

    result_dict = trim_members_by_message_number_threshold_if_needed(processing_params, result_dict)

    print(f"Before members number trim step: {result_dict}")

    result_dict = trim_members_if_needed(processing_params, result_dict)

    print(f"After members number trim step: {result_dict}")

    result_as_lists = {
        'members': list(result_dict.keys()),
        'number_of_messages': list(result_dict.values())
    }
    print(f"result as list: {result_as_lists}")
    pickle.dump(result_as_lists, open(get_most_active_members_result_abs_file_name(file_name), "wb"))
    print("count_lang_percentage_and_save_to_file -> end")


def trim_members_if_needed(processing_params, result_dict):
    if processing_params.get('number_of_members_to_display') \
            and isinstance(processing_params.get('number_of_members_to_display'), int):
        result_dict = trim_bottom_members(result_dict, processing_params.get('number_of_members_to_display'))
    return result_dict


def trim_members_by_message_number_threshold_if_needed(processing_params, result_dict):
    if processing_params.get('min_message_threshold') \
            and isinstance(processing_params.get('min_message_threshold'), int):
        threshold = processing_params.get('min_message_threshold')
        result_dict = {k: v for k, v in result_dict.items() if v >= threshold}
    return result_dict