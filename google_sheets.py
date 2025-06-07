import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Load service account credentials from environment variable
SERVICE_ACCOUNT_INFO = os.getenv("GOOGLE_CREDS_JSON")

if not SERVICE_ACCOUNT_INFO:
    raise EnvironmentError("Missing GOOGLE_CREDS_JSON in environment variables.")

try:
    service_account_info = json.loads(SERVICE_ACCOUNT_INFO)
except json.JSONDecodeError:
    raise ValueError("GOOGLE_CREDS_JSON is not a valid JSON string.")

# Define correct scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(creds)

# Open spreadsheet
try:
    sheet = client.open("ExpensesBotData").sheet1
except Exception as e:
    raise RuntimeError("Failed to open the spreadsheet. Ensure access is granted.") from e

def add_expense(user: str, category: str, amount: float, date: str) -> bool:
    """
    Adds a new expense row to the Google Sheet.
    
    Args:
        user (str): The name or ID of the user.
        category (str): The category of the expense.
        amount (float): The amount spent.
        date (str): The date of the expense.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        sheet.append_row([user, category, amount, date])
        print(f"[INFO] Expense added: {user}, {category}, {amount}, {date}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to append row: {e}")
        return False

