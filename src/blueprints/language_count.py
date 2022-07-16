from flask import Blueprint, render_template, request, Response
from os.path import exists

from src.utils.file_name_utils import validate_and_return_input_file_name, get_language_percentage_result_abs_file_name
from src.lang.lang_percentage_counter import async_count_lang_percentage_and_save_to_file
import pickle
import jsonpickle

language_count = Blueprint('language_count', __name__,
                           template_folder='templates')


@language_count.route("/language")
def lang_usage_page():
    return render_template('language-input.html')


@language_count.route('/api/language/upload', methods=['POST'])
def lang_usage_upload_file():
    print("Fie upload start")
    input_file = request.files['file']
    user_stop_list = [x.strip() for x in request.form['user_stop_list'].split(',')]
    print(f"Stop list: {user_stop_list}")

    raw_input_result_file_name = request.form['result_file_name']
    print(f"Raw result file name: {raw_input_result_file_name}")

    sanitized_input_result_file_name = validate_and_return_input_file_name(raw_input_result_file_name)
    print(f"Sanitized result file name: {sanitized_input_result_file_name}")

    result_file_name = async_count_lang_percentage_and_save_to_file(
        input_file, user_stop_list, file_name_without_extension=sanitized_input_result_file_name)
    return result_file_name


@language_count.route("/language/<file_uuid>", methods=['GET'])
def get_language_render_page(file_uuid):
    return render_template('language-result.html')


@language_count.route("/api/language/<file_uuid>", methods=['GET'])
def get_language_data(file_uuid):
    print(f"Get data from file uuid: {file_uuid}")
    file_path = get_language_percentage_result_abs_file_name(file_uuid)
    file_exists = exists(file_path)

    if not file_exists:
        return Response(
            status=404,
            mimetype='application/json'
        )

    result = pickle.load(open(file_path, "rb"))

    # TODO: not sure if using Response instead of app.response_class is fine
    return Response(
        response=jsonpickle.encode(result, unpicklable=False),
        status=200,
        mimetype='application/json'
    )