import requests
import re
import os
from datetime import datetime

STREAMS = [
    {"heading": "⭐ Primary Streams"},
    {"name": "Live Events Filter", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8"},
    {"name": "Roxie Streams", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/Roxiestreams.m3u"},
    {"name": "Power V2", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/powerv2/powerv2.m3u8"},
    {"name": "Buddy Live V1", "url": "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/buddylive_v1.m3u"},
    {"name": "The TV App", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/TheTVApp.m3u8"},
    {"name": "TV Main", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/tv.m3u"},
    {"name": "AX1S", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/AX1S.m3u8"}
]

def get_status(url):
    try:
        r = requests.get(url, timeout=10)
        count = len(re.findall(r'^#EXTINF', r.text, re.MULTILINE)) if r.status_code == 200 else 0
        return count, "🟢" if count > 0 else "🔴"
    except:
        return 0, "⚪"

def run():
    webhook = os.getenv("DISCORD_LIVE_WEBHOOK")
    report = []
    total = 0
    for s in STREAMS:
        if "heading" in s:
            report.append(f"\n**{s['heading']}**")
            continue
        count, dot = get_status(s['url'])
        total += count
        report.append(f"{dot} **{s['name']}** — `{count}`")
    
    if webhook:
        requests.post(webhook, json={
            "embeds": [{"title": "📺 Live TV Status", "description": "\n".join(report) + f"\n\n**Total:** `{total}`", "color": 3262548}]
        })

if __name__ == "__main__":
    run()
