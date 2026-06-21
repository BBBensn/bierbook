---
date_created: 2026-06-21 02:30:00
type: changelog
tags:
  - project
  - changelog
date_modified: 2026-06-21 02:30:00
---

# v1.0.1 — Toast-Fix, Marke löschen, Datum (2026-06-21)

- Fix: Toast-Notification bleibt nach Ausblenden nicht mehr unsichtbar im Rendering — opacity:0 + pointer-events:none im Basis-State statt nur translateY; opacity transition läuft parallel zur Transform-Animation
- Feature: Marke löschen in der Marken-Detailansicht — mit Schutzregel: Löschen nur möglich wenn keine Flaschen zugeordnet sind; bei Verstoß klare Fehlermeldung ("Marke hat noch X Flasche(n) — erst ändern oder löschen")
- Feature: Erstellungsdatum einer Flasche in der Detailansicht angezeigt ("Hinzugefügt: TT.MM.JJJJ")
