---
date_created: 2026-06-21 17:28:00
type: changelog
tags:
  - project
  - changelog
date_modified: 2026-06-21 17:28:00
---

# v2.0.1 — Service Worker, JSON-Fehler, Emoji-Reduktion (2026-06-21)

## Fix: PWA zeigt nach Deploys alte Version

- Neuer Service Worker (`sw.js`) mit versioniertem Cache-Name `bierbook-v[VERSION]`
- `skipWaiting()` im install-Event → neuer SW wird sofort aktiv, ohne App-Neustart abzuwarten
- `clients.claim()` im activate-Event → neuer SW übernimmt sofort Kontrolle aller offenen Tabs
- Alte Caches werden im activate-Event automatisch gelöscht (`caches.keys()` → alle außer aktuellem)
- Fetch-Strategie: API-Anfragen nie cachen; Fotos Cache-first; App-Shell Network-first mit Cache-Fallback (Offline-Fähigkeit)
- nginx: `Cache-Control: no-store` für `/sw.js` selbst, damit der Browser immer die aktuelle SW-Version lädt
- SW-Registration in `index.html` ergänzt

## Fix: "Unexpected token <" auf Brauereien-Seite

- `apiFetch()` hat bei einer nicht-JSON-Antwort (z.B. HTML-Fehlerseite) unkontrolliert gecrasht
- Fix: try/catch um `r.json()` — bei Parse-Fehler wird jetzt `Server-Fehler (HTTP-Status)` geworfen statt Crash
- Alle Fehler-Zustände im UI zeigen saubere Fehlermeldung statt unbehandeltem JS-Fehler
- Grundursache war wahrscheinlich alter SW-Cache mit falschen Routes (durch Fix 1 behoben)

## UI: Emoji-Reduktion

- Alle dekorativen Emojis aus der gesamten App entfernt: Stil-Icons (🍺🌿🏴…), Länder-Flags (🇦🇹🇩🇪…), Platzhalter-Icons (🏭📦📷⚠️), Button-Icons (✏️🗑️), Header-Logo
- `styleIcon()`- und `flag()`-Funktionen entfernt
- Platzhalter-Divs zeigen nun nur den Gradient-Hintergrund (kein Emoji)
- Leere Zustände (Empty States) ohne Emoji-Icon, nur Text
- Ausnahmen: Favicon und App-Icon (🍺 auf Homescreen) bleiben unverändert
