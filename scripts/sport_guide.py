import requests
import os
from datetime import datetime

# Direct live sports link
LIVE_GUIDE_URL = "https://sport-tv-guide.live/live/sport"

def run():
    webhook_url = os.getenv("DISCORD_SPORTS_WEBHOOK")
    
    if not webhook_url:
        print("Error: DISCORD_SPORTS_WEBHOOK secret not found.")
        return

    # 12-hour clock format (e.g., 08:30 AM)
    current_time_12h = datetime.now().strftime("%I:%M %p")

    payload = {
        "username": "Sports Schedule Bot",
        "avatar_url": "https://img.icons8.com/color/96/trophy.png",
        "embeds": [{
            "title": "🏆 Live Sports TV Guide",
            "description": f"Click the link below to view the current broadcast schedule.\n\n**Last updated: {current_time_12h}**",
            "url": LIVE_GUIDE_URL,
            "color": 15158332,
            "fields": [
                {
                    "name": "📡 Interactive Schedule", 
                    "value": f"[Open Live Sports Guide]({LIVE_GUIDE_URL})"
                }
            ],
            "footer": {
                "text": "BuddyChewChew Sports Automation",
                "icon_url": "https://img.icons8.com/color/48/football.png"
            }
        }]
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(f"Successfully posted to #sports-guide at {current_time_12h}")
        else:
            print(f"Failed to post. Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
