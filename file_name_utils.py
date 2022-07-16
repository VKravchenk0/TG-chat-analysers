import glob
import re
from pathvalidate import sanitize_filename
from settings import LANG_PERCENTAGE_RESULT_FOLDER


def get_language_percentage_result_abs_file_name(file_name):
    return f"{LANG_PERCENTAGE_RESULT_FOLDER}/{file_name}.p"


def validate_and_return_input_file_name(raw_input_result_file_name):
    print(f"validate_and_return_input_file_name start. File name: {raw_input_result_file_name}")
    if not raw_input_result_file_name:
        return raw_input_result_file_name

    sanitized_user_input = sanitize_filename(raw_input_result_file_name).strip()
    files_with_same_name = glob.glob(f"{LANG_PERCENTAGE_RESULT_FOLDER}/{sanitized_user_input}*.p")
    print(f"Files with same name: {files_with_same_name}")
    if not files_with_same_name:
        # returning sanitized user input
        print("No files found. Returning sanitized user input")
        return sanitized_user_input

    return get_next_file_name(files_with_same_name, sanitized_user_input)


def get_next_file_name(existing_files, sanitized_user_input):
    print(f"get_next_file_name. Sanitized user input: {sanitized_user_input}. \nExisting files: \n{existing_files}")
    file_numbers = [extract_number(absolute_file_name, sanitized_user_input) for absolute_file_name in
                    existing_files]
    print(f"File numbers: {file_numbers}")
    next_value = get_next_number(file_numbers)
    next_file_name = f"{sanitized_user_input}_{next_value}"
    print(f"next file name: {next_file_name}")
    return next_file_name


def get_next_number(file_numbers):
    file_numbers_as_ints = [int(n) if (n and n.isnumeric()) else 0 for n in file_numbers]
    print(f"file numbers as ints: {file_numbers_as_ints}")
    max_value = max(file_numbers_as_ints)
    print(f"max value: {max_value}")
    next_value = max_value + 1
    return next_value


def extract_number(absolute_file_name, fn_without_extension):
    print(f"extract_number start. absolute file name: {absolute_file_name}. fn without extension: {fn_without_extension}")
    step1 = re.sub(f"^{LANG_PERCENTAGE_RESULT_FOLDER}/{fn_without_extension}", '', absolute_file_name)
    print(f"step1 result: {step1}")

    # step to handle filenames without number (the first file)
    step2 = re.sub(f"^_", '', step1)
    print(f"step2 result: {step2}")

    step3 = re.sub(f".p$", '', step2)
    print(f"step3 result: {step3}")
    return step3