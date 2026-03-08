import requests
from datetime import datetime

# The specific links you provided
STREAMS = [
    {"name": "🏅 Live Events Filter", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8"},
    {"name": "📺 Roxie Streams", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/Roxiestreams.m3u"},
    {"name": "⚡ Power V2", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/powerv2/powerv2.m3u8"}
]

def check_status(url):
    try:
        # We use a GET request but only download the first few bytes to check if it's active
        r = requests.get(url, timeout=10, stream=True)
        if r.status_code == 200:
            return "🟢 Online"
        return "🔴 Offline"
    except:
        return "⚪ Down"

def generate_readme():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # This matches the style of a GitHub Profile README
    content = f"# 🚀 BuddyChewChew's Stream Dashboard\n\n"
    content += f"> **Last System Check:** `{timestamp}`\n\n"
    content += "| Stream Source | Status | Direct Link |\n"
    content += "| :--- | :--- | :--- |\n"
    
    for stream in STREAMS:
        status = check_status(stream['url'])
        content += f"| **{stream['name']}** | {status} | [M3U8 Link]({stream['url']}) |\n"
    
    content += "\n\n---\n*Dashboard auto-refreshes every hour via GitHub Actions.*"
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_readme()
