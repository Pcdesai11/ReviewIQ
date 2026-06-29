# ReviewIQ — Frontend

This is the dashboard UI for ReviewIQ. See the [project README](../README.md) and [`# ReviewIQ.ini`](../#%20ReviewIQ.ini) for architecture and roadmap.

## Stack

React 18 + TypeScript + Vite + Tailwind CSS + TanStack Query. The dashboard fetches live data from the ReviewIQ Results API (`src/api/client.ts`). Default API URL: `http://127.0.0.1:8001` — override with `VITE_API_URL` in `.env`.

## Run locally

```bash
# Terminal 1 — backend (from repo root)
cd backend
.\.venv\Scripts\uvicorn app.main:app --reload --port 8001

# Terminal 2 — frontend
npm install
npm run dev
```

## Build for production

```bash
npm run build
```

Outputs static files to `dist/`.

## Deploy

This is a static site — any static host works.

**Vercel**
```bash
npm i -g vercel
vercel
```
(Framework preset: Vite. No environment variables needed yet.)

**Netlify**
- Build command: `npm run build`
- Publish directory: `dist`

**GitHub Pages / any static host**
```bash
npm run build
# upload the contents of dist/
```

## Design system

- **Colors**: ivory background, navy/forest/brass as the three working accents, brick reserved only for genuine high-risk flags — see `tailwind.config.js`.
- **Type**: Fraunces (display), Inter (UI text), IBM Plex Mono (every number).
- **Pattern**: every list ends in a right-aligned monospace "balance column" (`src/components/ReviewSection.tsx`) — this is the one component to reuse for any new data type the backend adds.

## Next step

Add GitHub webhook ingest and LLM workers so the API serves real analysis instead of seeded demo data.
