# Feedback Platform

Python backend MVP scaffold for a semi-anonymous creative feedback platform.

## Stack

- Backend API: Django + Django REST framework
- Database: SQLite for local development, PostgreSQL in production
- Background jobs: Celery + Redis
- Mobile client target: SwiftUI iOS app

## Core product assumptions

- Creators upload works such as images, videos, audio, or illustrations.
- Reviewers leave qualitative feedback through comments.
- Public identity is semi-anonymous and limited to handle, gender, country, and age group.
- Moderation is a first-class feature from day one.

## Quick start

1. Install dependencies from `backend/requirements.txt`.
2. Confirm `.env` contains your local IP in `DJANGO_ALLOWED_HOSTS`.
3. Run `python manage.py migrate` from `backend`.
4. Run `python manage.py runserver 0.0.0.0:8000`.

## Phone access

- This PC LAN IP: `192.168.0.8`
- App prototype on this PC: `http://127.0.0.1:8000/`
- App prototype on phone: `http://192.168.0.8:8000/`
- Ops demo on phone: `http://192.168.0.8:8000/ops/`

Your iPhone and this PC must be on the same Wi-Fi network.
If Windows Firewall asks, allow Python on private networks.

## Demo UI

- App prototype: `http://127.0.0.1:8000/`
- Ops demo: `http://127.0.0.1:8000/ops/`
- Admin: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`

The root screen is a mobile-first app prototype for validating the end-user flow.
The `/ops/` screen is the operations-oriented demo surface for manual API exercise.
