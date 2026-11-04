# Eine Minute voraus · Dynamic Edition

Die neue, vollständig erhaltene Mark-Aufnahme als 344 Sekunden langer 2D-Cartoonfilm. 1920 × 1080, 16:9, 30 FPS. 96 motivierte Einstellungen in acht Set-Kategorien; durchschnittlich 3,58 Sekunden pro Einstellung. Eigene SVG-Sets, eine gemeinsame Figursteuerung, animierte Schlüsseltexte, vier Musikabschnitte und 57 synchronisierte Effekte. HyperFrames 0.9.12 rendert die tatsächlichen HTML/SVG/GSAP-Kompositionen.

Die neuen Schauplätze zeigen Küche, Bahnsteig, Büro, Börsenbildschirm, Fußballübertragung, Kreuzung, Café und Abendessen. Der Körperkontakt mit Gegenständen, die Tiefenstaffelung beim Einsteigen, die Torentscheidung und die Beispielrechnung sind bewusst nachvollziehbar angelegt. DESIGN.md hält den Stil aus den Nutzerreferenzen fest.

## Projekt öffnen

Node 22 oder neuer, FFmpeg/FFprobe und Chrome werden benötigt. `npm run dev` startet die lokale Studio-Oberfläche. Für eine persistente Cloud-Vorschau:

```sh
npx --yes hyperframes@0.9.12 preview --background --port 3211
```

Projektoberfläche: `http://localhost:3211/#project/hyperframes-dynamic`. `index.html` ist Quelltext. Der Vorschau-Prozess muss nach einem Umgebungsneustart neu gestartet werden.

## Aufbau und Bearbeitung

- `scripts/build_film.py`: 96 Szenen, Wortanker, Kameras, Requisiten und Textakzente.
- `scripts/worlds.py` und `scripts/art.py`: ursprüngliche Cartoon-Grafiken und Schauplätze.
- `assets/actor-rig.js`: Gelenke, Füße, Arme und Mimik.
- `assets/stage.js`: seekbare Schauspielaktionen und Objektbewegungen.
- `production/alignment.json`: ausschließlich lokal bestimmte Wortzeiten der neuen MP3.
- `production/scenes.json`: konkrete Szenenzeiten und Perspektiven.
- `assets/audio/CREDITS.md`: Musik-/Geräuschquellen und Veröffentlichungshinweise.

`python3 scripts/build_film.py` erzeugt die HTML-Kompositionen neu. Änderungen am Generator vornehmen; direkte Änderungen am erzeugten HTML würden beim nächsten Build überschrieben.

## Audio

Die Nutzeraufnahme wird ohne Tempo- oder Tonhöhenänderung vollständig verarbeitet und am Ende auf Bildlänge aufgefüllt. Musik wird während der Sprache abgesenkt. Originale synthetische Geräusche sind als gestaltete Effekte dokumentiert, nicht als Naturaufnahmen. Musikcredits beim Weiterveröffentlichen beibehalten.

Die separate MP3 und alle WAV-Mischspuren bleiben lokal. Die öffentliche MP4 enthält den gesamten fertigen Mix. Ein erneuter Render mit Ton erfordert die lokalen Audioinputs; das ist keine vollständige Hörabnahme des Ergebnisses.

## Render und Prüfung

```sh
npm run check
npx --yes hyperframes@0.9.12 snapshot --review
npx --yes hyperframes@0.9.12 render --fps 30 --quality high --workers 4 --output renders/captured-full.mp4
bash scripts/finish_export.sh
```

NumPy, Pillow und faster-whisper werden von den Python-Hilfen verwendet; requirements.txt enthält die hier verwendeten Versionen. Der Export übernimmt den H.264-Bildstrom des HyperFrames-Renders unverändert und verbindet ihn mit dem kanonischen AAC-Tonmix in einer MP4 mit Faststart. `scripts/qc_film.py` dekodiert genau diese Enddatei, kontrolliert Dauer, Framezahl, schwarze Frames, Spitzenpegel, Lautheit und Stimme/Mix-Ausrichtung und extrahiert Prüfbilder aller Einstellungen.
