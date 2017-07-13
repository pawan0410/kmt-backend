from flask import render_template
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from flask import request
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

import os


default_blueprint = Blueprint('default', __name__, url_prefix='/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#UPLOAD_FOLDER = '/path/to/the/uploads'
UPLOAD_PATH = os.path.join(
        BASE_DIR,
        'static',
        'uploads'
    )
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH


@default_blueprint.route('')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@default_blueprint.route('profile_upload', methods=['POST'])
def profile_upload():

    ALLOWED_EXTENSIONS = set(['png', 'jpg'])
    current_user = get_jwt_identity()
    if not current_user:
        return {'error': 'Invalid authorization token'}, 401

    user_id = current_user['uid']

    file = request.files['img']
    if 'file' not in request.files:
        print('No file part')

    file_path = os.join(UPLOAD_PATH, file.filename)
    if file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS :


        file.save(file_path, file.filename)
        return 'Success'
    else :
        print('This file type is not supported')
