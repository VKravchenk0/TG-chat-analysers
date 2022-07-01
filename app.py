import os

import jsonpickle
from flask import Flask, render_template, request, send_from_directory, send_file
import io
from flask import Response, redirect
import pickle

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
    def client_side_rendering():
        return render_template('index.html')

    @app.route("/api/data")
    def get_data():
        result = pickle.load(open("resources/save.p", "rb"))
        print(result)
        obj = {'var': 'hello'}
        response = app.response_class(
            response=jsonpickle.encode(result, unpicklable=False),
            status=200,
            mimetype='application/json'
        )
        return response

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
