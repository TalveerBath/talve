from flask import Flask, request
from ingestion.parser import parse_mime_string
from ingestion.parser import parse_eml
from ai.interpreter import extract_rewards_info

app = Flask(__name__)

@app.post("/")
def ingest():
    mime = request.form.get("body-mime", "")
    parsed = parse_mime_string(mime)
    print("\n=== Parsed Email From Mailgun ===")
    print(parsed)
    return "OK", 200

# LOCAL TESTING ONLY

if __name__ == "__main__":
    # This block ONLY runs when run: python main.py
    email = parse_eml("data/emails/talveer-tims-test.eml")

    print("\n=== Sending To AI ===")
    ai_result = extract_rewards_info(email)

    print("\n=== AI Extraction Result ===")
    print(ai_result)
