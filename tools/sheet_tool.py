import os
import gspread
import openai
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

os.environ["OPENAI_API_KEY"] = "NULL"
os.environ["openai_api_base"] = "http://localhost:1234/v1"

# Setup OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(
    api_key=openai.api_key,
    base_url="http://localhost:1234/v1"
)

# Setup Google Sheets
spread_sheets_id = os.getenv('SPREAD_SHEET_ID')
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(spread_sheets_id).sheet1

# Function to log missing information
def log_missing_information(row, col, header, timestamp):
    print(f"Missing information at Row: {row}, Column: {col}, Column Header: '{header}', Timestamp: {timestamp}")

# Function to scan the sheet for missing information
def scan_for_missing_info(sheet):
    data = sheet.get_all_values()
    # Assuming the first row is the header
    headers = data[0] if data else []
    # Starting scan from the second row since the first row contains headers
    for i, row in enumerate(data[1:], start=2): # Adjusted to skip header row in logging
        for j, cell in enumerate(row, start=1):
            if cell == "":  # Checking if the cell is empty
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                header = headers[j-1] if j <= len(headers) else "Unknown Header" # Handling cases where the column may not have a header
                log_missing_information(i, j, header, timestamp)

# Call the function to start scanning
scan_for_missing_info(sheet)
print("Scan complete. Check the log for missing information.")

