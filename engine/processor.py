import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def extract_clean_emails(raw_recipient_list):
        if not raw_recipient_list:
            return []
        # Get unique emails, lowercase them, and remove empty ones
        distinct_emails = sorted(list(set([e.strip().lower() for e in raw_recipient_list if e])))
        return distinct_emails

    @staticmethod
    def save_to_excel(email_list, config_path):
        if not os.path.exists(config_path):
            os.makedirs(config_path)
            
        df = pd.DataFrame(email_list, columns=["Recipient Email"])
        file_path = os.path.join(config_path, "extracted_recipients.xlsx")
        df.to_excel(file_path, index=False)
        return file_path