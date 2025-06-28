# YouTube Video Summarizer

An automated system that monitors YouTube channels for new videos, extracts transcriptions, generates AI-powered summaries with stock ticker tags, and deploys them to a web interface. This project is specifically designed for financial/stock market content analysis.

## 🎯 Project Overview

This system automatically processes YouTube videos from financial channels (currently configured for Jose Najarro Stocks) and creates comprehensive summaries with the following features:

- **Automated Video Detection**: Monitors YouTube channels for new uploads
- **Transcription Extraction**: Pulls full video transcripts using YouTube's API
- **AI-Powered Summaries**: Generates structured summaries using OpenRouter AI models
- **Stock Ticker Tagging**: Automatically identifies and tags mentioned stock symbols
- **Web Interface**: Deploys summaries to a clean, responsive web page
- **Discord Integration**: Ready for Discord bot integration (framework in place)

## 🏗️ Architecture

```
YouTube Channel → Video Detection → Transcription → AI Summary → Web Deployment
     ↓                ↓                ↓              ↓              ↓
get-latest-video-uploads.py → extract-transcription.py → generate-summary.py → surge-up.sh
```

### Core Components

1. **`get-latest-video-uploads.py`** - YouTube API integration to detect new videos
2. **`extract-transcription.py`** - Transcribes videos using YouTube Transcript API
3. **`generate-summary.py`** - AI-powered summary generation with OpenRouter
4. **`surge-up.sh`** - Deploys the web interface to Surge.sh
5. **`index.html`** - Web interface displaying summaries
6. **`utils.py`** - Shared utility functions
7. **`discord_util.py`** - Discord integration framework (placeholder)

## 📁 Project Structure

```
youtube-video-summariser/
├── get-latest-video-uploads.py    # Step 1: Detect new videos
├── extract-transcription.py        # Step 2: Extract transcriptions
├── generate-summary.py            # Step 3: Generate AI summaries
├── surge-up.sh                    # Step 4: Deploy to web
├── index.html                     # Web interface
├── utils.py                       # Shared utilities
├── discord_util.py                # Discord integration
├── summarise-history.json         # Video processing history
├── prompts/
│   ├── prompt_1.txt              # Main summary prompt
│   └── prompt_ticker_tag.txt     # Stock ticker extraction prompt
├── transcriptions/
│   └── UC5cEHfCr6WOE1R1zcohd1IA/ # Channel-specific transcriptions
│       └── [video_id]/
│           ├── raw_[video_id].txt
│           └── summary_[video_id].txt
└── notebooks/
    ├── general.ipynb
    └── video_status.json
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js (for Surge.sh deployment)
- YouTube Data API v3 key
- OpenRouter API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd youtube-video-summariser
   ```

2. **Install Python dependencies**
   ```bash
   pip install requests python-dotenv openai youtube-transcript-api
   ```

3. **Install Surge.sh globally**
   ```bash
   npm install -g surge
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   YOUTUBE_DATA_API_V3=your_youtube_api_key_here
   OPENROUTER_YOUTUBE_VIDEO_SUMMARISER=your_openrouter_api_key_here
   ```

5. **Configure Surge.sh (one-time setup)**
   ```bash
   surge login --email your-email@example.com --token your-surge-token
   ```

## 📋 Usage Workflow

The system follows a specific 4-step workflow. Run these scripts in order:

### Step 1: Detect New Videos
```bash
python get-latest-video-uploads.py
```
- Fetches latest videos from the configured YouTube channel
- Updates `summarise-history.json` with new video entries
- Skips videos that have already been processed

### Step 2: Extract Transcriptions
```bash
python extract-transcription.py
```
- Downloads transcriptions for all untranscribed videos
- Saves raw transcriptions to `transcriptions/[channel_id]/[video_id]/raw_[video_id].txt`
- Updates the history file to mark videos as transcribed

### Step 3: Generate AI Summaries
```bash
python generate-summary.py
```
- Processes untranscribed videos through AI models
- Generates structured summaries using prompts from `prompts/prompt_1.txt`
- Extracts stock ticker tags using `prompts/prompt_ticker_tag.txt`
- Saves summaries to `transcriptions/[channel_id]/[video_id]/summary_[video_id].txt`
- Updates history file with summary status and ticker tags

### Step 4: Deploy to Web
```bash
./surge-up.sh
```
- Deploys the web interface to Surge.sh
- Makes summaries publicly accessible at the configured domain

