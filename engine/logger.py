import pandas as pd
from datetime import datetime

class LiveLogger:
    def __init__(self):
        self.logs = []

    def log(self, order, description, tool, status):
        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Order": order,
            "Step Description": description,
            "Tool/App/URL/EXE": tool,
            "Status": status
        }
        self.logs.append(log_entry)
        return log_entry

    def get_df(self):
        return pd.DataFrame(self.logs)  