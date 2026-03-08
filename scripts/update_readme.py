import requests
import re
import os
from datetime import datetime

STREAMS = [
    {"name": "Live Events Filter", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8"},
    {"name": "Roxie Streams", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/Roxiestreams.m3u"},
    {"name": "Power V2", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/powerv2/powerv2.m3u8"},
    {"name": "Buddy Live V1", "url": "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/buddylive_v1.m3u"},
    {"name": "The TV App", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/TheTVApp.m3u8"}
]

def get_status_info(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            count = len(re.findall(r'^#EXTINF', response.text, re.MULTILINE))
            badge = "![Online](https://img.shields.io/badge/-Online-31c854?style=flat-square)"
            return badge, count, "🟢 Online"
        return "![Offline](https://img.shields.io/badge/-Offline-critical?style=flat-square)", 0, "🔴 Offline"
    except:
        return "![Down](https://img.shields.io/badge/-Down-grey?style=flat-square)", 0, "⚪ Down"

def send_to_discord(report_lines):
    # This looks for the secret you added in GitHub Settings
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK secret not found!")
        return

    data = {
        "username": "Stream Monitor",
        "embeds": [{
            "title": "📡 Stream Network Status",
            "description": "\n".join(report_lines),
            "color": 3066993,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    requests.post(webhook_url, json=data)

def update_dashboard():
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    total_channels = 0
    
    content = [
        "# 🚀 BuddyChewChew Stream Network",
        f"**Last Sync:** `{now}`",
        "",
        "| 📺 Repo Streams | Channels | M3U Link |",
        "| :--- | :--- | :--- |"
    ]
    
    discord_report = []

    for stream in STREAMS:
        badge, count, text_status = get_status_info(stream['url'])
        total_channels += count
        # Update Table
        content.append(f"| 📺 {badge} **{stream['name']}** | `{count}` | [Direct Link]({stream['url']}) |")
        # Update Discord List
        discord_report.append(f"📺 **{stream['name']}**: {text_status} (`{count}` channels)")

    content.append(f"\n> **Total Network Capacity:** `{total_channels}` Channels")
    
    # Save the README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    
    # Trigger the Discord post
    send_to_discord(discord_report)

if __name__ == "__main__":
    update_dashboard()
