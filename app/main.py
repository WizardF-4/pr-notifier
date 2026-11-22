
import os
import hmac
import hashlib

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException

from app.telegram import send_telegram_message

load_dotenv()

app = FastAPI(
    title="PR Notifier",
    description="GitHub Pull Request Notification Bot",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "PR Notifier is running!"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/webhook/github")
async def github_webhook(request: Request):
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")

    if not secret:
        raise HTTPException(
            status_code=503,
            detail="GitHub webhook secret is not configured"
        )

    body = await request.body()

    signature = request.headers.get("X-Hub-Signature-256", "")

    expected_signature = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=401,
            detail="Invalid signature"
        )

    event = request.headers.get("X-GitHub-Event")

    if event != "pull_request":
        return {"message": "Event ignored"}

    payload = await request.json()

    if payload.get("action") != "opened":
        return {"message": "Action ignored"}

    pr = payload["pull_request"]
    repository = payload["repository"]

    message = (
        "Новий Pull Request!\n\n"
        f"Репозиторій: {repository['full_name']}\n"
        f"Номер: #{pr['number']}\n"
        f"Назва: {pr['title']}\n"
        f"Автор: {pr['user']['login']}\n"
        f"Гілки: {pr['head']['ref']} → {pr['base']['ref']}\n\n"
        f"Посилання: {pr['html_url']}"
    )

    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not chat_id:
        raise HTTPException(
            status_code=503,
            detail="Telegram chat ID is not configured"
        )

    await send_telegram_message(chat_id, message)

    return {"message": "Pull Request notification sent"}

