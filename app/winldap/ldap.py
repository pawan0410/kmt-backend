import hashlib
import ldap
from flask import current_app
from app.models.user import UserModel
from app.extension import db


base = "dc=aig , dc= local"
criteria = "(&(objectCategory=person)(objectClass=user))"
attrs = ['displayName', 'sAMAccountName', 'userPrincipalName', 'department', 'telephoneNumber']


def ldap_server():
    return ldap.initialize(
        current_app.config['LDAP_SERVER']
    )


def set_protocol_version(server):
    server.protocol_version = ldap.VERSION3
    server.set_option(ldap.OPT_REFERRALS, 0)


def ldap_login():
    server = ldap_server()
    set_protocol_version(server)
    try:
        server.bind_s(
            current_app.config['LDAP_USER'],
            current_app.config['LDAP_PASSWORD']
        )
    except ldap.LDAPError as e:
        print('Authentication Fails')

    return server


def list_all_users():
    server = ldap_login()
    result = server.search_s(base, ldap.SCOPE_SUBTREE, criteria, attrs)
    results = [entry for dn, entry in result if isinstance(entry, dict)]

    output = []
    for r in results:
        try:
            output.append(
                dict(
                    name=r['displayName'][0],
                    create_uid=r['sAMAccountName'][0],
                    email=r['userPrincipalName'][0],
                    department=r['department'][0]
                )
            )
        except KeyError as e:
            current_app.logger.warn(e)

    return output


def load_users():
    db.session.query(UserModel).delete(synchronize_session = 'evaluate')
    user = [
        UserModel(
            name=user['name'],
            email=user['email'],
            department = user['department'],
            password_hash=hashlib.md5(str(user['name']).encode()).hexdigest()
        )
        for user in list_all_users()
        ]

    try:
        db.session.add_all(user)
        db.session.commit()
    except sqlalchemy.exc.ProgrammingError as e:
        return str(e)
















