
import requests
import json
import re

URL = "https://allinonereborn2.online/jiotv-m3u/jtv33.m3u8"

response = requests.get(URL, timeout=30)
response.raise_for_status()

text = response.text
channels = []

name = None
group = "Other"
logo = ""

for line in text.splitlines():
    line = line.strip()

    if line.startswith("#EXTINF:"):
        match = re.search(r'tvg-name="([^"]*)"', line)
        name = match.group(1) if match else (
            line.split(",")[-1].strip()
        )

        group_match = re.search(r'group-title="([^"]*)"', line)
        group = group_match.group(1) if group_match else "Other"

        logo_match = re.search(r'tvg-logo="([^"]*)"', line)
        logo = logo_match.group(1) if logo_match else ""

    elif line and not line.startswith("#") and name:
        channels.append({
            "name": name,
            "category": group,
            "logo": logo,
            "url": line
        })
        name = None
        logo = ""

with open("playlist.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Converted {len(channels)} channels")
