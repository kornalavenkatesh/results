import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot

# Hard-coded values (your bot token & chat ID)
BOT_TOKEN = "8207943916:AAHuYb7DTsHA9Vcjd8ArNEQC_C0Sh8utFr4"
CHAT_ID = "917106372"

bot = Bot(token=BOT_TOKEN)
url = "https://dnrcetautonomous.org/examresults"

# Track already seen results
seen_results = set()

def check_results():
    global seen_results
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.find_all("a")
        new_found = False
        for item in items:
            text = item.get_text(strip=True)
            href = item.get("href")
            if "M.Tech" in text or "MTECH" in text or ("M.Tech" in href if href else False):
                if text not in seen_results:
                    message = f"🎓 New M.Tech result uploaded:\n{text}\n🔗 {url}"
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    seen_results.add(text)
                    new_found = True
        if not new_found:
            print("No new M.Tech results.")
    except Exception as e:
        print("Error checking site:", e)

if __name__ == "__main__":
    # ✅ Startup message
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot started and watching for new M.Tech results...")
    print("📡 Monitoring started...")
    while True:
        check_results()
        time.sleep(300)  # check every 5 minutes
