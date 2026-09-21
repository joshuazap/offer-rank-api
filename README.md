# Offer Rank API

Personal FastAPI project: rank personalized consumer offers from simple event signals.

Built to demonstrate the ConvergeCONSUMER-adjacent stack: **FastAPI + Postgres + Docker + React**.

## Quick start

```bash
docker compose up --build
```

- API: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Optional React UI: see `frontend/README.md`

Local (without Docker; Python 3.11 or 3.12):

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Uses SQLite by default when `DATABASE_URL` is unset. Docker Compose sets Postgres.

## 1-day build plan

| Block | Time | Done when |
|-------|------|-----------|
| Morning | 2–3h | `docker compose up` works; `/docs` shows endpoints; seed data loads |
| Midday | 2h | Ranking logic uses events; add one test for rank order |
| Afternoon | 2h | Minimal React list + detail page calling the API |
| Close | 1h | README screenshots, push to GitHub, add resume bullet |

## Resume bullet (after you ship)

> Built a FastAPI + React offer-ranking service (Docker Compose, Postgres) that scores personalized offers from consumer event signals; published OpenAPI contracts and CI smoke tests.

## Interview talking points

1. Why FastAPI: typed request/response models, auto OpenAPI, async-ready.
2. Ranking is intentionally simple (explainable weights), not a black-box model.
3. Docker Compose mirrors how you ship API + DB together.
4. Next hardening step you would add: auth, caching, observability, A/B of weight configs.

## Repository

https://github.com/joshuazap/offer-rank-api
