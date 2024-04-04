from dotenv import load_dotenv
import os
load_dotenv()
from crewai_tools import BaseTool
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')

# The ID of the spreadsheet to update
SPREADSHEET_ID = '1sM5mGpuKjysqj5qcLqSbU3EcgO5WW8fpO5tJhuc2mmk'  # Replace with your actual spreadsheet ID

# Authenticate and construct service
credentials = Credentials.from_service_account_file(service_account_file, scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build('sheets', 'v4', credentials=credentials)

# Specify the range and values to update
range_name = 'Sheet1!A2:D2'  # Adjust 'Sheet1' if your sheet is named differently
values = [
    ['Confirmed', 'Confirmed B', 'Confirmed C', 'Confirmed D']  # Values to be written
]

# Prepare the request body and update the sheet
body = {'values': values}
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=range_name,
    valueInputOption='USER_ENTERED', body=body).execute()

print(f"{result.get('updatedCells')} cells updated.")