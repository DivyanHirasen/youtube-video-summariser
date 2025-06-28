import os
import json
import utils
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file from current directory
load_dotenv()

SUMMARISED_HISTORY_FILE = "summarise-history.json"
TRANSCRIPTION_DIR = "transcriptions"
OPENROUTER_YOUTUBE_VIDEO_SUMMARISER = os.getenv("OPENROUTER_YOUTUBE_VIDEO_SUMMARISER")
MODEL_NAME = "mistralai/mistral-small-3.2-24b-instruct:free"
PROMPT_FILE_PATH = "prompts/prompt_1.txt"

def create_and_submit_prompt(prompt):
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
        "content": prompt
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

def update_summary_status(history_data, video_id, value=True):
    for video in history_data:
        if video.get("video_id") == video_id:
            video["summarised"] = value
            break  # assuming video IDs are unique


def main():
    history_file_data = utils.read_history_file(SUMMARISED_HISTORY_FILE)

    unsummarised_videos = [video for video in history_file_data if not video.get("summarised", False)]

    print(f"Found {len(unsummarised_videos)} which need to be summarised and saved.")

    for video in unsummarised_videos:
        print(f"Summarising: {video["video_id"]}")
        data_file_path = f"{video["transcription_dir"]}/raw_{video["video_id"]}.txt"
        full_prompt = create_prompt(PROMPT_FILE_PATH, data_file_path)

        prompt_response = create_and_submit_prompt(full_prompt)

        output_summary_file_path = f"{video["summarised_dir"]}/summary_{video["video_id"]}.txt"

        with open(output_summary_file_path, "w") as f:
            json.dump(prompt_response, f, indent=4)

        update_summary_status(history_file_data, video["video_id"])

    with open(SUMMARISED_HISTORY_FILE, "w") as f:
        json.dump(history_file_data, f, indent=4)

    print("Summary job complete")


if __name__ == "__main__":
    main()