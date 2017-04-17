import re
from datetime import datetime

from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import sqlalchemy

from app.models.keyword import KeywordModel
from app.extension import db


class KeywordsList(Resource):

    @jwt_required
    def get(self, keyword):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        if keyword:
            rows = KeywordModel.query.filter(KeywordModel.name == keyword).all()
            keywords = [{'delta': str(row.delta, 'utf-8')} for row in rows]

        else:
            prefix = request.args.get('prefix')

            if len(prefix) > 2:
                rows = KeywordModel.query.filter(KeywordModel.name.like('%'+prefix+'%')).order_by('name').limit(5)
                keywords = [{'delta': str(row.delta, 'utf-8')} for row in rows]

        return keywords


class KeywordsListPrefix(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        prefix = request.args.get('prefix')

        keywords = []

        if len(prefix) > 2:
            rows = KeywordModel.query.filter(KeywordModel.name.like('%'+prefix+'%')).order_by('name').limit(5)
            keywords = [row.name for row in rows]

        return keywords

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        data = request.json
        name = data['name']
        delta = data['delta']

        user_id = current_user['uid']

        if not name or re.match('/^\.[a-zA-Z0-9_-]*$/', name):
            return {'error': 'Please provide a valid smart keyword name.'}

        keyword = KeywordModel.query.filter(KeywordModel.name == name).first()

        if keyword:
            return {'error': 'This smart keyword already exists.'}

        keyword = KeywordModel(
            name=name[0:50],
            delta=bytes(delta, 'utf-8'),
            create_uid=user_id,
            create_time=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            update_uid=user_id,
            update_time=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        )

        try:
            db.session.add(keyword)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError:
            return {'error': 'Smart keyword was not created.'}
        return {'id': keyword.id}