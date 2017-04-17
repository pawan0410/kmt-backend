from app.extension import db


class KeywordModel(db.Model):
    __tablename__ = 'keyword'

    id = db.Column(db.Integer , primary_key=True)
    create_uid = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    update_uid = db.Column(db.Integer)
    update_time = db.Column(db.DateTime)
    name = db.Column(db.String(255))
    delta = db.Column(db.LargeBinary)