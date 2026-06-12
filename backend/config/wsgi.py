"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()


def _ensure_telegram_webhook():
    """Re-register the Telegram webhook on every server start.

    Render free instances spin down and anyone running the local polling bot
    deletes the webhook — either way the bot silently stops. Re-setting it at
    startup makes the webhook self-healing. RENDER_EXTERNAL_URL is injected by
    Render automatically, so this is a no-op in local development.
    """
    base_url = os.getenv('RENDER_EXTERNAL_URL') or os.getenv('WEBHOOK_BASE_URL')
    bot_token = os.getenv('BOT_TOKEN')
    if not base_url or not bot_token:
        return
    try:
        import requests

        webhook_url = f"{base_url.rstrip('/')}/api/tg/webhook/{bot_token}/"
        resp = requests.get(
            f"https://api.telegram.org/bot{bot_token}/setWebhook",
            params={"url": webhook_url},
            timeout=15,
        )
        print(f"[TG] setWebhook -> {resp.json().get('description', resp.status_code)}")
    except Exception as exc:  # never block server startup over this
        print(f"[TG] setWebhook failed: {exc}")


_ensure_telegram_webhook()
