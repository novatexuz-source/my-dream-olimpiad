"""
Bot starter - ensures only ONE instance runs.
Sends deleteWebhook + drops pending updates before polling.
"""
import asyncio
import os
import sys

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apps.tg_bot.bot.handlers import registration

BOT_TOKEN = config('BOT_TOKEN')

async def main():
    bot = Bot(token=BOT_TOKEN)
    
    # Clear any existing webhook and pending updates to avoid conflicts
    await bot.delete_webhook(drop_pending_updates=True)
    print("[OK] Webhook cleared, pending updates dropped")
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(registration.router)
    
    print("[BOT] Bot ishga tushdi: @my_dream_olimpiad_bot")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())
