# ChainScope Project Important Info & API Keys

This document contains all the external API endpoints, keys, and important data URLs extracted from the ChainScope project.

## API Keys

### Maptiler API
- **Primary Key** (used in `index.html`): `wzYbF8hXDKBEhoG9HnCW`
- **Alternate Key** (found in `rewrite.py`/`fix.py` backups): `AVA08bxnKmJ3Pbc4DBA7`
- **Map Style Endpoint**: `https://api.maptiler.com/maps/darkmatter/style.json?key=<YOUR_KEY>`

## Important Services & External Endpoints

### 1. Cloudflare Worker (Live Ship Tracking)
- **Worker URL**: `https://delicate-recipe-b1b3.quantumfaizan.workers.dev/`
- **Purpose**: Acts as a proxy or service to fetch real-time ship locations, speed, and destination details.

### 2. World Bank API (Live Commodity Prices)
These endpoints are used to fetch real-time macroeconomic indicators for the dashboard:
- **Iron Ore**: `https://api.worldbank.org/v2/en/indicator/PIORECR.MT?format=json&mrv=1&per_page=1`
- **Coal AUS**: `https://api.worldbank.org/v2/en/indicator/PCOALAU.MT?format=json&mrv=1&per_page=1`
- **Brent Crude**: `https://api.worldbank.org/v2/en/indicator/POILBRE.USD?format=json&mrv=1&per_page=1`
- **Nat Gas**: `https://api.worldbank.org/v2/en/indicator/PNGASUS.USD?format=json&mrv=1&per_page=1`

### 3. BBC RSS Feed & CORS Proxy (Live News)
- **News Source RSS**: `https://feeds.bbci.co.uk/news/world/rss.xml`
- **CORS Proxy**: `https://api.allorigins.win/get?url=`
- **Usage**: The app fetches the BBC RSS feed via the `allorigins` proxy to bypass browser CORS restrictions and parses the XML to find matching keywords like (`ship`, `cargo`, `supply`, `trade`, `sanctions`, `oil`).

## External Assets / libraries
- **Fonts**: Space Mono, Inter (`https://fonts.googleapis.com/css2`)
- **Map Engine**: MapLibre GL JS v3.6.2 (`https://cdn.jsdelivr.net/npm/maplibre-gl@3.6.2/dist/maplibre-gl.js`)
