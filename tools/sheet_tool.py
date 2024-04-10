import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from crewai_tools import tool

class GoogleSheetsTool:
    def __init__(self):
        self.client = self.setup_google_sheets()

    def setup_google_sheets(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        return gspread.authorize(credentials)

    @tool("Audit Sheet")
    def audit_sheet(self, sheet_id: str) -> list:
        """Prepares research queries based on missing data and row headers."""
        sheet = self.client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)
        headers = worksheet.row_values(1)  # Assuming the first row contains headers
        data = worksheet.get_all_values()[1:]  # Skip header row
        missing_data_info = []
        for row_index, row in enumerate(data, start=2):  # Adjust for header row
            for col_index, cell in enumerate(row, start=1):
                if not cell:  # Cell is empty
                    header = headers[col_index - 1]
                    # Formulate a search query based on the header and potentially other cell values in the row
                    search_query = f"Find {header} for {row[0]}"  # Example, using the first column as a reference
                    missing_data_info.append({"row": row_index, "col": col_index, "query": search_query})
        return missing_data_info

    @tool("Update Google Sheet")
    def update_sheet(self, sheet_id: str, updates: list) -> None:
        """Updates the Google Sheet with provided data."""
        sheet = self.client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)
        for update in updates:
            row, col, value = update
            worksheet.update_cell(row, col, value)
            
if __name__ == "__main__":
    sheet_tool = GoogleSheetsTool()
    sheet_id = os.getenv("SPREAD_SHEET_ID")
    research_queries = sheet_tool.audit_sheet(sheet_id)
    # Process research_queries to fill missing data
    updates = [(query["row"], query["col"], "Researched Data") for query in research_queries]  # Example update
    sheet_tool.update_sheet(sheet_id, updates)
