import os
import json
import utils
from youtube_transcript_api import YouTubeTranscriptApi

SUMMARISED_HISTORY_FILE = "summarise-history.json"
TRANSCRIPTION_DIR = "transcriptions"

def transcribe_and_save_video(video_id, transcription_dir):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([entry['text'] for entry in transcript])

    # Create output directory if it doesn't exist
    os.makedirs(transcription_dir, exist_ok=True)

    # Save transcription to text file
    output_filename = f"raw_{video_id}.txt"
    output_path = os.path.join(transcription_dir, output_filename)
    with open(output_path, "w") as f:
        f.write(text)

    print(f"Successfully transcribed {video_id}")

def update_transcribed_status(history_data, video_id, value=True):
    for video in history_data:
        if video.get("video_id") == video_id:
            video["transcribed"] = value
            break  # assuming video IDs are unique


def main():
    history_file_data = utils.read_history_file(SUMMARISED_HISTORY_FILE)

    untranscribed_videos = [video for video in history_file_data if not video.get("transcribed", False)]

    print(f"Found {len(untranscribed_videos)} which need to be transcribed and saved.")

    for video in untranscribed_videos:
        transcribe_and_save_video(video["video_id"], video["transcription_dir"])
        update_transcribed_status(history_file_data, video["video_id"])

    # Update history file
    # Now save the updated data back to the JSON file
    with open(SUMMARISED_HISTORY_FILE, "w") as f:
        json.dump(history_file_data, f, indent=4)

    print("Transcription job complete")
    

if __name__ == "__main__":
    main()