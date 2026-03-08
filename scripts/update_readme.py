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
            # Compact green badge
            badge = "![Online](https://img.shields.io/badge/-Online-31c854?style=flat-square)"
            return badge, count
        return "![Offline](https://img.shields.io/badge/-Offline-critical?style=flat-square)", 0
    except:
        return "![Down](https://img.shields.io/badge/-Down-grey?style=flat-square)", 0

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

    for stream in STREAMS:
        badge, count = get_status_info(stream['url'])
        total_channels += count
        # This places the badge right after the TV emoji and name
        line = f"| 📺 {badge} **{stream['name']}** | `{count}` | [Direct Link]({stream['url']}) |"
        content.append(line)

    content.append(f"\n> **Total Network Capacity:** `{total_channels}` Channels")
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))

if __name__ == "__main__":
    update_dashboard()
