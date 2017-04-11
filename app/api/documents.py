from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from app.models.document import DocumentModel


class Documents(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        term = request.args.get('term')

        if term:
            documents = DocumentModel.query.\
                filter(DocumentModel.name.like("%"+term+"%")).all()
        else:
            documents = DocumentModel.query.all()

        if not documents:
            return []

        results= [
            {
                'id': doc.id,
                'update_time': doc.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'name': doc.name,
            } for doc in documents]
        return jsonify(documents=results)

    @jwt_required
    def put(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        id = request.args.get('id')

        if not id:
            return {'error': 'Invalid document ID'}, 400

        fields = request.args.get('fields')

        if not fields:
            return {'error': 'No field provided'}, 400













