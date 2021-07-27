import os
from Google import Create_Service
import pandas as pd


CLIENT_SECRET_FILE = 'credentials.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = "1uvQtOPdKIEJv6lX33lwSHgTUKarvAAUHcm7lV9AC2DM"


class SheetsAPI:
    def __init__(self):
        self.service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)


    def read_sheet(self):
        response = self.service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            majorDimension="ROWS",
            range="Sheet1"
        ).execute()
        return response







