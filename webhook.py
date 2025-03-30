# webhook.py
import os
from flask import Flask, request, jsonify
import requests
from google_sheets import log_search
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

app = Flask(_name_)

# Replace with your actual Apollo API key; here we use a sample key
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY", "sample_apollo_api_key_123456789")
APOLLO_ENDPOINT = "https://api.apollo.io/v1/people/match"

def search_person(query):
    """Search for a person using the Apollo API."""
    params = {'name': query}
    headers = {'Authorization': f'Bearer {APOLLO_API_KEY}'}
    response = requests.get(APOLLO_ENDPOINT, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    text = data.get("text")
    chat_id = data.get("chat_id")
    
    # Search for person details using Apollo API
    result = search_person(text)
    if result and "person" in result:
        person = result["person"]
        response_text = "🔍 Search Result:\n\n"
        response_text += f"👤 Name: {person.get('name', 'N/A')}\n"
        response_text += f"🏢 Company: {person.get('organization_name', 'N/A')}\n"
        response_text += f"📧 Email: {person.get('email', 'N/A')}\n"
        response_text += f"🔗 LinkedIn: {person.get('linkedin_url', 'N/A')}\n"
        
        # Log the search details into Google Sheets
        log_search(text, person)
    else:
        response_text = "⚠ No details found!"
    
    return jsonify({"response": response_text})

if _name_ == "_main_":
    app.run(port=5000, debug=True)