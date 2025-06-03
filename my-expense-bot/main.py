from fastapi import FastAPI, Request
import google.generativeai as genai
from google_sheets import add_expense
import json

app = FastAPI()

# Configure Gemini
genai.configure(api_key="AIzaSyChNdopDIWP_iWdRu2xOb4t5gTBdLF8St8")
model = genai.GenerativeModel('gemini-1.5-flash')


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("=== RAW INCOMING DATA ===")
    print(data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        sender = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        print(f"Received from {sender}: {message}")
    except (KeyError, IndexError) as e:
        print("Failed to extract message or sender:", e)
        return {"error": "Invalid message format"}

    # Ask Gemini to extract amount, category, and note
    prompt = f"""
    Extract amount, category, and note from this expense message:

    Message: "{message}"

    Respond ONLY in JSON format like:
    {{
        "amount": 100,
        "category": "groceries",
        "note": "milk and bread"
    }}
    """

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        print("Gemini response:", result)

        # Extract JSON block safely
        import re, json
        match = re.search(r"\{.*?\}", result, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON object found in Gemini response.")
        
        parsed = json.loads(match.group())

        amount = int(parsed["amount"])
        category = parsed["category"]
        note = parsed["note"]

        add_expense(amount, category, note, sender)

        return {"message": "Expense recorded."}


    except Exception as e:
        print("Error during Gemini parsing or saving:", str(e))
        return {"message": "Failed to process expense. Please try again."}
