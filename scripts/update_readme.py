import requests
from datetime import datetime

# List of your repos and the raw files you want to track
STREAMS = [
    {"name": "🏅 SS99 Live", "url": "https://raw.githubusercontent.com/BuddyChewChew/SS99/main/SS99.m3u"},
    {"name": "🏐 Live Events", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/main/liveeventsfilter.m3u8"}
]

def check_status(url):
    try:
        r = requests.head(url, timeout=5)
        return "✅ Online" if r.status_code == 200 else "❌ Offline"
    except:
        return "⚠️ Error"

def generate_readme():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    content = f"# 📺 My Live Stream Dashboard\n\n"
    content += f"Last Updated: `{timestamp}`\n\n"
    content += "| Stream Name | Status | M3U Link |\n"
    content += "| :--- | :--- | :--- |\n"
    
    for stream in STREAMS:
        status = check_status(stream['url'])
        content += f"| {stream['name']} | {status} | [Link]({stream['url']}) |\n"
    
    content += "\n\n---\n*This dashboard updates automatically every hour.*"
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_readme()