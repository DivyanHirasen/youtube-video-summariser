import os
import json

SUMMARISED_HISTORY_FILE = "summarise-history.json"

def read_history_file():
    if os.path.exists(SUMMARISED_HISTORY_FILE):
        with open(SUMMARISED_HISTORY_FILE, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    return existing_data


def main():
    print("asd")

if __name__ == "__main__":
    main()