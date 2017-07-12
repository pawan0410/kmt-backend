import os
from flask_restful import Resource, Api, reqparse
import werkzeug
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_PATH = os.path.join(
    BASE_DIR,
    'static',
    'uploads'
)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

