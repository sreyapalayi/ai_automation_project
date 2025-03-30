# google_sheets.py
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope for Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Path to your Google Sheets credentials JSON file
creds_file = "google_sheets_creds.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
client = gspread.authorize(credentials)

# Open your Google Sheet by name (ensure the sheet exists)
sheet = client.open("Apollo Searches").sheet1

def log_search(prompt, person):
    """
    Logs search details into the Google Sheet.
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = person.get("name", "N/A")
    company = person.get("organization_name", "N/A")
    email = person.get("email", "N/A")
    linkedin = person.get("linkedin_url", "N/A")
    row = [timestamp, prompt, name, company, email, linkedin]
    sheet.append_row(row)