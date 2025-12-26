import streamlit as st
import pandas as pd
import time
import os
from dotenv import load_dotenv
from engine.email_client import GmailClient
from engine.logger import LiveLogger
from engine.processor import DataProcessor

load_dotenv()

st.set_page_config(page_title="WorkCortex Email Agent", layout="wide")
st.title("📧 Email Extraction Agent")

# Sidebar Configuration
st.sidebar.header("Settings")
sender_input = st.sidebar.text_input("Sender Email to Filter", "noreply@theoneclickdesigner.com")
save_path = st.sidebar.text_input("Configurable Output Path", "./output")
start_btn = st.sidebar.button("START EXECUTION")

# Initialize Logger in session state so it persists
if "logger" not in st.session_state:
    st.session_state.logger = LiveLogger()

# Placeholder for the live table
log_table_placeholder = st.empty()

if start_btn:
    logger = st.session_state.logger
    processor = DataProcessor()
    
    try:
        # STEP 1: Connect
        logger.log(1, "Initializing Gmail Connection", "imaplib", "STARTED")
        log_table_placeholder.table(logger.get_df())
        
        client = GmailClient(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
        client.connect()
        
        logger.log(1, "Connected to Gmail", "IMAP SSL", "SUCCESS")
        log_table_placeholder.table(logger.get_df())

        # STEP 2: Fetch
        logger.log(2, f"Fetching emails from {sender_input}", "Gmail Search", "STARTED")
        log_table_placeholder.table(logger.get_df())
        
        email_ids = client.fetch_emails(sender_input)
        
        logger.log(2, f"Found {len(email_ids)} emails", "IMAP", "SUCCESS")
        log_table_placeholder.table(logger.get_df())

        # STEP 3: Extract
        logger.log(3, "Extracting distinct recipients", "Email Parser", "STARTED")
        log_table_placeholder.table(logger.get_df())
        
        raw_recipients = []
        for m_id in email_ids:
            raw_recipients.append(client.get_recipients(m_id))
        
        clean_emails = processor.extract_clean_emails(raw_recipients)
        
        logger.log(3, f"Extracted {len(clean_emails)} unique IDs", "Logic", "SUCCESS")
        log_table_placeholder.table(logger.get_df())

        # STEP 4: Save
        logger.log(4, "Saving to Excel", "Pandas", "STARTED")
        log_table_placeholder.table(logger.get_df())
        
        final_path = processor.save_to_excel(clean_emails, save_path)
        
        logger.log(4, f"Saved to {final_path}", "File System", "SUCCESS")
        log_table_placeholder.table(logger.get_df())
        st.success("Task Completed Successfully!")

    except Exception as e:
        logger.log(5, f"Error: {str(e)}", "System", "FAILED")
        log_table_placeholder.table(logger.get_df())
        st.error(f"Execution failed: {e}")