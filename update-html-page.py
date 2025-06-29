import os
import utils
from datetime import datetime

# Base directory to scan
BASE_DIR = "transcriptions/UC5cEHfCr6WOE1R1zcohd1IA"
SUMMARISED_HISTORY_FILE = "summarise-history.json"

# Main HTML file path
MAIN_HTML_PATH = "website/index.html"

# Placeholder comment in the HTML file where summaries will be inserted
PLACEHOLDER_START = "<!-- START_SUMMARIES -->"
PLACEHOLDER_END = "<!-- END_SUMMARIES -->"

# Template for one summary div, with placeholders to fill
DIV_TEMPLATE = """
<div
  class="summary"
  data-summary-path="{summary_path}"
  data-tags-path="{tags_path}"
>
  <div class="summary-header">
    <h2>{title}</h2>
    <p class="date-added">Added: <span>{date_added}</span></p>
  </div>

  <div class="tags-row"></div>

  <br /><br />

  <button class="toggle-btn">View Summary</button>
  <div class="summary-details"></div>

  <button
    class="youtube-btn"
    onclick="window.open('{youtube_link}', '_blank')"
  >
    Watch YouTube Video
  </button>
</div>
"""


def get_unique_ids(base_dir):
    """Return sorted list of unique subfolders in base_dir."""
    return sorted(
        [
            name
            for name in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, name))
        ]
    )


def get_video_name_by_id(history_data, video_id):
    for video in history_data:
        if video.get("video_id") == video_id:
            return video.get("title")
            break  # assuming video IDs are unique


def build_div_for_id(base_dir, unique_id):
    """Construct div HTML for given unique_id."""
    summary_path = os.path.join(
        base_dir, unique_id, f"summary_{unique_id}.txt"
    ).replace("\\", "/")
    tags_path = os.path.join(base_dir, unique_id, f"tags_{unique_id}.txt").replace(
        "\\", "/"
    )

    # For demonstration, you can set the title to the unique_id or customize
    history_file_data = utils.read_history_file(SUMMARISED_HISTORY_FILE)

    title = f"{get_video_name_by_id(history_file_data, unique_id)}"

    # For date added, use current date or fetch file modification date
    try:
        mod_time = os.path.getmtime(summary_path)
        date_added = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
    except Exception:
        date_added = "Unknown"

    # Example: construct youtube link based on unique_id or a mapping you maintain
    # For now, just a placeholder or the unique_id as the video id:
    youtube_link = f"https://www.youtube.com/watch?v={unique_id}"

    return DIV_TEMPLATE.format(
        summary_path=summary_path,
        tags_path=tags_path,
        title=title,
        date_added=date_added,
        youtube_link=youtube_link,
    )


def read_main_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_main_html(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def update_html_with_summaries(html_path, base_dir):
    html_content = read_main_html(html_path)

    # Find placeholder positions
    start_idx = html_content.find(PLACEHOLDER_START)
    end_idx = html_content.find(PLACEHOLDER_END)

    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        print(f"Placeholder comments not found or invalid in {html_path}")
        return

    start_idx += len(PLACEHOLDER_START)  # Position after the start comment

    unique_ids = get_unique_ids(base_dir)
    divs_html = "\n".join(build_div_for_id(base_dir, uid) for uid in unique_ids)

    # Build new HTML with divs injected
    new_html = (
        html_content[:start_idx] + "\n" + divs_html + "\n" + html_content[end_idx:]
    )

    write_main_html(html_path, new_html)
    print(f"Updated {html_path} with {len(unique_ids)} summaries.")


if __name__ == "__main__":
    update_html_with_summaries(MAIN_HTML_PATH, BASE_DIR)
