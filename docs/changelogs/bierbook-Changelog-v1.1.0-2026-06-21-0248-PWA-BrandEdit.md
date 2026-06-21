---
date_created: 2026-06-21 02:48:00
type: changelog
tags:
  - project
  - changelog
date_modified: 2026-06-21 02:48:00
---

# v1.1.0 — PWA-Fix, Marke bearbeiten, App-Icon (2026-06-21)

- Fix: PWA Standalone-Modus — Header und Tab-Bar kaputt durch fehlende Safe-Area-Behandlung; behoben mit `padding-top: env(safe-area-inset-top)` auf `<header>` und `padding-bottom: calc(10px + env(safe-area-inset-bottom))` auf Bottom-Nav; `height:100%` auf Nav-Buttons entfernt (war ursächlich für zu große Tab-Bar im Standalone-Modus)
- Fix: Toast-Position berücksichtigt jetzt `env(safe-area-inset-bottom)` — verschwindet nicht hinter der Home-Leiste
- Feature: Marke bearbeiten — Bearbeiten-Button in der Marken-Detailansicht, eigenes Formular (#brand-edit/:id), Backend-Endpunkt PUT /api/brands/:id mit Duplikat-Schutz
- Feature: App-Icon für PWA/Homescreen-Installation — 512×512, 192×192 (manifest.json) und 180×180 (apple-touch-icon.png), 🍺-Emoji auf orangem Hintergrund
- Feature: manifest.json mit name, short_name, theme_color, display:standalone
- Konsistenz: Bearbeiten-Buttons überall in Orange (btn-primary statt btn-outline), Löschen-Buttons in Rot (btn-danger) — Flasche und Marke konsistent
