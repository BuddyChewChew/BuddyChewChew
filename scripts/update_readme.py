import requests
import re
import os
from datetime import datetime

STREAMS = [
    {"name": "🏅 Live Events Filter", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8"},
    {"name": "📺 Roxie Streams", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/Roxiestreams.m3u"},
    {"name": "⚡ Power V2", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/powerv2/powerv2.m3u8"},
    {"name": "🔥 Buddy Live V1", "url": "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/buddylive_v1.m3u"},
    {"name": "📱 The TV App", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/TheTVApp.m3u8"}
]

def get_stream_info(url):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            channel_count = len(re.findall(r'^#EXTINF', response.text, re.MULTILINE))
            return "🟢 Online", channel_count
        return "🔴 Offline", 0
    except:
        return "⚪ Down", 0

def send_to_discord(report_lines):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url:
        return

    # Create a nice Discord embed message
    description = "\n".join(report_lines)
    data = {
        "username": "Stream Health Monitor",
        "embeds": [{
            "title": "📡 Stream Network Status Report",
            "description": description,
            "color": 3066993, # A nice green color
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    requests.post(webhook_url, json=data)

def update_dashboard():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    content = [
        "# 🚀 BuddyChewChew's Stream Network",
        f"> **System Health Check:** `{now}`",
        "",
        "| Stream Source | Status | Channels | Direct Link |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    discord_report = []

    for stream in STREAMS:
        status, count = get_stream_info(stream['url'])
        line = f"| **{stream['name']}** | {status} | `{count}` | [Link]({stream['url']}) |"
        content.append(line)
        # Add to the discord report
        discord_report.append(f"**{stream['name']}**: {status} ({count} channels)")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    
    # Send the update to Discord
    send_to_discord(discord_report)

if __name__ == "__main__":
    update_dashboard()
