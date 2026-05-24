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
4. Run `python manage.py migrate` from `backend`.
5. Run `python manage.py runserver 0.0.0.0:8000`.

## Phone access

- This PC LAN IP: `192.168.0.8`
- Login screen on this PC: `http://127.0.0.1:8000/`
- App prototype on this PC: `http://127.0.0.1:8000/app/`
- Login screen on phone: `http://192.168.0.8:8000/`
- App prototype on phone: `http://192.168.0.8:8000/app/`
- Ops demo on phone: `http://192.168.0.8:8000/ops/`

Your iPhone and this PC must be on the same Wi-Fi network.
If Windows Firewall asks, allow Python on private networks.

## Demo UI

- Login screen: `http://127.0.0.1:8000/`
- App prototype: `http://127.0.0.1:8000/app/`
- Ops demo: `http://127.0.0.1:8000/ops/`
- Admin: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`

The root screen is a social login entry screen with Google, KakaoTalk, and Naver OAuth buttons.
OAuth credentials are configured with `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `KAKAO_OAUTH_CLIENT_ID`, `KAKAO_OAUTH_CLIENT_SECRET`, `NAVER_OAUTH_CLIENT_ID`, and `NAVER_OAUTH_CLIENT_SECRET`.
The app prototype lives at `/app/` for validating the end-user flow before OAuth credentials are ready.
The `/ops/` screen is the operations-oriented demo surface for manual API exercise.
