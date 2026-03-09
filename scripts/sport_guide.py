import requests
import os
from datetime import datetime

# The specific widget URL provided by the user
GUIDE_URL = "https://sport-tv-guide.live/sportwidget/fecb68ae09be?time_zone=America%2FNew_York&sports=22,19,5,4,1,40,39,7,16&grp=1"

def run():
    # Retrieve the secret specifically for the sports channel
    webhook_url = os.getenv("DISCORD_SPORTS_WEBHOOK")
    
    if not webhook_url:
        print("Error: DISCORD_SPORTS_WEBHOOK secret not found in environment.")
        return

    # Payload for the Discord Embed
    payload = {
        "username": "Sports Schedule Bot",
        "avatar_url": "https://img.icons8.com/color/96/trophy.png",
        "embeds": [{
            "title": "🏆 Today's Live Sports Schedule",
            "description": "Click the link below to view the full live broadcast schedule for NFL, NBA, MLB, and more.",
            "url": GUIDE_URL,
            "color": 15158332, # Vibrant Red-Orange
            "fields": [
                {
                    "name": "🔗 Live TV Guide", 
                    "value": f"[Open Sports Widget]({GUIDE_URL})"
                },
                {
                    "name": "⏰ Timezone", 
                    "value": "America/New_York", 
                    "inline": True
                }
            ],
            "footer": {
                "text": "BuddyChewChew Sports Automation",
                "icon_url": "https://img.icons8.com/color/48/football.png"
            },
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    # Post the new message to Discord
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Successfully posted sports guide to #sports-guide.")
        else:
            print(f"Failed to post. Discord returned: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run()
