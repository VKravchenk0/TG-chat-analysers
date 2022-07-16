import pickle

from src.utils.file_name_utils import get_most_active_members_result_abs_file_name


def count_members_activity_and_save_to_file(data, file_name):
    print("count_activity_and_save_to_file -> start")
    print(f"original messages length: {len(data['messages'])}")
    result = {"i": "I'm an object"}
    pickle.dump(result, open(get_most_active_members_result_abs_file_name(file_name), "wb"))
    print("count_lang_percentage_and_save_to_file -> end")