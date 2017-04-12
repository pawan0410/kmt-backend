"""
© AIG Business. See LICENSE file for full copyright & licensing details.
"""

import hashlib
import time
from flask_restful import Resource
from app.models.user import UserModel
from flask import current_app
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


class Auth(Resource):

    def post(self):
        data = request.json

        try:
            email = data['email']
            password = hashlib.md5(data['password'].encode()).hexdigest()
        except KeyError:
            email, password = None, None

        user = UserModel.query.filter(UserModel.email == email, UserModel.password_hash == password).first()

        if not user:
            return {'error': 'Invalid email/password combination.'}, 401

        response = {
            'uid': user.id,
            'name': user.name,
            'issued': int(time.time()),
            'lifetime': current_app.config['TOKEN_LIFETIME']
        }

        return {'token': create_access_token(identity=response)}, 200


class Validate(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401
        else:
            return {'token': create_access_token(identity=current_user)}, 200


