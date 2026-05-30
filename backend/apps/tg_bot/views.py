"""
Telegram webhook endpoint for the Render-hosted Django backend.

The bot runs in WEBHOOK mode (not polling): Telegram POSTs each update to
`/api/tg/webhook/<BOT_TOKEN>/`, we feed it to the aiogram Dispatcher, and the
existing handlers (apps.tg_bot.bot.handlers.registration) reply.
"""
import asyncio
import json
import os

from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

BOT_TOKEN = os.getenv('BOT_TOKEN')

_dispatcher = None


def _get_dispatcher():
    """Build the Dispatcher once per worker and reuse it."""
    global _dispatcher
    if _dispatcher is None:
        from aiogram import Dispatcher
        from aiogram.fsm.storage.memory import MemoryStorage
        from apps.tg_bot.bot.handlers import registration

        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(registration.router)
        _dispatcher = dp
    return _dispatcher


async def _feed(update_dict):
    from aiogram import Bot
    from aiogram.types import Update

    bot = Bot(token=BOT_TOKEN)
    try:
        update = Update.model_validate(update_dict, context={"bot": bot})
        await _get_dispatcher().feed_update(bot, update)
    finally:
        await bot.session.close()


@csrf_exempt
def telegram_webhook(request, token):
    """Receive updates from Telegram and process them synchronously."""
    if not BOT_TOKEN or token != BOT_TOKEN:
        return HttpResponseForbidden('forbidden')
    if request.method != 'POST':
        return HttpResponse('ok')
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return HttpResponse('bad request', status=400)
    try:
        asyncio.run(_feed(data))
    except Exception:
        import traceback
        traceback.print_exc()
    # Always 200 so Telegram does not spam retries on a handler error.
    return HttpResponse('ok')


@csrf_exempt
def set_webhook(request, token):
    """Visit once in a browser to point Telegram at this server's webhook URL."""
    if not BOT_TOKEN or token != BOT_TOKEN:
        return HttpResponseForbidden('forbidden')

    import requests

    webhook_url = f"https://{request.get_host()}/api/tg/webhook/{BOT_TOKEN}/"
    resp = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
        params={"url": webhook_url, "drop_pending_updates": "true"},
        timeout=30,
    )
    return JsonResponse({"webhook_url": webhook_url, "telegram": resp.json()})
