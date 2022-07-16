import jsonpickle
from flask import Flask, render_template, request, send_from_directory
import pickle
from os.path import exists
from werkzeug.utils import redirect

from lang_percentage_counter import async_count_lang_percentage_and_save_to_file


def create_app():
    app = Flask(__name__, static_url_path='')

    # serving js files
    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('templates/js', path)

    # serving css files
    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('templates/css', path)

    # https://flatlogic.com/blog/top-mapping-and-maps-api/
    @app.route("/")
    def index():
        return redirect('/language', code=302)

    @app.route("/language")
    def lang_usage_page():
        return render_template('language-input.html')

    @app.route('/api/language/upload', methods=['POST'])
    def lang_usage_upload_file():
        print("Fie upload start")
        if request.method == 'POST':
            input_file = request.files['file']
            user_stop_list = [x.strip() for x in request.form['user_stop_list'].split(',')]
            print("Stop list:")
            print(user_stop_list)
            file_uuid = async_count_lang_percentage_and_save_to_file(input_file, user_stop_list)
            return str(file_uuid)

    @app.route("/language/<file_uuid>", methods=['GET'])
    def get_language_render_page(file_uuid):
        return render_template('language-result.html')

    @app.route("/api/language/<file_uuid>", methods=['GET'])
    def get_language_data(file_uuid):
        print(f"Get data from file uuid: {file_uuid}")
        file_path = f"resources/lang_percentage_result/{file_uuid}.p"
        file_exists = exists(file_path)

        if not file_exists:
            return app.response_class(
                status=404,
                mimetype='application/json'
            )

        result = pickle.load(open(file_path, "rb"))
        return app.response_class(
            response=jsonpickle.encode(result, unpicklable=False),
            status=200,
            mimetype='application/json'
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
