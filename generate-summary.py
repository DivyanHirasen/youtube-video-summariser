import os
import utils
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file from current directory
load_dotenv()

SUMMARISED_HISTORY_FILE = "summarise-history.json"
TRANSCRIPTION_DIR = "transcriptions"
OPENROUTER_YOUTUBE_VIDEO_SUMMARISER = os.getenv("OPENROUTER_YOUTUBE_VIDEO_SUMMARISER")
MODEL_NAME = "mistralai/mistral-small-3.2-24b-instruct:free"

def create_and_submit_prompt():
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_YOUTUBE_VIDEO_SUMMARISER,
    )

    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    model=MODEL_NAME,
    messages=[
        {
        "role": "user",
        "content": "What is the meaning of life?"
        }
    ]
    )

    return completion.choices[0].message.content

def create_prompt(prompt_file_path, data_file_path):
    with open(prompt_file_path, "r") as f:
        prompt_template = f.read()

    with open(data_file_path, "r") as f:
        data_text = f.read()

    # Combine the two — append the data to the prompt
    final_prompt = f"{prompt_template.strip()}\n\n{data_text.strip()}"
    return final_prompt

def main():
    history_file_data = utils.read_history_file(SUMMARISED_HISTORY_FILE)

    unsummarised_videos = [video for video in history_file_data if not video.get("summarised", False)]

    print(f"Found {len(unsummarised_videos)} which need to be summarised and saved.")

    for video in unsummarised_videos:
        raw_trancription_dir = 

    #summary = create_and_submit_prompt()

    print(summary)




if __name__ == "__main__":
    main()