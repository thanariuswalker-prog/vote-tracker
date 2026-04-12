import requests
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://icpolls.com/p/01KNGHM0G5658N5F7YZVKZGB5Q"
CSV_FILE = "votes.csv"

def get_votes():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers, timeout=20)

    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    results = {"YEONJUN": None, "BAEKHYUN": None}

    targets = {
        "YEONJUN": ["yeonjun", "연준"],
        "BAEKHYUN": ["baekhyun", "백현"],
    }

    for item in soup.select("div.item"):
        name_tag = item.select_one("div.item-title b")
        if not name_tag:
            continue

        name = name_tag.text.strip().lower()

        for group, keywords in targets.items():
            if results[group] is not None:
                continue

            if any(k in name for k in keywords):
                vote_tag = item.select_one(".votes")
                if vote_tag:
                    results[group] = int(vote_tag.text.replace(",", ""))

    return results


def save_csv(data):
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "YEONJUN", "BAEKHYUN"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("YEONJUN"),
            data.get("BAEKHYUN"),
        ])


def main():
    data = get_votes()
    if data:
        print("Votes:", data)
        save_csv(data)
    else:
        print("No data found")


if __name__ == "__main__":
    main()
