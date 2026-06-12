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


def _ensure_admin():
    """Create/rotate the admin account from env vars on every server start.

    The old approach was a one-time migration — once it had run (e.g. before
    the env vars were added), changing ADMIN_USERNAME/ADMIN_PASSWORD on Render
    had no effect. Syncing at startup makes the env vars the source of truth.
    Dashes/spaces are stripped so '+998-91-...' matches the login form, which
    submits the phone without separators.
    """
    username = (os.getenv('ADMIN_USERNAME') or '').replace('-', '').replace(' ', '')
    password = os.getenv('ADMIN_PASSWORD') or ''
    if not username or not password:
        return
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)
        needs_update = (
            created
            or not user.check_password(password)
            or not user.is_superuser
            or not user.is_active
        )
        if needs_update:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            if hasattr(user, 'role'):
                user.role = 'super_admin'
            user.save()
            print(f"[ADMIN] account ensured for {username}")
    except Exception as exc:  # never block server startup over this
        print(f"[ADMIN] ensure failed: {exc}")


_ensure_telegram_webhook()
_ensure_admin()
