import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"  # change to "llama3" if needed


def extract_rewards_info(email_data: dict) -> dict:
    """
    Extract:
    - rewards program name
    - points earned
    - customer email
    - awarded date
    - expiry date
    """

    prompt = f"""
You are a strict information extraction engine.

Extract rewards information from the email below.

Return ONLY valid JSON.
Do NOT explain.
Do NOT add commentary.
Do NOT describe anything.
Do NOT wrap in markdown.
If a value does not exist, return null.

Format EXACTLY like this:

{{
  "program": string or null,
  "points": number or null,
  "email": string or null,
  "awarded_date": string or null,
  "expiry_date": string or null
}}

Email:
Subject: {email_data.get('subject')}
Sender: {email_data.get('sender')}
Body: {email_data.get('body')}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0
            },
            timeout=160
        )

        data = response.json()
        ai_text = data.get("response")

        if not ai_text:
            return {
                "error": "No 'response' field returned from Ollama",
                "raw": data
            }

        ai_text = ai_text.strip()

        # Remove markdown formatting if model adds ```json
        if ai_text.startswith("```"):
            ai_text = re.sub(r"```json|```", "", ai_text).strip()

        # Try normal JSON parsing
        try:
            structured = json.loads(ai_text)
            return structured
        except json.JSONDecodeError:
            # Attempt to extract JSON substring
            match = re.search(r"\{.*\}", ai_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass

            return {
                "error": "AI did not return valid JSON",
                "raw_ai_output": ai_text
            }

    except Exception as e:
        return {
            "error": "Request to Ollama failed",
            "details": str(e)
        }