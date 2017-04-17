"""
© AIG Business. See LICENSE file for full copyright & licensing details.
"""

from datetime import datetime

from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import sqlalchemy

from app.models.document import DocumentModel
from app.extension import db
from app.services.google import GoogleDrive


class DocumentsList(Resource):

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
    def post(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        user_id = current_user['uid']
        fields = request.json
        name, keyword = fields['name'], fields['keyword']

        if not name:
            return {'error': 'Please provide a document name'}, 400

        document = DocumentModel(
            name=name[0:50],
            create_uid=user_id,
            create_time=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            update_uid =user_id,
            update_time=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            own_uid = user_id
        )
        try:
            db.session.add(document)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError:
            return {'error': 'Document was not created.'}, 400

        return [{'id': document.id, 'keyword': keyword[0:20]}], 200


class Documents(Resource):

    @jwt_required
    def get(self, id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        documents = DocumentModel.query.get(id)

        if not documents:
            return []

        if documents.delta:
            delta = str(documents.delta, 'utf-8')
        else:
            delta = ''

        results = {
                    'id': documents.id,
                    'own_uid': documents.own_uid,
                    'name': documents.name,
                    'delta': delta
                }
        return jsonify(documents=[results])

    @jwt_required
    def put(self, id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        if not id:
            return {'error': 'Invalid document ID'}, 400

        fields = request.json

        if not fields:
            return {'error': 'No field provided'}, 400

        user_id = current_user['uid']

        document = DocumentModel.query.get(id)

        if not document or document.own_uid != user_id:
            return {'error': 'Invalid document ID'}, 400

        current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        if fields['fields']['delta']:
            delta = fields['fields']['delta']
            doc_id = document.id

            db.session.execute("""
            UPDATE document SET update_uid= :user_id, update_time= :current_time, delta= :delta WHERE id= :doc_id
            """, {'user_id': user_id, 'current_time': current_time, 'delta': delta, 'doc_id': doc_id})
            db.session.commit()

        if document.delta:
            delta = str(document.delta, 'utf-8')
        else:
            delta = ''

        results = {
            'id': document.id,
            'own_uid': document.own_uid,
            'name': document.name,
            'delta': delta
        }
        return jsonify(documents=[results])

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401

        if not id:
            return {'error': 'Invalid document ID'}, 400
        user_id = current_user['uid']
        document = DocumentModel.query.get(id)

        if not document or document.own_uid != user_id:
            return {'error': 'Invalid document ID'}, 400

        try:
            db.session.delete(document)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError:
            return {'error': 'Document was not deleted.'}, 400

        return []


class Export(Resource):

    @jwt_required
    def post(self, id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Invalid authorization token'}, 401


        if not id:
            return {'error': 'Invalid document ID'}, 400

        user_id = current_user['uid']

        document = DocumentModel.query.get(id)

        if not document or document.own_uid != user_id:
            return {'error': 'Invalid document ID'}, 400

        html_content = request.json['content']

        folder_id = GoogleDrive.create_folder(current_user['name'])

        file_id = GoogleDrive.create_file(document.name, html_content, folder_id)

        return {'file_id': file_id}

















