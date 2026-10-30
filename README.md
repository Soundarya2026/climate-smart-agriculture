# Agri Smart — Django starter application

A runnable Django + SQLite web app for farmer accounts, farm records, soil readings, crop suitability suggestions, weather lookup, plant-disease image submissions, market-price records and an admin dashboard.

## Requirements
- Python 3.10+
- Internet connection for Bootstrap CDN and optional live weather
- Optional OpenWeatherMap API key for live weather

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

## Setup (macOS / Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000

## Routes
- `/` — home
- `/register/` — farmer registration
- `/login/` — sign in
- `/dashboard/` — farmer dashboard
- `/farms/` — farm records
- `/soil/` — soil readings
- `/recommendations/` — rule-based crop suggestions
- `/weather/` — live weather when `OPENWEATHER_API_KEY` is set
- `/disease/` — image and symptom submission
- `/market/` — market price records
- `/control-room/` — custom admin dashboard (staff only)
- `/django-admin/` — Django's full admin CRUD

## Enable live weather
Set the environment variable before starting the server:
```bash
# macOS/Linux
export OPENWEATHER_API_KEY="your-key"

# Windows PowerShell
$env:OPENWEATHER_API_KEY="your-key"
```
Restart `runserver`. Weather lookup uses OpenWeatherMap current-weather endpoint.

## Admin use
Create a superuser using `python manage.py createsuperuser`, then log in at `/login/`. Staff users can access `/control-room/`; the superuser can also access `/django-admin/` to create/edit/delete crops, market prices, users, soil readings and reports.

## Important limitations / production checklist
- Market price rows seeded by `seed_demo` are explicitly sample values, not live mandi prices. Add a trusted data source such as AGMARKNET/e-NAM or a licensed provider before production.
- Crop suggestions are simple transparent rules, not a validated ML model. Confirm recommendations with local agricultural experts and region/season-specific data.
- Disease upload is a report workflow only. It does not identify disease. To add AI diagnosis, train/evaluate a model on labelled local crop images and add confidence thresholds and expert review.
- Soil readings are manually entered. Connect calibrated sensors using a secure authenticated device API before calling it IoT monitoring.
- Before deployment: set `DEBUG=0`, use a strong secret key, configure allowed hosts, HTTPS, secure cookies, backups, file-upload limits and a production database/web server. Add email verification, password reset, rate limiting, audit logs and privacy/consent controls.
