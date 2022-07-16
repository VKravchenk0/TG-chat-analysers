from flask import Blueprint, send_from_directory

static_files_blueprint = Blueprint('static_files_blueprint', __name__, template_folder='templates')

# serving js files
@static_files_blueprint.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/js', path)


# serving css files
@static_files_blueprint.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('templates/css', path)