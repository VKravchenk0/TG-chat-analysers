import json
from flask import Blueprint, render_template, request, Response
from os.path import exists

from settings import LANG_PERCENTAGE_RESULT_FOLDER
from src.utils.file_name_utils import validate_and_return_input_file_name, get_language_percentage_result_abs_file_name
from src.data_processors.lang_percentage_counter import count_lang_percentage_and_save_to_file
from src.data_processors.counters import LanguagePercentageCounterType, TimeSpanType
from src.utils.async_utils import async_start_job
import pickle
import jsonpickle

language_count_bp = Blueprint('language_count', __name__,
                              template_folder='templates')


@language_count_bp.route("/language")
def input_page():
    return render_template('language-input.html')


@language_count_bp.route('/api/language/upload', methods=['POST'])
def upload_file():
    print("Fie upload start")
    input_file = request.files['file']
    user_stop_list = [x.strip() for x in request.form['user_stop_list'].split(',')]
    print(f"Stop list: {user_stop_list}")

    counter_type = LanguagePercentageCounterType.WEIGHTED
    if 'counter_type' in request.form:
        request_counter_type = request.form.get('counter_type')
        print(f'counter_type is present in request: {request_counter_type}')
        counter_type = LanguagePercentageCounterType[request_counter_type]
    print(f"selected counter type: {counter_type}")

    timespan_type = TimeSpanType.WEEK
    if 'timespan_type' in request.form:
        request_timespan_type = request.form.get('timespan_type')
        print(f'request_timespan_type is present in request: {request_timespan_type}')
        timespan_type = TimeSpanType[request_timespan_type]
    print(f"selected timespan type: {timespan_type}")

    raw_input_result_file_name = request.form['result_file_name']
    print(f"Raw result file name: {raw_input_result_file_name}")

    sanitized_input_result_file_name = validate_and_return_input_file_name(LANG_PERCENTAGE_RESULT_FOLDER,
                                                                           raw_input_result_file_name, counter_type,
                                                                           timespan_type)
    print(f"Sanitized result file name: {sanitized_input_result_file_name}")

    data = json.load(input_file)
    async_start_job(count_lang_percentage_and_save_to_file,
                    (data, sanitized_input_result_file_name, user_stop_list, counter_type, timespan_type)
                    )
    return sanitized_input_result_file_name


@language_count_bp.route("/language/<file_name>", methods=['GET'])
def result_page(file_name):
    return render_template('language-result.html')


@language_count_bp.route("/api/language/<file_name>", methods=['GET'])
def result_data(file_name):
    print(f"Get data from file uuid: {file_name}")
    file_path = get_language_percentage_result_abs_file_name(file_name)
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