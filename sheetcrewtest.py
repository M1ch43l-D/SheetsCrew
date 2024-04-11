import os
from dotenv import load_dotenv
import gspread
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import openai

# Load environment variables
load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SPREAD_SHEET_ID = os.getenv('SPREAD_SHEET_ID')
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY if OPENAI_API_KEY else "NULL"
os.environ["openai_api_base"] = "http://localhost:1234/v1"

# Setup OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(
    api_key=openai.api_key,
    base_url="http://localhost:1234/v1"
)

@tool("Google Sheet Scanner")
def google_sheet_scanner(spread_sheets_id: str) -> str:
    """Scans Google Sheets for missing information."""
    # Setup Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS_PATH, scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(spread_sheets_id).sheet1

    missing_info_log = []

    # Scan for missing information, including headers
    data = sheet.get_all_values()
    headers = data[0] if data else []  # Assuming the first row is the header

    for i, row in enumerate(data[1:], start=2):  # Skip header row
        for j, cell in enumerate(row, start=1):
            if cell == "":  # Check for missing cell
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                header = headers[j-1] if j <= len(headers) else "Unknown Header"
                missing_info_log.append(f"Missing information at Row: {i}, Column: {j}, Column Header: '{header}', Timestamp: {timestamp}")

    return '\n'.join(missing_info_log) if missing_info_log else "No missing information found."

# Create an agent that uses the Google Sheet Scanner tool
agent = Agent(
    role='Data Auditor',
    goal='Identify missing information in Google Sheets',
    tools=[google_sheet_scanner],  # Use the decorated function as a tool
    verbose=True,
    backstory='A meticulous auditor dedicated to ensuring data completeness and accuracy.'
)

# Define a task for scanning a specific Google Sheet
scan_task = Task(
    description="Scan the provided Google Sheet for missing information.",
    tools=[google_sheet_scanner],  # Use the decorated function as a tool
    agent=agent,
    expected_output="""A list (or a structured report) indicating the locations (row, column and header) of missing information, along with a timestamp and the recommended the best agent to find the relevant information.
                Example Output: 
                Missing information at Row: 2, Column: 14, Column Header: 'Persons Twitter', Timestamp: 2024-04-10 18:04:46
                Missing information at Row: 2, Column: 15, Column Header: 'Persons LinkedIn Post 1', Timestamp: 2024-04-10 18:04:46
                Missing information at Row: 2, Column: 16, Column Header: 'Persons LinkedIn Post 2', Timestamp: 2024-04-10 18:04:46
                Missing information at Row: 3, Column: 7, Column Header: 'Departments', Timestamp: 2024-04-10 18:04:46"""
)

# Create a crew with the agent and assign the task
crew = Crew(
    agents=[agent],
    tasks=[scan_task],
    process=Process.sequential
)

# Kick off the crew with inputs (spreadsheet ID)
result = crew.kickoff(inputs={'spread_sheets_id': SPREAD_SHEET_ID})
print(result)
