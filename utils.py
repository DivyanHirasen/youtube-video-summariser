import os
import json

def read_history_file(SUMMARISED_HISTORY_FILE):
    if os.path.exists(SUMMARISED_HISTORY_FILE):
        with open(SUMMARISED_HISTORY_FILE, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    return existing_data