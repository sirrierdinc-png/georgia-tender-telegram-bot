import requests
from bs4 import BeautifulSoup
import os

TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT")

URL = "https://tenders.procurement.gov.ge/public/?lang=en"

KEYWORDS = [
    "water", "potable water", "drinking water", "water supply", "water distribution",
    "wastewater", "waste water", "sewage", "sewer", "sewerage", "stormwater", "storm water",
    "drainage", "flood protection", "flood control",

    "treatment plant", "water treatment plant", "wastewater treatment plant",
    "WWTP", "WTP", "STP", "effluent treatment", "biological treatment",
    "membrane treatment", "filtration plant",
    "pumping station", "booster station", "lift station",

    "pipeline", "pipe network", "pipeline construction", "pipe installation",
    "HDPE pipeline", "ductile iron pipeline", "steel pipeline",
    "gravity pipeline", "pressure pipeline",

    "road", "highway", "bypass road", "ring road",
    "road construction", "road rehabilitation", "road reconstruction",
    "asphalt", "pavement",

    "bridge", "viaduct", "overpass", "underpass", "culvert",
    "tunnel", "road tunnel", "railway tunnel",

    "railway", "rail line", "railway infrastructure",
    "tramway", "tram line",
    "metro", "subway",

    "school", "hospital",
    "public building", "government building",

    "infrastructure", "civil works", "engineering works",
    "earthworks", "excavation", "trenching", "retaining wall"
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def main():
    r = requests.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a", href=True)

    for link in links:
        title = link.get_text(strip=True)
        href = link["href"]

        if not title:
            continue

        lower_title = title.lower()
        if any(k.lower() in lower_title for k in KEYWORDS):
            msg = f"📌 NEW TENDER MATCH\n\n{title}\n\nhttps://tenders.procurement.gov.ge{href}"
            send_telegram(msg)

if __name__ == "__main__":
    main()
