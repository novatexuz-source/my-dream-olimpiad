# My Dream Olimpiad

Olimpiada/test platformasi: ro'yxatdan o'tish, qo'ng'iroqlar, testlar, natijalar va Telegram bot.

## Stack

- **Backend**: Django 5 + DRF + SimpleJWT
- **Frontend**: React 19 + Vite + Tailwind CSS + Zustand
- **Database**: PostgreSQL (Supabase)
- **Telegram bot**: Aiogram 3 (polling)
- **Deploy**: Render (backend) + Vercel (frontend) + Fly.io (bot)

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

```bash
cd backend
python -m apps.tg_bot.bot.main
```

## Environment variables

See `backend/.env.example` and `frontend/.env.example`.

**Backend required:**
- `SECRET_KEY` — Django secret (50+ chars, random)
- `DEBUG` — `True` for dev, `False` for prod
- `ALLOWED_HOSTS` — comma-separated hosts
- `DATABASE_URL` — Supabase Session Pooler URL (port 5432, NOT 6543)
- `BOT_TOKEN` — from @BotFather
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

### 4. Telegram bot — Fly.io
1. `fly launch` in `backend/` (no deploy yet)
2. `fly secrets set BOT_TOKEN=... DATABASE_URL=... SECRET_KEY=...`
3. Set `app = "your-bot-name"` and configure Dockerfile to run `python -m apps.tg_bot.bot.main`
4. `fly deploy`

### 5. Keep backend awake — UptimeRobot
- Add HTTP monitor pinging `https://your-backend.onrender.com/` every 5 min
