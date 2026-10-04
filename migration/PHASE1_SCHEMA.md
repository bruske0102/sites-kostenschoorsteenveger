# Phase 1 — content schema (kostenschoorsteenveger.nl)

**Approved** with Phase 0 (same shape as other niches). Collection: `schoorsteenvegers`.

One JSON file per listing: `src/content/schoorsteenvegers/{provincie}--{plaats}--{slug}.json`

Fields follow the shared directory schema (naam, slug, provincie, plaats, adres, telefoon, website, status, kenmerken, …). See `scrape_listings.py` for writers.
