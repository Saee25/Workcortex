import os
from dotenv import load_dotenv
from engine.email_client import GmailClient
from engine.processor import DataProcessor

def run():
    load_dotenv()
    client = GmailClient(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
    processor = DataProcessor()
    
    sender = input("Enter sender email: ")
    
    client.connect()
    ids = client.fetch_emails(sender)
    
    recs = [client.get_recipients(i) for i in ids]
    clean = processor.extract_clean_emails(recs)
    
    path = processor.save_to_excel(clean, "./output")
    print(f"Success! Saved to {path}")

if __name__ == "__main__":
    run()