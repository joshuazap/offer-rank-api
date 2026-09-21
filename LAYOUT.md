# Layout

```text
offer-rank-api/
├── app/
│   ├── main.py              # FastAPI app + CORS + startup seed
│   ├── config.py            # DATABASE_URL + ranking weights
│   ├── db.py                # SQLAlchemy engine/session
│   ├── models.py            # Consumer, Offer, Event
│   ├── schemas.py           # Pydantic response models
│   ├── seed.py              # Demo data (c_alex, c_blake, c_casey)
│   ├── api/routes.py        # HTTP endpoints
│   └── services/ranking.py  # Explainable score logic
├── frontend/index.html      # Minimal UI (swap for React later)
├── tests/test_ranking.py
├── Dockerfile
├── docker-compose.yml       # api + Postgres
├── requirements.txt
└── .github/workflows/smoke.yml
```

# Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness |
| GET | `/consumers` | List seed consumers |
| GET | `/offers` | List active offers |
| GET | `/consumers/{external_id}/recommendations?limit=5` | Ranked offers + reasons |

Try: `c_alex`, `c_blake`, `c_casey`.

# Resume bullet (paste after GitHub is public)

Built a FastAPI + React/HTML offer-ranking service (Docker Compose, Postgres) that scores personalized offers from consumer event signals; published OpenAPI at `/docs` and CI smoke tests.

# Upgrade path (optional, day 2)

1. Replace `frontend/index.html` with a Vite + React app using the same endpoints.
2. Add `POST /events` to ingest new signals.
3. Add JWT auth on write endpoints.
4. Cache rankings in Redis for hot consumers.
