import os
import json
import utils
import requests
from dotenv import load_dotenv

# Load the .env file from current directory
load_dotenv()

# print(os.getenv("OPENROUTER_YOUTUBE_VIDEO_SUMMARISER"))

SUMMARISED_HISTORY_FILE = "summarise-history.json"
CHANNEL_ID = "UC5cEHfCr6WOE1R1zcohd1IA"  # Jose Najarro Stocks
MAX_RESULTS = 5  # Check last 5 videos to avoid missing uploads and avoid pulling too much information
YT_API = os.getenv("YOUTUBE_DATA_API_V3")


def get_latest_videos(CHANNEL_ID):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={YT_API}&channelId={CHANNEL_ID}"
        f"&part=snippet,id&order=date&maxResults={MAX_RESULTS}"
    )
    response = requests.get(url)
    data = response.json()

    videos = []
    for item in data.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            published_at = item["snippet"]["publishedAt"]
            title = item["snippet"]["title"]
            videos.append(
                {"video_id": video_id, "title": title, "published_at": published_at}
            )
    return videos


def main():
    # Get all existing video ids
    existing_data = utils.read_history_file(SUMMARISED_HISTORY_FILE)
    existing_ids = {video["video_id"] for video in existing_data}

    # Get new videos from channel, which isn't saved into the output file.
    latest_videos = get_latest_videos(CHANNEL_ID)
    new_videos = [v for v in latest_videos if v["video_id"] not in existing_ids]

    for video in new_videos:
        print("***********NEW VIDEO FOUND***********")
        print(f"video_id: {video["video_id"]}")
        print(f"channel_id: {CHANNEL_ID}")
        print(f"title: {video["title"]}")
        print(f"published_at: {video["published_at"]}")
        print(f"transcribed: {False}")
        print(f"transcription_dir: transcriptions/{CHANNEL_ID}/{video["video_id"]}")
        print(f"summarised: {False}")
        print(f"summarised_dir: transcriptions/{CHANNEL_ID}/{video["video_id"]}")
        print(f"posted_to_discord: {False}")

        video_entry = {
            "video_id": video["video_id"],
            "channel_id": CHANNEL_ID,
            "title": video["title"],
            "published_at": video["published_at"],
            "transcribed": False,
            "transcription_dir": f"transcriptions/{CHANNEL_ID}/{video["video_id"]}",
            "summarised": False,
            "summarised_dir": f"transcriptions/{CHANNEL_ID}/{video["video_id"]}",
            "posted_to_discord": False,
        }

        existing_data.append(video_entry)

        # Save to JSON file
        with open(SUMMARISED_HISTORY_FILE, "w") as f:
            json.dump(existing_data, f, indent=4)


if __name__ == "__main__":
    main()
