# 📧 WorkCortex Email Extraction System

A Python-based email extraction system that fetches emails from Gmail, extracts distinct recipient addresses, and saves them to Excel with live execution logging.

## 🎯 Features

- Gmail IMAP integration with secure authentication
- Filter emails by sender address
- Extract and deduplicate recipient email addresses
- Export to Excel at configurable location
- Live execution logs with UI controls (Start/Pause/Resume/Abort)
- Automatic retry mechanism for failed connections
- Real-time status updates: STARTED, SUCCESS, FAILED, RETRIED

## 📁 Project Structure

```
Workcortex/
├── engine/
│   ├── email_client.py      # Gmail IMAP client
│   ├── logger.py            # Live logging system
│   └── processor.py         # Data processing & Excel export
├── output/                  # Excel output directory
├── .env.example             # Credentials template
├── main.py                  # CLI interface
├── ui.py                    # Streamlit UI
└── requirements.txt         # Dependencies
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone <your-repo-url>
cd Workcortex

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file in project root:

```env
GMAIL_USER=your-email@gmail.com
GMAIL_PASS=your-app-password
```

> **Note**: Use Gmail App Password (requires 2FA). [Create App Password](https://support.google.com/accounts/answer/185833)

### 3. Run Application

**UI Mode (Recommended):**
```bash
streamlit run ui.py
```

**CLI Mode:**
```bash
python main.py
```

## 🎮 UI Controls

- **▶️ START** - Begin email extraction
- **⏸️ PAUSE** - Pause execution
- **▶️ RESUME** - Resume paused execution
- **⏹️ ABORT** - Stop execution immediately

## 📊 Live Execution Logs

| Timestamp | Order | Step Description | Tool/App/URL/EXE | Status |
|-----------|-------|------------------|------------------|--------|
| 2025-12-26 22:30:15 | 1 | Initializing Gmail Connection | imaplib | STARTED |
| 2025-12-26 22:30:17 | 1 | Connected to Gmail | IMAP SSL | SUCCESS |
| 2025-12-26 22:30:20 | 2 | Found 45 emails | IMAP | SUCCESS |
| 2025-12-26 22:30:25 | 3 | Extracted 127 unique IDs | Logic | SUCCESS |
| 2025-12-26 22:30:27 | 4 | Saved to ./output/extracted_recipients.xlsx | File System | SUCCESS |

## 📝 Sample Output

Excel file with deduplicated, sorted recipient emails:

| Recipient Email |
|----------------|
| user1@example.com |
| user2@example.com |
| user3@example.com |

## 🏗️ Architecture & Design Decisions

### Technology Stack
- **IMAP (imaplib)**: Direct Gmail access, no API quotas
- **Streamlit**: Rapid UI development with built-in state management
- **Pandas + openpyxl**: Industry-standard data manipulation and Excel export
- **python-dotenv**: Secure credential management

### Modular Design
- `email_client.py`: Gmail IMAP operations (connect, fetch, extract)
- `logger.py`: Live logging with required columns
- `processor.py`: Email deduplication and Excel export
- `ui.py`: Streamlit UI with execution controls
- `main.py`: CLI interface

### Key Features
- **Retry Mechanism**: Auto-retry (3 attempts) for connection failures
- **Pause/Resume**: Session state-based execution control
- **Live Logging**: Real-time table updates via Streamlit placeholders
- **Security**: Environment variables, no hard-coded credentials

## 🔍 Assumptions

1. Gmail account with IMAP enabled and App Password configured
2. Standard email "To" headers present
3. Stable internet connection for IMAP operations
4. Python 3.8+ with pip installed
5. Write permissions for output directory
6. Modern browser for Streamlit UI
7. Single-user local execution
8. Reasonable email volume (tested up to 1000 emails)

## 🛠️ Troubleshooting

**Authentication failed**
- Verify App Password in `.env` file
- Ensure 2FA is enabled on Gmail

**No emails found**
- Check sender email address is correct
- Verify emails exist from that sender

**Permission denied saving Excel**
- Check output directory write permissions
- Close Excel file if currently open

**Streamlit UI not loading**
- Check port 8501 is available
- Try: `streamlit run ui.py --server.port 8502`

## � Dependencies

```
streamlit       # Web UI framework
pandas          # Data manipulation
openpyxl        # Excel file support
python-dotenv   # Environment variables
```

## 🎥 Demo

[Video demonstration will be added here]

## 📸 Screenshots

[Screenshots will be added here]

---

**Built for WorkCortex Intelligence Pvt Ltd**
