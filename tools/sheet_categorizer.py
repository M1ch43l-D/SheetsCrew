import os
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials


os.environ["OPENAI_API_KEY"] = "NULL"
os.environ["openai_api_base"] = "http://localhost:1234/v1"

# Setup OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(
    api_key=openai.api_key,
    base_url="http://localhost:1234/v1"
)

# Setup Google Sheets
spread_sheets_id = os.getenv('SPREAD_SHEETS_ID')
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(spread_sheets_id).sheet1
def classify_comment(comment):
    try:
        response = client.chat.completions.create(
            model="Mixtral",
            messages=[
                {"role": "system", "content": """
                    You are a helpful assistant designed to classify comments into: 
                    Neutral, Request, Question, Appreciation, Error or Other. 
                    Must respond with one word.
                    """
                },
                {"role": "user", "content": "This video was really helpful, thanks!"},
                {"role": "assistant", "content": "Appreciation"},
                {"role": "user", "content": "Can you explain how quantum computing works?"},
                {"role": "assistant", "content": "Question"},
                {"role": "user", "content": "Please create a video on how to use the new software."},
                {"role": "assistant", "content": "Request"},
                {"role": "user", "content": "There is an error in the code"},
                {"role": "assistant", "content": "Error"},
                {"role": "user", "content": "This video is okay, nothing special."},
                {"role": "assistant", "content": "Neutral"},
                {"role": "user", "content": comment}  # This is the comment you want to classify
            ]
        )
        category = response.choices[0].message.content.strip()
        print(f"Comment: '{comment}' -> Category: '{category}'")
        return category.title()
    except Exception as e:
        print(f"Error in classifying comment: {e}")
        return "Process Failed"

# Read data from the sheet
data = sheet.get_all_values()
header = data[0]  # Assuming the first row is the header
comments_rows = data[1:]  # Exclude header




# Iterate over each row that contains comments
for i, row in enumerate(comments_rows, start=3):  # Google Sheets is 1-indexed; header is row 1, so data starts at row 2
    comment = row[1]  # Assuming the comment is in the second column
    category = classify_comment(comment)
    # Update the 3th column (index 2) with the classification
    sheet.update_cell(i, 3, category)

print("The Google Sheet has been updated with categories for each comment.")