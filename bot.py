import requests
import html
import json
import os
import time
from bs4 import BeautifulSoup

TOKEN = "8340890767:AAGw24PUeo74NWSyDgG1DHwPWytnZtumahU"
CHAT_ID = "-1003647530419"
DB_FILE = "sent_jobs.json"


# ---------------- LOAD HISTORY ----------------
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        sent_jobs = set(json.load(f))
else:
    sent_jobs = set()


# ---------------- TELEGRAM SEND ----------------
def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": msg,
                "disable_web_page_preview": False
            },
            timeout=20
        )
        time.sleep(1.5)
    except:
        print("Telegram send failed")


# =====================================================
# 🔵 BARCLAYS (INDIA FILTER)
# =====================================================
def scan_barclays():
    global sent_jobs

    print("Scanning Barclays (India only)...")

    # India search page
    url = "https://search.jobs.barclays/search-jobs/India"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("Barclays fetch failed")
        return

    job_cards = soup.find_all("a", href=True)

    for card in job_cards:
        href = card["href"]

        if "/job/" not in href:
            continue

        link = "https://search.jobs.barclays" + href

        if link in sent_jobs:
            continue

        title = card.get_text(strip=True)
        if not title:
            continue

        message = f"""🏦 Barclays Hiring

👔 {title}
📍 India

🔗 Apply:
{link}

#Jobs #Barclays
"""

        send(message)
        sent_jobs.add(link)

    print("Barclays scan complete")


# =====================================================
# 🔴 HSBC (INDIA FILTER)
# =====================================================
def scan_hsbc():
    global sent_jobs

    print("Scanning HSBC (India only)...")

    url = "https://portal.careers.hsbc.com/careers?location=India&pid=563774607726794&domain=hsbc.com"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("HSBC fetch failed")
        return

    job_links = soup.find_all("a", href=True)

    for tag in job_links:
        href = tag["href"]

        if "/job/" not in href:
            continue

        link = "https://portal.careers.hsbc.com" + href

        if link in sent_jobs:
            continue

        title = tag.get_text(strip=True)
        if not title:
            continue

        message = f"""🏦 HSBC Hiring

👔 {title}
📍 India

🔗 Apply:
{link}

#Jobs #HSBC
"""

        send(message)
        sent_jobs.add(link)

    print("HSBC scan complete")


# =====================================================
# 🚀 RUN SCANNERS
# =====================================================
scan_barclays()
scan_hsbc()


# ---------------- SAVE HISTORY ----------------
with open(DB_FILE, "w") as f:
    json.dump(list(sent_jobs), f)

print("Run complete")