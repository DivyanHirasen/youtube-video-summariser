import os
import json
import utils
import codecs
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file from current directory
load_dotenv()

SUMMARISED_HISTORY_FILE = "summarise-history.json"
TRANSCRIPTION_DIR = "transcriptions"
OPENROUTER_YOUTUBE_VIDEO_SUMMARISER = os.getenv("OPENROUTER_YOUTUBE_VIDEO_SUMMARISER")
# MODEL_NAME = "mistralai/mistral-small-3.2-24b-instruct:free" # Pretty good
# MODEL_NAME = "minimax/minimax-m1:extended" # Kinda slow
MODEL_NAME = "meta-llama/llama-3.2-1b-instruct:free"  # Kinda slow
PROMPT_FILE_PATH = "prompts/prompt_1.txt"
TAGS_PROMPT_FILE_PATH = "prompts/prompt_ticker_tag.txt"


def submit_prompt(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_YOUTUBE_VIDEO_SUMMARISER,
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return completion.choices[0].message.content


def strip_intro(summary_text):
    lines = summary_text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---":
            return "\n".join(lines[i + 1 :])  # Return everything after the first '---'
    return summary_text  # Return original if no '---' found


def clean_and_save_summary(raw_text: str, output_file: str):
    try:
        # Step 1: Decode unicode-escaped sequences
        decoded = raw_text.encode("utf-8").decode("unicode_escape")

        # Step 2: Fix emojis and accented characters
        clean_text = codecs.decode(decoded.encode("latin1"), "utf-8")

        clean_text = strip_intro(clean_text)

        # Step 3: Save it to a readable UTF-8 file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(clean_text)

        print(f"✅ Summary saved to: {output_file}")
    except Exception as e:
        print(f"❌ Error cleaning text: {e}")


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


def update_tags(history_data, video_id, tags):
    for video in history_data:
        if video.get("video_id") == video_id:
            video["ticker_tags"] = tags


def main():
    history_file_data = utils.read_history_file(SUMMARISED_HISTORY_FILE)

    unsummarised_videos = [
        video for video in history_file_data if not video.get("summarised", False)
    ]

    print(f"Found {len(unsummarised_videos)} which need to be summarised and saved.")

    for video in unsummarised_videos:
        print(f"Summarising: {video["video_id"]}")
        data_file_path = f"{video["transcription_dir"]}/raw_{video["video_id"]}.txt"
        full_prompt = create_prompt(PROMPT_FILE_PATH, data_file_path)

        prompt_response = submit_prompt(full_prompt)

        output_summary_file_path = (
            f"{video["summarised_dir"]}/summary_{video["video_id"]}.txt"
        )

        # Save summary
        clean_and_save_summary(prompt_response, output_summary_file_path)

        # Get Tags
        build_tags_prompt = create_prompt(
            TAGS_PROMPT_FILE_PATH, output_summary_file_path
        )
        tags_prompt_response = submit_prompt(build_tags_prompt)
        tags_list = [tag.strip() for tag in tags_prompt_response.split(",")]

        # Update tags and summary status to true
        update_tags(history_file_data, video["video_id"], tags_list)
        update_summary_status(history_file_data, video["video_id"])

    with open(SUMMARISED_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_file_data, f, indent=4)

    print("Summary job complete")


if __name__ == "__main__":
    main()
