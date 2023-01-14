from flask import Flask
from werkzeug.utils import redirect

from src.blueprints.language_count_blueprint import language_count_bp
from src.blueprints.most_active_members_blueprint import most_active_members_count_bp
from src.blueprints.static_blueprint import static_files_blueprint

# кількість повідомлень на один день перебування в чаті (?)
def create_app():
    app = Flask(__name__, static_url_path='')
    app.register_blueprint(static_files_blueprint)
    app.register_blueprint(language_count_bp)
    app.register_blueprint(most_active_members_count_bp)

    # https://flatlogic.com/blog/top-mapping-and-maps-api/
    @app.route("/")
    def index():
        return redirect('/language', code=302)

    return app


application = create_app()

if __name__ == "__main__":
    application.run()
