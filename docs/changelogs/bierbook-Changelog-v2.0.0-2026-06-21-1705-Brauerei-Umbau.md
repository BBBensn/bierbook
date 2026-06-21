---
date_created: 2026-06-21 17:05:00
type: changelog
tags:
  - project
  - changelog
date_modified: 2026-06-21 17:05:00
---

# v2.0.0 — Brauerei als oberste Entität (2026-06-21)

Breaking Change: Datenmodell, API-Endpunkte und Frontend vollständig umgebaut.

## Datenmodell
- Tabelle `brands` → `breweries` (Brauerei als oberste Sammel-Entität)
- `bottles.brand_id` → `bottles.brewery_id`
- Neues Pflichtfeld `bottles.bezeichnung` (Produktname/Markenname auf dem Etikett, z.B. "Obertrumer Original")
- DB auf Server zurückgesetzt (nur Test-Eintrag vorhanden)

## API
- Alle `/api/brands/...` → `/api/breweries/...`
- `GET /api/breweries` — Brauerei-Liste
- `GET /api/breweries/autocomplete` — Autocomplete
- `GET /api/breweries/:id/bottles` — Brauerei-Detail + Flaschen
- `PUT /api/breweries/:id` — Brauerei bearbeiten
- `DELETE /api/breweries/:id` — Brauerei löschen (mit Schutzregel)
- `POST/PUT /api/bottles` — jetzt mit `brewery_name`, `brewery_country`, `bezeichnung`

## Frontend
- Grid-Karten: `bezeichnung` als Haupttitel, `brewery_name` als Sekundärinfo
- Flaschen-Detail: `bezeichnung` prominent, Brauerei als eigenes Feld
- Formular: Felder Brauerei (Autocomplete), Land, Bezeichnung/Marke, Stil, Notizen
- Tab "Marken" → "Brauereien", Route `brands` → `breweries`
- Brauerei-Detailansicht mit Bearbeiten/Löschen
- Suche durchsucht jetzt auch `bezeichnung`
