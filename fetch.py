
import json
import sys

import requests

assert len(sys.argv) == 2

group = sys.argv[1]

assert group in {
    # Communications
    "intelsat",  # Intelsat
    "iridium",  # Iridium
    "starlink",  # Starlink
    "oneweb",  # OneWeb
    # GNSS
    "gps-ops",  # GPS Operational
    "glo-ops",  # GLONASS Operational
    "galileo",  # Galileo
    "beidou",  # Beidou
}

resp = requests.get(f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json")

assert resp.status_code == 200

with open(f"{group}.json", "w", encoding="utf-8") as wf:
    wf.write(resp.text)

