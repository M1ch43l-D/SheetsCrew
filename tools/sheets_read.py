from dotenv import load_dotenv
import os
load_dotenv()
from crewai_tools import BaseTool
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime

service_account_file = "path/to/service_account.json"  # Replace with the actual path to the service account file

credentials = Credentials.from_service_account_file(service_account_file)
title = sheets[0].get("properties", {}).get("title", "Sheet1")
print(f"First sheet title: {title}")

SERVICE_ACCOUNT_FILE='/Users/mcnas/OneDrive/Documents/VS/sheetscrew/SheetsCrew/qualified-world-414006-0223c92c9791.json'


class GoogleSheetsReadTool(BaseTool):
    name: str = "GoogleSheetsReadTool"
    description: str = "Scans a Google Sheet to identify rows and columns with missing information."

    def _run(self, service_account_file: str, spreadsheet_id: str, range: str) -> str:
        # Authenticate and construct the service
        credentials = Credentials.from_service_account_file(service_account_file)
        service = build('sheets', 'v4', credentials=credentials)

        # Read the data from the specified range in the sheet
        sheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
        values = sheet.get('values', [])

        # Identify missing data
        missing_data_info = []
        for row_idx, row in enumerate(values):
            for col_idx, value in enumerate(row):
                if value == '':  # or use `if not value:` to catch None values as well
                    missing_data_info.append((row_idx + 1, col_idx + 1))  # Adding 1 to match the actual sheet's indexing

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            'missing_data_info': missing_data_info,
            'timestamp': timestamp
        }

        return str(result)
