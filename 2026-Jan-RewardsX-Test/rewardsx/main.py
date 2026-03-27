# main.py

from ingestion.parser import parse_eml

email = parse_eml("data/emails/talveer-tims-test.eml")


from ai.interpreter import extract_rewards_info

print("\n=== Sending To AI ===")
ai_result = extract_rewards_info(email)

print("\n=== AI Extraction Result ===")
print(ai_result)