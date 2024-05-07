import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

spread_sheets_id = os.getenv('SPREAD_SHEET_ID')
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(spread_sheets_id).sheet1

def log_missing_information(row, col, header, company_name, timestamp):
    print(f"Missing information at Row: {row}, Column: {col}, Column Header: '{header}', Company: '{company_name}', Timestamp: {timestamp}")

def scan_for_missing_info(sheet):
    data = sheet.get_all_values()
    headers = data[0] if data else []
    company_index = headers.index('Company Name') if 'Company Name' in headers else None
    for i, row in enumerate(data[1:], start=2):
        company_name = row[company_index] if company_index is not None else "Unknown"
        for j, cell in enumerate(row, start=1):
            if cell == "":
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                header = headers[j-1] if j <= len(headers) else "Unknown Header"
                log_missing_information(i, j, header, company_name, timestamp)

scan_for_missing_info(sheet)
print("Scan complete.")