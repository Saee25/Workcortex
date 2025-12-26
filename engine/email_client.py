import imaplib
import email

class GmailClient:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.mail = None

    def connect(self):
        # Connect to Gmail IMAP
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.user, self.password)
        self.mail.select("inbox")

    def fetch_emails(self, sender_email):
        # Search for all emails from the specific sender
        status, messages = self.mail.search(None, f'FROM "{sender_email}"')
        if status != 'OK':
            return []
        return messages[0].split()

    def get_recipients(self, msg_id):
        # Extract the 'To' header from the email
        _, data = self.mail.fetch(msg_id, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        return msg.get("To")