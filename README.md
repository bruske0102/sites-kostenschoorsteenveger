# Kostenschoorsteenveger.nl (Astro)

Dutch psychologist / practice directory — Django-overzicht family, scaffolded from basisschool-gids and scrubbed for schoorsteenvegers.

## Run

```bash
cd sites/kostenschoorsteenveger
npm install
npm run dev
```

Dev server: [http://127.0.0.1:43861](http://127.0.0.1:43861)

## Build

```bash
npm run build
npm run preview
```

## Data

- `src/content/schoorsteenvegers/*.json` — scraped + triage (separate scrape process)
- `src/data/cities.json` — Group A stub (Semrush NL volumes TBD)
- `src/lib/city-intents.ts` — titles/descriptions + city H2 stubs (fill after Semrush)
- `migration/semrush/` — place NL exports here (do not reuse basisschool/keramiek CSVs)
- `migration/assets/heroes/` — city heroes (synced to `public/heroes` on prebuild)

**Scrape vs Semrush:** scrape = listing inventory on the live site; Semrush = KD + volume for keywords/cities.

## Design

Blue CSS tokens (porcelain + cobalt) in `src/styles/global.css`. Brand mark: **Zwembad**`1`**.nl**. See `migration/design/`.

## Hosting

GitHub: `bruske0102/sites-kostenschoorsteenveger` (site-only push at repo root). Worker name: `kostenschoorsteenveger`.  
CF **Root directory = empty**. See `migration/GO_LIVE_NOW.md` for CF Worker + Builds, Email Routing, domain, GSC+Bing.

## Locked decisions

See `migration/DECISIONS.md` — brand Kostenschoorsteenveger.nl, schoorsteenvegers only (no coaches/lifestyle junk), SBO-equivalent N/A.
