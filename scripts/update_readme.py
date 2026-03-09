import requests
import re
import os
from datetime import datetime

# Full manual list with every regional file from your repository
STREAMS = [
    {"heading": "⭐ Primary Streams"},
    {"name": "Live Events Filter", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/liveeventsfilter.m3u8"},
    {"name": "Roxie Streams", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/Roxiestreams.m3u"},
    {"name": "Power V2", "url": "https://raw.githubusercontent.com/BuddyChewChew/sports/refs/heads/main/powerv2/powerv2.m3u8"},
    {"name": "Buddy Live V1", "url": "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/buddylive_v1.m3u"},
    {"name": "The TV App", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/TheTVApp.m3u8"},
    {"name": "TV Main", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/tv.m3u"},
    {"name": "AX1S", "url": "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/AX1S.m3u8"},
    
    {"heading": "🎥 Plex Regional"},
    {"name": "Plex All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_all.m3u"},
    {"name": "Plex AU", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_au.m3u"},
    {"name": "Plex CA", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_ca.m3u"},
    {"name": "Plex ES", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_es.m3u"},
    {"name": "Plex FR", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_fr.m3u"},
    {"name": "Plex GB", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_gb.m3u"},
    {"name": "Plex MX", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_mx.m3u"},
    {"name": "Plex NZ", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_nz.m3u"},
    {"name": "Plex US", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_us.m3u"},
    
    {"heading": "🌌 PlutoTV Regional"},
    {"name": "PlutoTV All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_all.m3u"},
    {"name": "PlutoTV AT", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_at.m3u"},
    {"name": "PlutoTV AU", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_au.m3u"},
    {"name": "PlutoTV BR", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_br.m3u"},
    {"name": "PlutoTV CA", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_ca.m3u"},
    {"name": "PlutoTV DE", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_de.m3u"},
    {"name": "PlutoTV DK", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_dk.m3u"},
    {"name": "PlutoTV ES", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_es.m3u"},
    {"name": "PlutoTV FR", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_fr.m3u"},
    {"name": "PlutoTV GB", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_gb.m3u"},
    {"name": "PlutoTV IT", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_it.m3u"},
    {"name": "PlutoTV MX", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_mx.m3u"},
    {"name": "PlutoTV NO", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_no.m3u"},
    {"name": "PlutoTV SE", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_se.m3u"},
    {"name": "PlutoTV US", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_us.m3u"},
    
    {"heading": "📱 Other FAST Services"},
    {"name": "Roku All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/roku_all.m3u"},
    {"name": "SamsungTVPlus All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_all.m3u"},
    {"name": "Stirr All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/stirr_all.m3u"},
    {"name": "Tubi All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/tubi_all.m3u"},
    {"name": "Xumo", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/xumo.m3u"},
    {"name": "LocalNow", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/localnow.m3u"},
    {"name": "Mojo", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/mojo.m3u"}
]

def get_status_info(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            count = len(re.findall(r'^#EXTINF', response.text, re.MULTILINE))
            badge = "![Online](https://img.shields.io/badge/-Online-31c854?style=flat-square)"
            return badge, count, "🟢 Online"
        return "![Offline](https://img.shields.io/badge/-Offline-critical?style=flat-square)", 0, "🔴 Offline"
    except:
        return "![Down](https://img.shields.io/badge/-Down-grey?style=flat-square)", 0, "⚪ Down"

def send_to_discord(report_lines, total_channels):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url: return
    
    status_text = "\n".join(report_lines)
    description = f"{status_text}\n\n**Total Network Capacity:** `{total_channels}` Channels"
    
    data = {
        "username": "Stream Health Monitor",
        "embeds": [{
            "title": "📡 Stream Network Status",
            "description": description,
            "color": 3066993,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    requests.post(webhook_url, json=data)

def update_dashboard():
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    total_channels = 0
    content = ["# 📡 Stream Network Status", f"**Last Sync:** `{now}`", "", "| 📺 Repo Streams | Direct Access |", "| :--- | :--- |"]
    discord_report = []

    for item in STREAMS:
        if "heading" in item:
            header = item["heading"]
            content.append(f"| **{header}** | |")
            discord_report.append(f"\n**{header}**")
            continue

        badge, count, text_status = get_status_info(item['url'])
        total_channels += count
        
        # GitHub Table Row
        content.append(f"| 📺 {badge} **{item['name']}**: ({count} channels) | [M3U8 Link]({item['url']}) |")
        
        # Discord Embed Line (with hyperlinks)
        discord_report.append(f"📺 {text_status} [**{item['name']}**]({item['url']}): ({count} channels)")

    content.append(f"\n> **Total Network Capacity:** `{total_channels}` Channels")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    
    send_to_discord(discord_report, total_channels)

if __name__ == "__main__":
    update_dashboard()
