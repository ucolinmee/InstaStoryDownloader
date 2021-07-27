from __future__ import print_function
import os.path
import httplib2
from apiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import oauth


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


class DriveAPI:
    def __init__(self):
        authInst = oauth.Auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
        credentials = authInst.getCredentials()

        http = credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v3', http=http)

    def listFiles(self, size):
        results = self.drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))

    def uploadFile(self, filename, filepath, mimetype, folder_id):
        flder_id = folder_id
        file_metadata = {'name': filename,
                         'parents': [flder_id]}
        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
        file = self.drive_service.files().create(body=file_metadata,
                                                 media_body=media,
                                                 fields='id').execute()




























# # If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive']
#
# class DriveAPI:
#     def __init__(self):
#         pass
#
#     def main(self):
#         """Shows basic usage of the Drive v3 API.
#         Prints the names and ids of the first 10 files the user has access to.
#         """
#         creds = None
#         # The file token.json stores the user's access and refresh tokens, and is
#         # created automatically when the authorization flow completes for the first
#         # time.
#         if os.path.exists('token.json'):
#             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#         # If there are no (valid) credentials available, let the user log in.
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     'credentials.json', SCOPES)
#                 creds = flow.run_local_server(port=0)
#             # Save the credentials for the next run
#             with open('token.json', 'w') as token:
#                 token.write(creds.to_json())
#
#
#         service = build('drive', 'v3', credentials=creds)
#
#         # Call the Drive v3 API
#         results = service.files().list(
#             pageSize=10, fields="nextPageToken, files(id, name)").execute()
#         items = results.get('files', [])
#
#         if not items:
#             print('No files found.')
#         else:
#             print('Files:')
#             for item in items:
#                 print(u'{0} ({1})'.format(item['name'], item['id']))
#
#         def uploadFile(self, filename, filepath, mimetype):
#             file_metadata = {'name': filename}
#             media = MediaFileUpload(filepath, mimetype=mimetype)
#             file = service.files().create(body=file_metadata,
#                                                 media_body=media,
#                                                 fields='id').execute()
#
#
#
#
#
#
#     if __name__ == '__main__':
#         main()



# API_KEY = "AIzaSyAqSLuzTm4iRYQlBN2wYHKffZMlVj5ioWE"
# CLIENT_ID = "513632947211-loan84pu432k10dlg5qlqluu3s1udkao.apps.googleusercontent.com"
# SECRET_KEY = "150zkHEct4xuBWilBZY0PeDL"


