# Optional React UI (afternoon block)

## Goal

List consumers, fetch `GET /consumers/{id}/recommendations`, show ranked offers with scores and reasons.

## Fastest path (no Vite setup required)

Open `index.html` via any static server after the API is up:

```bash
# from frontend/
python -m http.server 5173
```

Then visit http://localhost:5173

## Endpoints used

- `GET /consumers`
- `GET /consumers/{external_id}/recommendations?limit=5`

CORS is already allowed for `http://localhost:5173`.
