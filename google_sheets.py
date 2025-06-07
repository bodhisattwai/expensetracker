import os
import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "service_account.json"  # Ensure this file exists in the same directory

# Define correct scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Validate file existence
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    raise FileNotFoundError(f"Service account file '{SERVICE_ACCOUNT_FILE}' not found.")

# Authenticate
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open spreadsheet
sheet = client.open("ExpensesBotData").sheet1

def add_expense(user: str, category: str, amount: float, date: str):
    sheet.append_row([user, category, amount, date])
