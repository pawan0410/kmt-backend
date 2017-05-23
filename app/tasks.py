from app.extension import task_server
from app.winldap.ldap import list_all_users
from app.application import application
from app.models.user import UserModel
from app.extension import db
import sqlalchemy



@task_server.task()
def import_users_from_ldapserver():
    app = application('local')
    with app.test_request_context():
        db.session.query(UserModel).delete(synchronize_session='evaluate')
        user = [
            UserModel(
                name=user['name'],
                email=user['email'],
                department=user['department']
            )
            for user in list_all_users()
            ]

        try:
            db.session.add_all(user)
            db.session.commit()
        except sqlalchemy.exc.ProgrammingError as e:
            return str(e)