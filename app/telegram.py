import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def send_telegram_message(chat_id: str, message: str):
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не знайдено у .env")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message
            }
        )

        response.raise_for_status()
        return response.json()
