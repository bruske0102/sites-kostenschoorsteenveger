# Kostenschoorsteenveger.nl — beginner go-live

1. **GitHub** — `bruske0102/sites-kostenschoorsteenveger` `main` has site at repo root (not monorepo).
2. **CF Worker Builds** — Worker name `kostenschoorsteenveger`, Root directory **empty**, `npm ci && npm run build`, `npx wrangler deploy`.
3. **Visit** — **Done** / **Live** — `https://kostenschoorsteenveger.nl/`
4. **Email Routing** — confirm `info@kostenschoorsteenveger.nl` (`playbook/CF_EMAIL_ROUTING.md`).
5. **Custom domain** — **Live** — `kostenschoorsteenveger.nl` (Thomas).
6. **GSC + Bing** — submit `https://kostenschoorsteenveger.nl/sitemap-index.xml`.

See also: [`GO_LIVE_NOW.md`](./GO_LIVE_NOW.md)

## Local

- Preview (agent): `http://127.0.0.1:43861/`
- Verify: `npm run verify:golive` (optional; needs running preview)
