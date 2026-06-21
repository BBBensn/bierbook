---
date_created: 2026-06-21 02:17:00
type: changelog
tags:
  - project
  - changelog
date_modified: 2026-06-21 02:17:00
---

# v1.0.0 — MVP (2026-06-21)

- Flask + SQLite Backend mit drei Tabellen: brands, bottles, bottle_photos
- Zentrales db.py mit Context-Manager-Pattern für saubere Transaktionen
- Foto-Upload: EXIF-Rotation, RGB-Konvertierung, 400×400px JPEG-Thumbnails
- API-Endpunkte: Flaschen anlegen/bearbeiten/löschen, Marken-Autocomplete, Stil-Autocomplete
- Einzelfotos löschen via DELETE /api/photos/<id>
- Vanilla JS Single-Page-App (ein index.html, kein Build-Step)
- Mobile-first Design mit amber/cream Farbschema
- Grid-Ansicht aller Flaschen mit Thumbnail oder Style-Icon als Placeholder
- Markenansicht mit Flaschenzahl und Thumbnail
- Detailansicht: Fotogalerie (Original-Auflösung), alle Felder, Bearbeiten/Löschen
- Formular: Marken-Autocomplete mit Auto-Anlage, Stil-Autocomplete, Drag-&-Drop Foto-Upload
- Such-/Filterleiste: Freitext + Länder-Chips
- Hash-basiertes Routing (#grid, #brands, #bottle/:id, #brand/:id, #add, #edit/:id)
- Bierstil-Icons (Emoji) je nach Stilkategorie
- Länder-Flaggen aus Markenname/Ländereingabe
- Deployment auf bensn-server (CX23): gunicorn, systemd-Service bierbook.service auf Port 5005
- nginx-Reverse-Proxy mit SSL via certbot (https://bierbook.bensn.at)
- Uploads-Verzeichnis außerhalb des API-Roots, nginx served /uploads/ direkt
