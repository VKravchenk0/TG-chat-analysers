
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import redirect

from src.blueprints.language_count import language_count


def create_app():
    app = Flask(__name__, static_url_path='')
    app.register_blueprint(language_count)

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

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
