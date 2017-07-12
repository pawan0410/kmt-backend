import hashlib
from datetime import datetime

from flask_restful import Resource, Api, reqparse
import werkzeug

import os
from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import sqlalchemy

from app.models.user import UserModel
from app.extension import db


class UserList(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        term = request.args.get('term')

        if term:
            users = UserModel.query.\
                filter(UserModel.name.like("%"+term+"%")).all()

        else:
            users = UserModel.query.all()
        if not users:
            return []
        results = [{
            'name' : user.name,
            'email' : user.email,
            'id' : user.id
        } for user in users]
        return jsonify(users=results)



    @jwt_required
    def post(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        UPLOAD_PATH = os.path.join(
            BASE_DIR,
            'static',
            'uploads'
        )
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        user_id = current_user['uid']
        fields = request.json
        name, email,f_name = fields['name'], fields['email'] ,fields['f_name']
        file = request.files['img']
        file.save(UPLOAD_PATH, f_name)

        if not name:
            return {'error': 'Please provide a user name'}, 400


        user = UserModel(
            name=name,
            email = email,
            password_hash = hashlib.md5(name.encode('UTF-8')).hexdigest(),
            create_uid=user_id,
            create_time=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            update_uid=user_id,
            update_time=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            profile_pic_path = UPLOAD_PATH

        )
        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError:
            return {'error': 'User was not created.'}, 400

        return {'id': user.id, 'email': email }, 200


class Users(Resource):
    @jwt_required
    def get(self,id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        user = UserModel.query.get(id)
        if not user:
            return []
        results = [{
                       'name': user.name,
                       'email': user.email,
                       'id': user.id,
                   }]
        return jsonify(users=results)

    @jwt_required
    def put(self, id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        user = UserModel.query.get(id)
        if not user:
            return []

        fields = request.json
        name, email  = fields['name'], fields['email']

        user.name = name
        user.email = email
        user.update_uid = current_user['uid']
        user.update_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


        db.session.add(user)
        db.session.commit()

        return jsonify(users=[{
            'name': user.name,
            'email' : user.email
        }])

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        user = UserModel.query.get(id)
        if not user:
            return []
        try:
            db.session.delete(user)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError:
            return {'error': 'User was not deleted.'}, 400

        return []



