import os
import json
from datetime import date, datetime
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen


BOT_TOKEN = os.environ["BOT_TOKEN"]


CHANNELS = {
    "@otchet_do_ng": ("нового года", 1, 1, "https://t.me/otchet_do_ng"),
    "@otchet_do_zimi": ("зимы", 12, 1, "https://t.me/otchet_do_zimi"),
    "@otchet_do_vesni": ("весны", 3, 1, "https://t.me/otchet_do_vesni"),
    "@othet_do_leta": ("лета", 6, 1, "https://t.me/othet_do_leta"),
    "@otchet_do_oseni": ("осени", 9, 1, "https://t.me/otchet_do_oseni"),
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
        "text": text,
        "parse_mode": "HTML",
        "link_preview_options": {
            "is_disabled": True
        }
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

    for channel, (event_name, month, day, channel_url) in CHANNELS.items():
        event_date = date(today.year, month, day)

        # В день события сразу начинаем новый годовой отсчёт
        if event_date <= today:
            event_date = date(today.year + 1, month, day)

        days_left = (event_date - today).days

        text = (
            f"До {event_name} осталось "
            f"{days_left} {days_word(days_left)}\n\n"
            f'👉 <a href="{channel_url}">Подписаться на отчёт</a>'
        )

        send_message(channel, text)


if __name__ == "__main__":
    main()
