from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity


class Documents(Resource):

    def get(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        return {'token': ''}
