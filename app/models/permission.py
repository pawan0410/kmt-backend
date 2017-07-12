from app.extension import db


class PermissionModel(db.Model):
    __tablename__ = 'permission'


    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)
    doc_id = db.Column(db.Integer)

