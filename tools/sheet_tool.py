from crewai_tools import BaseTool
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import datetime
from typing import ClassVar


class GoogleSheetsTool(BaseTool):
    credentials_path: ClassVar[str] = '/Users/mcnas/OneDrive/Documents/VS/sheetscrew/SheetsCrew/qualified-world-414006-0223c92c9791.json'
    name: str = "GoogleSheetsTool"
    description: str = "Interact with Google Sheets for data scanning and updating."

    # Set your credentials path here
    credentials_path = '/Users/mcnas/OneDrive/Documents/VS/sheetscrew/SheetsCrew/qualified-world-414006-0223c92c9791.json'

    def _run(self, action: str, sheet_id: str, data=None) -> str:
        # Setup Google Sheets with the specific credentials path
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(sheet_id).sheet1

        if action == "scan":
            return self.scan_for_missing_data(sheet)
        elif action == "update":
            return self.update_sheet(sheet, data)
        else:
            return "Invalid action"

    def scan_for_missing_data(self, sheet) -> str:
        missing_data_info = []
        data = sheet.get_all_values()
        for row_index, row in enumerate(data, start=1):
            for col_index, value in enumerate(row, start=1):
                if not value:  # Checks if the cell is empty
                    missing_data_info.append(f"Row: {row_index}, Column: {col_index}")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Missing Data at {timestamp}: " + ", ".join(missing_data_info)

    def update_sheet(self, sheet, update_instructions) -> str:
        for instruction in update_instructions:
            row, col, value = instruction
            sheet.update_cell(row, col, value)
        return f"Updated {len(update_instructions)} cells successfully."
