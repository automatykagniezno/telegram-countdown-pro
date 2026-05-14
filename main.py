from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime
import asyncio
import os

TOKEN = os.getenv("8915227053:AAF9T201HjWC-dkKY_aU3ooxSWFXHeNnXSc")
CHAT_ID = os.getenv("-1003392815023")

bot = Bot(token=TOKEN)

TARGET_DATE = datetime(2026, 6, 6, 19, 0, 0)

MESSAGE_FILE = "message.txt"

message_id = None


def load_message_id():
    global message_id

    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r") as f:
            content = f.read().strip()

            if content:
                message_id = int(content)


def save_message_id(msg_id):
    with open(MESSAGE_FILE, "w") as f:
        f.write(str(msg_id))


async def create_message():
    global message_id

    msg = await bot.send_message(
        chat_id=CHAT_ID,
        text="⏳ Uruchamianie odliczania..."
    )

    message_id = msg.message_id

    save_message_id(message_id)

    try:
        await bot.pin_chat_message(
            chat_id=CHAT_ID,
            message_id=message_id,
            disable_notification=True
        )
    except:
        pass


async def update_countdown():
    global message_id

    while True:
        now = datetime.now()
        diff = TARGET_DATE - now

        if diff.total_seconds() <= 0:
            text = (
                "🎉 TO JUŻ DZIŚ! 🎉\n\n"
                "🍾🍾🍾"
            )
        else:
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            text = (
                "🎯 ODLICZANIE DO 6 CZERWCA\n\n"
                f"📅 {days} dni\n"
                f"🕐 {hours} godzin\n"
                f"⌛ {minutes} minut\n"
                f"⚡ {seconds} sekund\n\n"
                "🔥 Ekipa już odlicza..."
            )

        try:
            await bot.edit_message_text(
                chat_id=CHAT_ID,
                message_id=message_id,
                text=text
            )
        except TelegramError:
            pass

        await asyncio.sleep(5)


async def main():
    load_message_id()

    if message_id is None:
        await create_message()

    await update_countdown()


asyncio.run(main())