## 🔧 Configuration

### YouTube Channel Configuration
Edit `get-latest-video-uploads.py`:
```python
CHANNEL_ID = "UC5cEHfCr6WOE1R1zcohd1IA"  # Change to your target channel
MAX_RESULTS = 5  # Number of recent videos to check
```

### AI Model Configuration
Edit `generate-summary.py`:
```python
MODEL_NAME = "meta-llama/llama-3.2-1b-instruct:free"  # Change AI model as needed
```

### Web Deployment Configuration
Edit `surge-up.sh`:
```bash
DOMAIN="curly-parcel.surge.sh"  # Change to your preferred domain
```

## 📊 Data Structure

### Video History JSON Format
```json
{
    "video_id": "unique_video_id",
    "channel_id": "youtube_channel_id",
    "title": "Video Title",
    "published_at": "2025-06-28T02:02:59Z",
    "transcribed": false,
    "transcription_dir": "transcriptions/channel_id/video_id",
    "summarised": false,
    "summarised_dir": "transcriptions/channel_id/video_id",
    "youtube_link": "https://www.youtube.com/watch?v=video_id",
    "ticker_tags": ["NVDA", "GOOGL", "AMD"],
    "posted_to_discord": false
}
```

### Summary Format
Summaries follow a structured format with sections:
- 🎯 Video Objective
- 📌 Key Takeaways
- 📊 Companies Mentioned
- 🚫 Companies Criticized or Deprioritized
- 🧠 Expert Commentary
- 💡 Closing Thoughts / Final Recommendations

## 🌐 Web Interface

The web interface (`index.html`) provides:
- Clean, responsive design
- Expandable summary sections
- Direct links to original YouTube videos
- Color-coded stock ticker tags
- Markdown rendering for summaries

### Features
- **Responsive Design**: Works on desktop and mobile
- **Dynamic Loading**: Summaries load on-demand
- **Stock Tag Colors**: Pre-configured colors for major stocks
- **YouTube Integration**: Direct links to source videos

## 🤖 AI Integration

### OpenRouter Models
The system uses OpenRouter for AI processing:
- **Primary Model**: `meta-llama/llama-3.2-1b-instruct:free`
- **Alternative Models**: 
  - `mistralai/mistral-small-3.2-24b-instruct:free` (high quality)
  - `minimax/minimax-m1:extended` (slower but comprehensive)

### Prompt Engineering
Two specialized prompts:
1. **Main Summary Prompt** (`prompts/prompt_1.txt`): Structured financial analysis
2. **Ticker Tag Prompt** (`prompts/prompt_ticker_tag.txt`): Stock symbol extraction

## 🔄 Automation

### Manual Execution
Run the workflow manually:
```bash
# Complete workflow
python get-latest-video-uploads.py
python extract-transcription.py
python generate-summary.py
./surge-up.sh
```

### Scheduled Execution
Set up cron jobs for automation:
```bash
# Check for new videos every hour
0 * * * * cd /path/to/project && python get-latest-video-uploads.py

# Process transcriptions every 2 hours
0 */2 * * * cd /path/to/project && python extract-transcription.py

# Generate summaries every 3 hours
0 */3 * * * cd /path/to/project && python generate-summary.py

# Deploy updates daily at 6 AM
0 6 * * * cd /path/to/project && ./surge-up.sh
```

## 🛠️ Troubleshooting

### Common Issues

1. **YouTube API Quota Exceeded**
   - Check your YouTube Data API v3 quota
   - Reduce `MAX_RESULTS` in `get-latest-video-uploads.py`

2. **Transcription Failures**
   - Some videos may not have available transcripts
   - Check video language and availability

3. **AI Model Errors**
   - Verify OpenRouter API key
   - Check model availability and rate limits
   - Try alternative models in `generate-summary.py`

4. **Surge.sh Deployment Issues**
   - Ensure you're logged into Surge.sh
   - Check domain availability
   - Verify Node.js installation

### Debug Mode
Add debug prints to scripts:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔮 Future Enhancements

- **Discord Bot Integration**: Complete the Discord utility for automated posting
- **Multiple Channel Support**: Process multiple YouTube channels
- **Advanced Analytics**: Track summary performance and engagement
- **Email Notifications**: Alert on new video processing
- **Database Integration**: Replace JSON files with proper database
- **API Endpoints**: REST API for programmatic access

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add contact information or support channels here]