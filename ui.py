import streamlit as st
import pandas as pd
import time
import os
from dotenv import load_dotenv
from engine.email_client import GmailClient
from engine.logger import LiveLogger
from engine.processor import DataProcessor

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="WorkCortex Email Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
    }
    
    /* Hide default Streamlit header/navbar */
    header[data-testid="stHeader"] {
        background: transparent !important;
        display: none !important;
    }
    
    /* Hide hamburger menu */
    #MainMenu {
        visibility: hidden;
    }
    
    /* Hide footer */
    footer {
        visibility: hidden;
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Custom Header Bar */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 70px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.95) 0%, rgba(139, 92, 246, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        z-index: 999;
        display: flex;
        align-items: center;
        padding: 0 2rem;
        animation: slideDown 0.5s ease-out;
    }
    
    @keyframes slideDown {
        from {
            transform: translateY(-100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .header-title {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .header-title h1 {
        color: white !important;
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: white !important;
        font-size: 1.75rem !important;
        margin: 0 !important;
        font-weight: 700;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .running-man {
        font-size: 2rem;
        animation: run 2s infinite ease-in-out;
        display: inline-block;
        filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
    }
    
    @keyframes run {
        0%, 100% {
            transform: translateX(0) rotate(0deg);
        }
        25% {
            transform: translateX(10px) rotate(5deg);
        }
        75% {
            transform: translateX(-10px) rotate(-5deg);
        }
    }
    
    .status-badge {
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        50% {
            box-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
        }
    }
    
    /* Add padding to main content to account for fixed header */
    .main .block-container {
        padding-top: 90px !important;
    }
    
    /* Header styling for content area */
    h1 {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem !important;
        margin-bottom: 2rem !important;
        letter-spacing: -0.02em;
    }
    
    h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
        z-index: 998 !important;
        padding-top: 70px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.875rem !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* Primary button (START) */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
    }
    
    /* Secondary buttons */
    .stButton button[kind="secondary"] {
        background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
        color: white !important;
    }
    
    /* Disabled buttons */
    .stButton button:disabled {
        opacity: 0.4 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }
    
    /* Table styling */
    .dataframe {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }
    
    .dataframe tbody tr td {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: var(--text-primary) !important;
        padding: 0.875rem !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.1) !important;
    }
    
    .dataframe tbody tr:hover td {
        background-color: rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Status badges */
    .status-success {
        color: var(--success-color);
        font-weight: 600;
    }
    
    .status-failed {
        color: var(--error-color);
        font-weight: 600;
    }
    
    .status-started {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px !important;
        border-left: 4px solid !important;
    }
    
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border-left-color: var(--success-color) !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border-left-color: var(--warning-color) !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border-left-color: var(--error-color) !important;
    }
    
    .stInfo {
        background-color: rgba(99, 102, 241, 0.1) !important;
        border-left-color: var(--primary-color) !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(99, 102, 241, 0.2) !important;
        margin: 2rem 0 !important;
    }
    
    /* Card-like containers */
    .element-container {
        transition: all 0.3s ease;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.75rem !important;
        }
        
        .stButton button {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Custom Header Bar
def get_status_text():
    if st.session_state.get("is_running", False):
        if st.session_state.get("is_paused", False):
            return "⏸️ PAUSED"
        else:
            return "🟢 RUNNING"
    elif st.session_state.get("abort_requested", False):
        return "⚠️ ABORTED"
    else:
        return "⚪ IDLE"

st.markdown(f"""
<div class="custom-header">
    <div class="header-content">
        <div class="header-title">
            <h1>WorkCortex Email Agent</h1>
        </div>
        <div class="status-badge">{get_status_text()}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Title (hidden but kept for structure)
st.markdown('<div style="display: none;">', unsafe_allow_html=True)
st.title("Email Extraction Agent")
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state variables
if "logger" not in st.session_state:
    st.session_state.logger = LiveLogger()
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "is_paused" not in st.session_state:
    st.session_state.is_paused = False
if "abort_requested" not in st.session_state:
    st.session_state.abort_requested = False

# Callback functions for buttons
def start_execution():
    st.session_state.is_running = True
    st.session_state.is_paused = False
    st.session_state.abort_requested = False
    st.session_state.logger = LiveLogger()

def pause_execution():
    st.session_state.is_paused = True

def resume_execution():
    st.session_state.is_paused = False

def abort_execution():
    st.session_state.abort_requested = True
    st.session_state.is_running = False

# Sidebar Configuration
st.sidebar.header("Settings")
sender_input = st.sidebar.text_input(
    "Sender Email to Filter",
    "",
    placeholder="Sender's Email",
    help="Enter the email address to filter messages from"
)
save_path = st.sidebar.text_input(
    "Output Path",
    "./output",
    help="Directory where the Excel file will be saved"
)

st.sidebar.markdown("---")
st.sidebar.header("Execution Controls")

# Control buttons with callbacks
col1, col2 = st.sidebar.columns(2)
with col1:
    start_btn = st.button(
        "START",
        disabled=st.session_state.is_running,
        use_container_width=True,
        type="primary",
        on_click=start_execution,
        key="start_button"
    )
    pause_btn = st.button(
        "PAUSE",
        disabled=not st.session_state.is_running or st.session_state.is_paused,
        use_container_width=True,
        on_click=pause_execution,
        key="pause_button"
    )
with col2:
    resume_btn = st.button(
        "RESUME",
        disabled=not st.session_state.is_paused,
        use_container_width=True,
        on_click=resume_execution,
        key="resume_button"
    )
    abort_btn = st.button(
        "ABORT",
        disabled=not st.session_state.is_running,
        use_container_width=True,
        on_click=abort_execution,
        key="abort_button"
    )

# Status indicators in sidebar
st.sidebar.markdown("---")
if st.session_state.is_running:
    if st.session_state.is_paused:
        st.sidebar.info("Status: PAUSED")
    else:
        st.sidebar.success("Status: RUNNING")
elif st.session_state.abort_requested:
    st.sidebar.warning("Status: ABORTED")
else:
    st.sidebar.info("Status: IDLE")

# Placeholder for the live table
log_table_placeholder = st.empty()

# Helper function to check pause/abort
def check_pause_abort(logger, log_table_placeholder):
    while st.session_state.is_paused and not st.session_state.abort_requested:
        time.sleep(0.5)
    if st.session_state.abort_requested:
        logger.log(99, "Execution Aborted by User", "User Action", "FAILED")
        log_table_placeholder.table(logger.get_df())
        return True
    return False

if start_btn or st.session_state.is_running:
    if start_btn:
        logger = st.session_state.logger
        processor = DataProcessor()
        
        try:
            # STEP 1: Connect
            logger.log(1, "Initializing Gmail Connection", "imaplib", "STARTED")
            log_table_placeholder.table(logger.get_df())
            if check_pause_abort(logger, log_table_placeholder):
                st.session_state.is_running = False
                st.stop()
            
            client = GmailClient(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
            
            # Retry mechanism for connection
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    client.connect()
                    break
                except Exception as conn_err:
                    if attempt < max_retries - 1:
                        logger.log(1, f"Connection attempt {attempt + 1} failed, retrying...", "IMAP SSL", "RETRIED")
                        log_table_placeholder.table(logger.get_df())
                        time.sleep(2)
                    else:
                        raise conn_err
            
            logger.log(1, "Connected to Gmail", "IMAP SSL", "SUCCESS")
            log_table_placeholder.table(logger.get_df())
            if check_pause_abort(logger, log_table_placeholder):
                st.session_state.is_running = False
                st.stop()

            # STEP 2: Fetch
            logger.log(2, f"Fetching emails from {sender_input}", "Gmail Search", "STARTED")
            log_table_placeholder.table(logger.get_df())
            if check_pause_abort(logger, log_table_placeholder):
                st.session_state.is_running = False
                st.stop()
            
            email_ids = client.fetch_emails(sender_input)
            
            logger.log(2, f"Found {len(email_ids)} emails", "IMAP", "SUCCESS")
            log_table_placeholder.table(logger.get_df())
            if check_pause_abort(logger, log_table_placeholder):
                st.session_state.is_running = False
                st.stop()

            # STEP 3: Extract
            logger.log(3, "Extracting distinct recipients", "Email Parser", "STARTED")
            log_table_placeholder.table(logger.get_df())
            if check_pause_abort(logger, log_table_placeholder):
                st.session_state.is_running = False
                st.stop()
            
            raw_recipients = []
            for idx, m_id in enumerate(email_ids):
                if check_pause_abort(logger, log_table_placeholder):
                    st.session_state.is_running = False
                    st.stop()
                raw_recipients.append(client.get_recipients(m_id))
                if (idx + 1) % 10 == 0:  # Log progress every 10 emails
                    logger.log(3, f"Processing email {idx + 1}/{len(email_ids)}", "Email Parser", "STARTED")
                    log_table_placeholder.table(logger.get_df())
            
            clean_emails = processor.extract_clean_emails(raw_recipients)
            
            logger.log(3, f"Extracted {len(clean_emails)} unique IDs", "Logic", "SUCCESS")
            log_table_placeholder.table(logger.get_df())
            if check_pause_abort(logger, log_table_placeholder):
                st.session_state.is_running = False
                st.stop()

            # STEP 4: Save
            logger.log(4, "Saving to Excel", "Pandas", "STARTED")
            log_table_placeholder.table(logger.get_df())
            if check_pause_abort(logger, log_table_placeholder):
                st.session_state.is_running = False
                st.stop()
            
            final_path = processor.save_to_excel(clean_emails, save_path)
            
            logger.log(4, f"Saved to {final_path}", "File System", "SUCCESS")
            log_table_placeholder.table(logger.get_df())
            st.success("Task Completed Successfully!")
            
            st.session_state.is_running = False

        except Exception as e:
            logger.log(5, f"Error: {str(e)}", "System", "FAILED")
            log_table_placeholder.table(logger.get_df())
            st.error(f"Execution failed: {e}")
            st.session_state.is_running = False

# Display current logs if they exist
if st.session_state.logger.logs:
    st.subheader("Live Execution Logs")
    log_table_placeholder.table(st.session_state.logger.get_df())
else:
    # Show welcome message when no logs
    st.info("Configure settings in the sidebar and click START to begin email extraction.")