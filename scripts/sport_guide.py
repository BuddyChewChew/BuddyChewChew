import requests
import os
from datetime import datetime

# The specific widget URL for your guide
GUIDE_URL = "https://sport-tv-guide.live/sportwidget/fecb68ae09be?time_zone=America%2FNew_York&sports=22,19,5,4,1,40,39,7,16&grp=1"

def run():
    webhook = os.getenv("DISCORD_LIVE_WEBHOOK")
    
    if not webhook:
        print("Error: DISCORD_LIVE_WEBHOOK not found.")
        return

    payload = {
        "username": "Sports Guide Bot",
        "avatar_url": "https://img.icons8.com/color/96/trophy.png",
        "embeds": [{
            "title": "📅 Today's Live Sports Schedule",
            "description": "Click the link below to see today's broadcast schedule for NFL, NBA, MLB, and more.",
            "url": GUIDE_URL,
            "color": 15158332,
            "fields": [
                {
                    "name": "🔗 Interactive Guide", 
                    "value": f"[Open Live Sports TV Guide]({GUIDE_URL})"
                },
                {
                    "name": "📍 Timezone", 
                    "value": "America/New_York", 
                    "inline": True
                }
            ],
            "footer": {"text": "BuddyChewChew Sports Monitor"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    response = requests.post(webhook, json=payload)
    if response.status_code == 204:
        print("Successfully posted to Discord.")
    else:
        print(f"Failed to post: {response.status_code}")

if __name__ == "__main__":
    run()
