from flask import render_template
from flask import Blueprint


default_blueprint = Blueprint('default', __name__, url_prefix='/')


@default_blueprint.route('')
def index():
    return render_template('index.html')