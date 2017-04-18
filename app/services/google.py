import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

from flask import current_app


class GoogleDrive(object):
    @staticmethod
    def get_credentials():
        """Gets valid user credentials from storage.

            If nothing has been stored, or if the stored credentials are invalid,
            the OAuth2 flow is completed to obtain the new credentials.

            Returns:
                Credentials, the obtained credential.
            """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'drive-python.json')

        store = Storage(credential_path)

        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(current_app.config['CLIENT_SECRET_FILE'],
                                                  current_app.config['SCOPES'])
            flow.user_agent = current_app.config['APPLICATION_NAME']

            credentials = tools.run_flow(flow, store, None)
            current_app.logger.info('Storing credentails to %s' % credential_path)
        return credentials

    @staticmethod
    def service():
        credentials = GoogleDrive.get_credentials()
        http = credentials.authorize(httplib2.Http())
        return discovery.build('drive', 'v3', http=http)

    @staticmethod
    def create_folder(name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = GoogleDrive.service().files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    @staticmethod
    def create_file(name, content, folder_id):
        file_metadata = {
            'name': name,
            'parents': [folder_id]
        }
        html_file = '{0}/temp_uploads/{1}.html'.format(current_app.config['BASE_DIR'], name.replace(' ', '_'))

        current_app.logger.info("The HTML File %s " % html_file)

        with open(html_file, 'w+') as fp:
           fp.write(content)
           fp.close()

        media = MediaFileUpload(html_file,
                                mimetype='text/html',
                                resumable=True)
        file = GoogleDrive.service().files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()

        os.remove(html_file)

        return file.get('id')
