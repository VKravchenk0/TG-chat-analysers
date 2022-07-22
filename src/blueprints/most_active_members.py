import json
from flask import Blueprint, render_template, request, Response
from os.path import exists

from settings import MOST_ACTIVE_MEMBERS_RESULT_FOLDER
from src.data_processors.most_active_members_counter import count_members_activity_and_save_to_file
from src.utils.file_name_utils import validate_and_return_input_file_name, get_language_percentage_result_abs_file_name, \
    get_most_active_members_result_abs_file_name
from src.utils.async_utils import async_start_job
import pickle
import jsonpickle

most_active_members_count_bp = Blueprint('most_active_members_count', __name__, template_folder='templates')


@most_active_members_count_bp.route("/most-active-members")
def input_page():
    return render_template('most-active-members-input.html')


@most_active_members_count_bp.route('/api/most-active-members/upload', methods=['POST'])
def upload_file():
    print("Fie upload start")
    input_file = request.files['file']

    processing_params = json.loads(request.form['processing_params'])
    print("Processing params: ")
    print(processing_params)

    raw_input_result_file_name = request.form['result_file_name']
    print(f"Raw result file name: {raw_input_result_file_name}")

    sanitized_input_result_file_name = validate_and_return_input_file_name(MOST_ACTIVE_MEMBERS_RESULT_FOLDER,
                                                                           raw_input_result_file_name)
    print(f"Sanitized result file name: {sanitized_input_result_file_name}")

    data = json.load(input_file)
    async_start_job(count_members_activity_and_save_to_file, (data, sanitized_input_result_file_name, processing_params))
    return sanitized_input_result_file_name


@most_active_members_count_bp.route("/most-active-members/<file_name>", methods=['GET'])
def result_page(file_name):
    return render_template('most-active-members-result.html')


@most_active_members_count_bp.route("/api/most-active-members/<file_name>", methods=['GET'])
def result_data(file_name):
    print(f"Get data from file uuid: {file_name}")
    file_path = get_most_active_members_result_abs_file_name(file_name)
    file_exists = exists(file_path)

    if not file_exists:
        return Response(
            status=404,
            mimetype='application/json'
        )

    result = pickle.load(open(file_path, "rb"))
    print(f"Result found: {result}")
    # TODO: not sure if using Response instead of app.response_class is fine
    return Response(
        response=jsonpickle.encode(result, unpicklable=False),
        status=200,
        mimetype='application/json'
    )