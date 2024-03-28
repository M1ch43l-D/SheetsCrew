from crewai import Agent, Task, Crew
from crewai_tools import BaseTool
import google.auth
from googleapiclient.discovery import build


# Custom tool for Google Sheets interaction
class GoogleSheetsTool(BaseTool):
    name = "GoogleSheetsTool"
    description = "Interacts with Google Sheets to read and write data"

    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.service = self.authenticate_google_sheets()

    def authenticate_google_sheets(self):
        creds, _ = google.auth.default()
        service = build('sheets', 'v4', credentials=creds)
        return service

    def read_sheet(self, range_name):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=range_name).execute()
        return result.get('values', [])

    def write_to_sheet(self, range_name, values):
        body = {'values': values}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        return result

    def _run(self, argument: str) -> str:
        # Implementation of the logic to decide whether to read or write,
        # and potentially calling other tools for data retrieval.
        pass