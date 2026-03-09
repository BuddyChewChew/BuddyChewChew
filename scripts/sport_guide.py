import requests
import os
from datetime import datetime

# The specific widget URL you found
GUIDE_URL = "https://sport-tv-guide.live/sportwidget/fecb68ae09be?time_zone=America%2FNew_York&sports=22,19,5,4,1,40,39,7,16&grp=1"

def run():
    webhook = os.getenv("DISCORD_LIVE_WEBHOOK")
    
    # In a real scenario, you'd use BeautifulSoup to parse the GUIDE_URL
    # For now, we will set up the Embed structure for your guide
    payload = {
        "username": "Sports Guide Bot",
        "embeds": [{
            "title": "🏆 Live Sports TV Guide",
            "url": "https://sport-tv-guide.live",
            "description": "Daily schedule for NFL, NBA, MLB, and more.",
            "color": 15158332,
            "fields": [
                {"name": "Check Live Schedule", "value": f"[Click here to view full guide]({GUIDE_URL})"}
            ],
            "footer": {"text": "Powered by Sport-TV-Guide"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    if webhook:
        requests.post(webhook, json=payload)

if __name__ == "__main__":
    run()
