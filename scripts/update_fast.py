import requests
import re
import os
from datetime import datetime

# Full List of Regional and FAST Services
STREAMS = [
    {"heading": "▶️ Plex Regional"},
    {"name": "Plex All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_all.m3u"},
    {"name": "Plex AU", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_au.m3u"},
    {"name": "Plex CA", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_ca.m3u"},
    {"name": "Plex ES", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_es.m3u"},
    {"name": "Plex FR", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_fr.m3u"},
    {"name": "Plex GB", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_gb.m3u"},
    {"name": "Plex MX", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_mx.m3u"},
    {"name": "Plex NZ", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_nz.m3u"},
    {"name": "Plex US", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_us.m3u"},
    
    {"heading": "▶️ PlutoTV Regional"},
    {"name": "PlutoTV All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_all.m3u"},
    {"name": "PlutoTV AT", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_at.m3u"},
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
    
    {"heading": "▶️ SamsungTVPlus Regional"},
    {"name": "Samsung All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_all.m3u"},
    {"name": "Samsung AT", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_at.m3u"},
    {"name": "Samsung BR", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_br.m3u"},
    {"name": "Samsung CH", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_ch.m3u"},
    {"name": "Samsung DE", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_de.m3u"},
    {"name": "Samsung ES", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_es.m3u"},
    {"name": "Samsung FR", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_fr.m3u"},
    {"name": "Samsung GB", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_gb.m3u"},
    {"name": "Samsung IN", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_in.m3u"},
    {"name": "Samsung IT", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_it.m3u"},
    {"name": "Samsung KR", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_kr.m3u"},
    {"name": "Samsung US", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_us.m3u"},

    {"heading": "▶️ Other FAST Services"},
    {"name": "Roku All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/roku_all.m3u"},
    {"name": "Tubi All", "url": "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/tubi_all.m3u"}
]

def get_status(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            count = len(re.findall(r'^#EXTINF', r.text, re.MULTILINE))
            badge = "![Online](https://img.shields.io/badge/Status-Online-31c854?style=flat-square)"
            dot = "🟢"
            return count, badge, dot
        return 0, "![Offline](https://img.shields.io/badge/Status-Offline-critical?style=flat-square)", "🔴"
    except:
        return 0, "![Down](https://img.shields.io/badge/Status-Down-grey?style=flat-square)", "⚪"

def run():
    webhook = os.getenv("DISCORD_FAST_WEBHOOK")
    discord_report = []
    readme_rows = []
    total = 0
    for s in STREAMS:
        if "heading" in s:
            discord_report.append(f"\n**{s['heading']}**")
            readme_rows.append(f"| | **{s['heading']}** | |")
            continue
        count, badge, dot = get_status(s['url'])
        total += count
        readme_rows.append(f"| {badge} | **{s['name']}** ({count}) | [Link]({s['url']}) |")
        discord_report.append(f"{dot} **{s['name']}** — `{count}`")
    
    if webhook:
        mid = len(discord_report) // 2
        payload = {"username": "Stream Monitor", "embeds": [
            {"title": "🚀 FAST Health Check (1)", "description": "\n".join(discord_report[:mid]), "color": 3262548},
            {"title": "🚀 FAST Health Check (2)", "description": "\n".join(discord_report[mid:]) + f"\n\n**Total:** `{total}`", "color": 3262548, "timestamp": datetime.utcnow().isoformat()}
        ]}
        requests.post(webhook, json=payload)
    
    with open("temp_fast.txt", "w") as f:
        f.write("\n".join(readme_rows))

if __name__ == "__main__":
    run()
