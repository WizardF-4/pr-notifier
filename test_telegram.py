
import os
import asyncio
from dotenv import load_dotenv
from app.telegram import send_telegram_message

load_dotenv()

async def main():
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    print("Перевірка налаштувань...")
    print("TELEGRAM_CHAT_ID знайдено:", bool(chat_id))

    if not chat_id:
        print("Помилка: CHAT_ID не знайдено!")
        return

    try:
        print("Надсилаємо повідомлення...")

        result = await send_telegram_message(
            chat_id,
            "Привіт! 👋 Це тестове повідомлення PR Notifier!"
        )

        print("Відповідь Telegram:", result)

    except Exception as error:
        print("Виникла помилка:", repr(error))


if __name__ == "__main__":
    asyncio.run(main())

