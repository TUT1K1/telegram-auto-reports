import os
import json
from datetime import date, datetime
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen


BOT_TOKEN = os.environ["BOT_TOKEN"]


CHANNELS = {
    "@otchet_do_ng": ("нового года", 2027, 1, 1),
    "@otchet_do_zimi": ("зимы", 2026, 12, 1),
    "@otchet_do_vesni": ("весны", 2027, 3, 1),
    "@othet_do_leta": ("лета", 2027, 6, 1),
    "@otchet_do_oseni": ("осени", 2027, 9, 1),
}


def days_word(number):
    last_two = number % 100
    last = number % 10

    if 11 <= last_two <= 14:
        return "дней"

    if last == 1:
        return "день"

    if 2 <= last <= 4:
        return "дня"

    return "дней"


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = json.dumps({
        "chat_id": chat_id,
        "text": text
    }).encode("utf-8")

    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=30) as response:
        response.read()


def main():
    today = datetime.now(ZoneInfo("Europe/Moscow")).date()

    for channel, (event_name, year, month, day) in CHANNELS.items():
        event_date = date(year, month, day)
        days_left = (event_date - today).days

        text = (
            f"До {event_name} осталось "
            f"{days_left} {days_word(days_left)}."
        )

        send_message(channel, text)


if __name__ == "__main__":
    main()
