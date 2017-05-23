from app.extension import db


class UserModel(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer , primary_key=True)
    create_uid = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    update_uid = db.Column(db.Integer)
    update_time = db.Column(db.DateTime)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    department = db.Column(db.String(255))




