import time
from datetime import datetime


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