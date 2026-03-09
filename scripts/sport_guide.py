import requests
import os
from datetime import datetime

# Your specific widget URL
GUIDE_URL = "https://sport-tv-guide.live/sportwidget/fecb68ae09be?time_zone=America%2FNew_York&sports=22,19,5,4,1,40,39,7,16&grp=1"

def run():
    # Grabs the secret you already have saved in GitHub
    webhook = os.getenv("DISCORD_LIVE_WEBHOOK")
    
    if not webhook:
        print("Error: DISCORD_LIVE_WEBHOOK secret not found.")
        return

    payload = {
        "username": "Sports Guide Bot",
        "avatar_url": "https://img.icons8.com/color/96/trophy.png", # Custom Trophy Icon
        "embeds": [{
            "title": "📅 Today's Live Sports Schedule",
            "description": "Daily broadcast schedule for NFL, NBA, MLB, and more.",
            "url": GUIDE_URL,
            "color": 15158332, # Reddish-Orange color
            "fields": [
                {
                    "name": "🔗 Interactive Guide", 
                    "value": f"[Open Live Sports TV Guide]({GUIDE_URL})"
                }
            ],
            "footer": {"text": "BuddyChewChew Sports Monitor"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    # Sends a fresh message every time (not an edit)
    requests.post(webhook, json=payload)

if __name__ == "__main__":
    run()
