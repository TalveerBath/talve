from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import quopri
import re

EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'


def extract_email(text: str) -> str:
    if not text:
        return ""
    match = re.search(EMAIL_REGEX, text)
    return match.group(0) if match else ""


def extract_body_from_mime(msg):
    """Extracts HTML or plain text body from a real-world email."""
    if msg.is_multipart():
        html_body = None
        text_body = None

        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition"))

            if "attachment" in disp:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            charset = part.get_content_charset() or "utf-8"
            decoded = payload.decode(charset, errors="ignore")

            if ctype == "text/html":
                html_body = decoded

            if ctype == "text/plain":
                text_body = decoded

        return html_body or text_body or ""
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")
        return msg.get_payload()

def clean_html(html: str) -> str:
    """Convert HTML to clean text."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Only decode quoted-printable if it looks encoded
    if "=" in text:
        try:
            decoded = quopri.decodestring(text).decode("utf-8", errors="ignore")
            text = decoded
        except Exception:
            pass

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_eml(path: str) -> dict:
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    raw_subject = msg.get("subject", "")
    raw_from = msg.get("from", "")
    raw_reply_to = msg.get("reply-to", "")

    sender = extract_email(raw_from) or extract_email(raw_reply_to)

    raw_body = extract_body_from_mime(msg)
    cleaned_body = clean_html(raw_body)

    return {
        "subject": raw_subject.strip(),
        "sender": sender.strip(),
        "body": cleaned_body
    }