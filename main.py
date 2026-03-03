import requests
from bs4 import BeautifulSoup
import os
SENT_FILE = "sent_ids.txt"
TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT")

URL = "https://tenders.procurement.gov.ge/public/?lang=en"

KEYWORDS = [
"water","potable water","drinking water","water supply","water distribution","water network","water pipeline","water transmission","water mains",

"wastewater","waste water","sewage","sewer","sewerage","sewer system","sewer network","sewer pipeline","stormwater","storm water","storm sewer","drainage","rainwater drainage","flood protection","flood control",

"treatment plant","water treatment plant","wastewater treatment plant","wwtp","wtp","stp","effluent treatment plant","biological treatment","membrane treatment","filtration plant","pumping station","booster station","lift station",

"pipeline","pipe network","pipeline construction","pipe installation","hdpe pipeline","ductile iron pipeline","steel pipeline","gravity pipeline","pressure pipeline","transmission line","distribution line",

"road","roadway","highway","expressway","bypass road","ring road","urban road","rural road","road construction","road rehabilitation","road reconstruction","road upgrading","asphalt","asphalt works","pavement","rigid pavement","flexible pavement",

"bridge","viaduct","overpass","underpass","interchange","junction","culvert","box culvert",

"tunnel","road tunnel","railway tunnel","underpass construction",

"railway","railroad","rail line","railway line","railway infrastructure","railway construction","railway rehabilitation","railway station","rail station","rail depot","depot",

"tramway","tram","tram line","tramway line","tramway construction","tramway infrastructure",

"metro","subway","underground railway","metro line","metro station",

"school","primary school","secondary school","high school","kindergarten","preschool","college","university","campus","education building",

"hospital","general hospital","medical center","clinic","health facility","healthcare building","emergency hospital","trauma center",

"public building","government building","administrative building","municipal building","city hall","ministry building","courthouse","justice building","police station","fire station",

"social facility","community center","sports complex","stadium","arena",

"industrial building","warehouse","logistics center","terminal building","airport building","airport infrastructure","hangar",

"infrastructure","public infrastructure","municipal infrastructure","urban infrastructure","utility works","underground utilities","utility relocation",

"construction","construction works","building construction","building works","civil works","civil engineering works","engineering works",

"earthworks","excavation","trenching","backfilling","retaining wall","slope stabilization","ground improvement"
]

def send_telegram(message: str):
    token = TELEGRAM_TOKEN
    chat_id = CHAT_ID

    if not token or not chat_id:
        raise RuntimeError("TG_TOKEN veya TG_CHAT boş. GitHub Secrets'i kontrol et.")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(
        url,
        data={"chat_id": chat_id, "text": message},
        timeout=30
    )

    print("TELEGRAM STATUS:", r.status_code)
    print("TELEGRAM RESPONSE:", r.text)

    # Telegram hata döndürürse Action kırmızı olsun diye hata fırlatıyoruz
    r.raise_for_status()


def main():
    # Test mesajı (bu gelmiyorsa token/chat yanlış demektir)
    send_telegram("✅ TEST: GitHub Actions çalışıyor. Telegram bağlantısı OK.")

    r = requests.get(URL, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a", href=True)

    sent = 0
    for link in links:
        title = link.get_text(strip=True)
        href = link["href"]

        if not title:
            continue

        lower_title = title.lower()
        if any(k.lower() in lower_title for k in KEYWORDS):
            full_url = href
            if href.startswith("/"):
                full_url = "https://tenders.procurement.gov.ge" + href

            msg = f"📌 NEW TENDER MATCH\n\n{title}\n\n{full_url}"
            send_telegram(msg)

            sent += 1
            if sent >= 3:
                break


if __name__ == "__main__":
    main()
