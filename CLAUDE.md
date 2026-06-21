---
date_created: 2026-05-05 16:49:24
date_modified: 2026-06-21 01:30:08
---

# BierBook — CLAUDE.md

Projekt-spezifischer Kontext. Ergänzt `~/.claude/CLAUDE.md`. Ablageort: `~/Documents/Coding/BierBook/CLAUDE.md`

---

## Projekt-Basics

- **Name:** BierBook
- **Domain:** bierbook.bensn.at
- **Version:** v1.0.1 ✅ deployed 2026-06-21
- **Status:** active
- **Stack:** Vanilla JS + Flask + SQLite

---

## Hintergrund & Zweck

Katalogisierungs-App für die Bierflaschensammlung meines Vaters (möglichst obskure Marken). Einziger Nutzer: mein Vater, hauptsächlich am Handy. Offline-Fähigkeit bewusst nicht in v1.0.0 — kann bei Bedarf später nachgerüstet werden.

---

## Datenmodell

**brands** (Marke/Brauerei)

- `id`
- `name` (unique)
- `country` (optional — Land/Region ist Eigenschaft der Marke, nicht der einzelnen Flasche)
- `created_at`

**bottles** (Flasche)

- `id`
- `brand_id` (FK → brands)
- `style` (optional, z.B. "Pils", "IPA")
- `notes` (Notizen/Bewertung, freitext)
- `created_at`

**bottle_photos** (Fotos pro Flasche)

- `id`
- `bottle_id` (FK → bottles)
- `filename`
- `created_at`
- Beziehung 1:n — mehrere Fotos pro Flasche möglich, kein Pflichtfoto (Platzhalterbild im Frontend, wenn keine Fotos vorhanden)

**Marken-Handling:** Keine separate Verwaltungsoberfläche für Marken. Beim Anlegen einer Flasche wird der Markenname per Autocomplete vorgeschlagen (bestehende Marken); existiert die Marke noch nicht, wird sie automatisch beim Speichern angelegt.

---

## Funktionsumfang v1.0.0

- Flasche anlegen: Marke (Autocomplete + Auto-Anlage), Stil (optional), Notizen/Bewertung, 0–n Fotos
- Grid-/Karten-Ansicht aller Flaschen (Platzhalterbild ohne Foto)
- Such-/Filterleiste: nach Marke, Stil, Land — von Anfang an wichtig, kein Nachrüsten
- Markenansicht: alle Varianten/Flaschen einer Marke gruppiert
- Detailansicht einer Flasche: alle Felder + Fotos, bearbeiten/löschen
- Design: etwas Liebe zum Detail gewünscht (z.B. Bierstil-Icons, ansprechende Grid-/Karten-Ansicht) — kein reines Funktions-Minimum

---

## Lokale Struktur

```
~/Documents/Coding/BierBook/
├── frontend/
│   └── index.html
├── backend/
│   ├── app.py
│   ├── db.py
│   └── uploads/            ← hochgeladene Fotos (lokal vor Deploy)
├── docs/
│   └── changelogs/         ← Claude Code schreibt Changelogs hierher
├── CLAUDE.md
└── .gitignore
```

---

## Remote-Struktur

```
/var/www/bierbook/
├── public/                 ← Frontend
├── api/                    ← Backend
└── uploads/                ← Fotos (Original + ggf. Thumbnails)
```

---

## Services & Ports

|Dienst|Port|systemd-Service|
|---|---|---|
|BierBook-Backend|5005|`bierbook.service`|

---

## Deploy

```bash
# Frontend
scp ~/Documents/Coding/BierBook/frontend/index.html \
  bensn:/var/www/bierbook/public/index.html

# Backend
scp ~/Documents/Coding/BierBook/backend/app.py \
  bensn:/var/www/bierbook/api/app.py
ssh bensn systemctl restart bierbook
```

---

## Git

- **Repo:** `https://github.com/BBBensn/bierbook`
- **Remote:** `git remote add origin git@github.com:BBBensn/bierbook.git`

```bash
# Typischer Commit nach Version
git add .
git commit -m "Add [feature]"
git push origin main
```

---

## Auth

- [ ] Auth via `auth.bensn.me` (nginx `auth_request`)
- [x] Öffentlich — kein Auth

Begründung: Einziger Nutzer (Vater), keine sensiblen Daten (Bierfotos/Notizen), eigener Service ohne Zugriff auf andere bensn-hub-Komponenten oder Secrets — fehlende Auth wirkt sich nicht auf die Sicherheit des restlichen Systems aus. Kein direkter DB-Zugriff von außen, nur über die API.

---

## Projekt-spezifische Konventionen

- API-Responses: `{success, data, error}`
- DB-Zugriffe nur über `db.py`
- Bilder serverseitig mit Thumbnail-Generierung speichern (schnelles Grid-Laden auf dem Handy)
- Land/Region hängt an `brands`, nicht an `bottles`

---

## Roadmap

|Version|Feature|Status|
|---|---|---|
|v1.0.0|MVP: Flaschen anlegen/anzeigen, Marken-Autocomplete, Fotos, Suche/Filter, Markenansicht|✅ done|
|v1.1.0|Offline-Fähigkeit (PWA, Service Worker, lokale Queue)|geplant|

---

## Obsidian-Doku

- Projekt-MD: `03_Projects/Coding PC/BierBook/BierBook.md`
- Changelogs: `03_Projects/Coding PC/BierBook/Changelogs/`
- Changelog-All: `03_Projects/Coding PC/BierBook/BierBook-Changelog-All.md`