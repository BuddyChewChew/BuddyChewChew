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
        if r.status_code == 200:
            count = len(re.findall(r'^#EXTINF', r.text, re.MULTILINE))
            badge, dot = "![Online](https://img.shields.io/badge/Status-Online-31c854?style=flat-square)", "🟢"
            return count, badge, dot
        return 0, "![Offline](https://img.shields.io/badge/Status-Offline-critical?style=flat-square)", "🔴"
    except:
        return 0, "![Down](https://img.shields.io/badge/Status-Down-grey?style=flat-square)", "⚪"

def run():
    webhook = os.getenv("DISCORD_LIVE_WEBHOOK")
    msg_id = os.getenv("DISCORD_LIVE_MESSAGE_ID")
    discord_report, readme_rows, total = [], [], 0

    for s in STREAMS:
        if "heading" in s:
            discord_report.append(f"\n**{s['heading']}**")
            readme_rows.append(f"| | **{s['heading']}** | |")
            continue
        count, badge, dot = get_status(s['url'])
        total += count
        readme_rows.append(f"| {badge} | **{s['name']}** ({count}) | [Link]({s['url']}) |")
        discord_report.append(f"{dot} **{s['name']}** ({count}) — [[Link]]({s['url']})")
    
    payload = {"username": "Stream Monitor", "embeds": [{"title": "📺 Live TV Health Check", "description": "\n".join(discord_report) + f"\n\n**Total:** `{total}`", "color": 3262548, "timestamp": datetime.utcnow().isoformat()}]}
    if webhook:
        if msg_id: requests.patch(f"{webhook}/messages/{msg_id}", json=payload)
        else: requests.post(f"{webhook}?wait=true", json=payload)
    with open("temp_live.txt", "w") as f: f.write("\n".join(readme_rows))

if __name__ == "__main__":
    run()
