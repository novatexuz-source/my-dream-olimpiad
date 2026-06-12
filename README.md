# My Dream Olimpiad

Olimpiada/test platformasi: ro'yxatdan o'tish, qo'ng'iroqlar, testlar, natijalar va Telegram bot.

## Stack

- **Backend**: Django 5 + DRF + SimpleJWT
- **Frontend**: React 19 + Vite + Tailwind CSS
- **Database**: PostgreSQL (Supabase)
- **Telegram bot**: Aiogram 3 — production'da WEBHOOK rejimi (Render backend ichida), lokalda polling
- **Deploy**: Render (backend + bot webhook) + Vercel (frontend) + Supabase (database)

## Project structure

```
backend/        Django project (apps: users, registration, tests_app, exams, results, monitor_app, tg_bot)
frontend/       React + Vite app
```

## Local development

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
copy .env.example .env         # then fill values
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
copy .env.example .env         # then fill VITE_API_BASE_URL
npm run dev
```

### Telegram bot (local polling)

⚠️ Lokal polling production webhookni O'CHIRIB yuboradi, shuning uchun maxsus flag talab qilinadi:

```bash
cd backend
set ALLOW_POLLING=1        # Windows (macOS/Linux: export ALLOW_POLLING=1)
python -m apps.tg_bot.bot.main
```

Ishlatib bo'lgach production webhookni tiklash uchun brauzerda oching (yoki backendni restart qiling — webhook avtomatik tiklanadi):

```
https://my-dream-olimpiad.onrender.com/api/tg/set-webhook/<BOT_TOKEN>/
```

## Environment variables

See `backend/.env.example` and `frontend/.env.example`.

**Backend required:**
- `SECRET_KEY` — Django secret (50+ chars, random)
- `DEBUG` — `True` for dev, `False` for prod (defaults to `False` when unset)
- `ALLOWED_HOSTS` — comma-separated hosts
- `DATABASE_URL` — Supabase Session Pooler URL (port 5432, NOT 6543)
- `BOT_TOKEN` — from @BotFather
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` — admin account; migrations create/rotate the admin from these (REQUIRED in production, no hardcoded fallback)
- `WEBAPP_URL` — frontend register page URL used in Telegram buttons
- `CORS_ALLOWED_ORIGINS` — frontend URL (prod only)
- `CSRF_TRUSTED_ORIGINS` — frontend + backend URLs (prod only)

**Frontend required:**
- `VITE_API_BASE_URL` — e.g. `https://your-backend.onrender.com/api`

## Deploy

### 1. Database — Supabase
1. Create project at supabase.com
2. Settings → Database → Connection string → **Session pooler** (port 5432)
3. Copy URL → use as `DATABASE_URL`

### 2. Backend — Render
1. New Web Service → connect GitHub repo
2. Root directory: `backend`
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Start command: `gunicorn config.wsgi:application`
5. Add env vars (see list above)

### 3. Frontend — Vercel
1. New project → import GitHub repo
2. Root directory: `frontend`
3. Framework preset: Vite
4. Add env var: `VITE_API_BASE_URL=https://your-backend.onrender.com/api`

### 4. Telegram bot — webhook (alohida server KERAK EMAS)
Bot Render'dagi backend ichida webhook orqali ishlaydi:
- Har deploy/restart'da webhook avtomatik o'rnatiladi (`config/wsgi.py` — Render'ning `RENDER_EXTERNAL_URL` env'idan foydalanadi).
- Qo'lda o'rnatish/tekshirish: brauzerda `https://your-backend.onrender.com/api/tg/set-webhook/<BOT_TOKEN>/` oching.
- Webhook holatini tekshirish: `https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo`

### 5. Keep backend awake — UptimeRobot (MAJBURIY!)
Render free tier 15 daqiqa harakatsizlikdan keyin uxlab qoladi — bot ham, sayt ham sekinlashadi/javob bermaydi.
- uptimerobot.com da bepul akkaunt oching
- HTTP monitor: `https://my-dream-olimpiad.onrender.com/` (endi `{"status": "ok"}` qaytaradi), interval: 5 min
