import requests
import re
from datetime import datetime

# The complete list of your stream sources
STREAMS = [
    {"name": "🏅 Live Events Filter", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8"},
    {"name": "📺 Roxie Streams", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/Roxiestreams.m3u"},
    {"name": "⚡ Power V2", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/powerv2/powerv2.m3u8"},
    {"name": "🔥 Buddy Live V1", "url": "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/buddylive_v1.m3u"},
    {"name": "📱 The TV App", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/TheTVApp.m3u8"}
]

def get_stream_info(url):
    try:
        # Use a timeout to keep the dashboard snappy
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            # Counts lines starting with #EXTINF to get the total number of channels
            channel_count = len(re.findall(r'^#EXTINF', response.text, re.MULTILINE))
            return "🟢 Online", channel_count
        return "🔴 Offline", 0
    except Exception:
        return "⚪ Down", 0

def update_dashboard():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Header for your Profile README
    content = [
        "# 🚀 BuddyChewChew's Stream Network",
        f"> **System Health Check:** `{now}`",
        "",
        "| Stream Source | Status | Channels | Direct Link |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for stream in STREAMS:
        status, count = get_stream_info(stream['url'])
        # Formats each row of the table
        line = f"| **{stream['name']}** | {status} | `{count}` | [M3U/8 Link]({stream['url']}) |"
        content.append(line)

    content.append("\n---\n*Dashboard auto-refreshes every hour. To manually update, trigger the 'Update Profile Dashboard' Action.*")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))

if __name__ == "__main__":
    update_dashboard()
