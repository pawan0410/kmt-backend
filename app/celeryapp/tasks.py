from app.models.user import UserModel
from app.extension import db
from app.winldap.ldap import list_all_users
from app.application import application
from .celery import task_server


@task_server.task()
def load_users():
    from app.winldap.ldap import list_all_users
    app = application('development')

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
