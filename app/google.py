from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask import current_app


def login():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)  # Create GoogleDrive instance with authenticated GoogleAuth instance
    return gauth, drive


def upload(name, content):
    auth, drive = login()
    file = drive.CreateFile({
        'title': name,
        'mimeType': 'text/html',
        'parents': [current_app.config['DRIVE_FOLDER_ID']],
    })

    file.SetContentString(content)
    file.Upload()
    return file['id']