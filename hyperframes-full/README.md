# Eine Minute voraus · vollständiger HyperFrames-Cartoonfilm

Ein 303 Sekunden langer, ausgespielter 2D-Cartoonfilm mit der vom Nutzer gelieferten Mark-Aufnahme. 22 verbundene Einstellungen, eigene Figursteuerung, 36 gezielte Textakzente, Musik und ortsbezogene Geräusche. Zukunftsblick, Tasse, Nachrichten und Café-Gespräch folgen derselben festgelegten Logik. Stil und Szenenplan stehen in `DESIGN.md` und `SPEC.md`.

Die Kompositionen werden tatsächlich durch **HyperFrames 0.9.12** mit GSAP und lokalen SVG/HTML-Assets gerendert. Der offizielle HyperFrames-Skill wurde angewandt. Der Marker-Baustein wurde über die Registry bezogen; seine SVG-Strichmechanik wurde für die Unterstreichungen in der eigenen Typografie übernommen. Die Ausgabe entsteht aus diesen HTML/SVG-Kompositionen im HyperFrames-Renderlauf.

## Vorschau und Bearbeitung

Node 22 oder neuer, FFmpeg/FFprobe und Chrome/headless-shell werden benötigt. Die hier geprüfte Umgebung verwendet Node 24.22.1, FFmpeg 7.1.5 und Chrome Headless Shell 158.0.8127.2. Die npm-Skripte pinnen HyperFrames 0.9.12.

```sh
npm run dev
npm run check
```

Im Cloud-Arbeitsbereich: `hyperframes preview --background --port 3210`; die Projektoberfläche ist `http://localhost:3210/#project/hyperframes-full`. Der Preview-Prozess muss nach einem Umgebungsneustart neu gestartet werden. `index.html` ist die Quelldatei, nicht der Vorschau-Link.

## Quelldateien

- `scripts/build_film.py`: erzeugt die einzeln bearbeitbaren Szenen und die Typografie aus den festgelegten Zeitpunkten.
- `assets/film-runtime.js`: SVG-Rig, Gelenke, Blick, Schritte, Greifaktionen, Kamera und Szenenbewegung.
- `compositions/`: 22 Szenen und die gemeinsame Typografiespur.
- `production/`: Wortzeiten, Szenen, Ton-Cues und technische Berichte.
- `assets/audio/CREDITS.md`: Musik- und Geräuschquellen sowie erforderliche Veröffentlichungshinweise.

`python3 scripts/build_film.py` überschreibt die generierten HTML-Dateien. Änderungen entweder direkt in HTML bearbeiten und den Generator danach nicht ausführen oder die entsprechenden Änderungen im Generator vornehmen.

## Lokale Toninputs

Die hochgeladene MP3 und die separaten WAV-Mischspuren werden nicht im öffentlichen GitHub-Zweig veröffentlicht. Zum erneuten vollständigen Rendern sind die lokalen Toninputs nötig. Die fertige MP4 enthält bereits alle Spuren.

`scripts/mix_audio.py` nimmt die neue Mark-MP3, die bereits vorhandene isolierte Absurditas-Foleyspur und den Ordner der HyperFrames-Bundle-Effekte entgegen. Die frühere Foleyspur enthält keine Sprache. Falls nötig kann sie mit `cartoon-v2/scripts/make_audio.py` und der damaligen Originalaufnahme neu erzeugt werden. Musik und Regen werden von den in den Credits verlinkten Primärquellen bezogen und unter den im Skript erwarteten Dateinamen in `assets/audio/` abgelegt. NumPy wird für die Mischung benötigt.

```sh
python3 scripts/mix_audio.py /pfad/Mark.mp3 /pfad/foley.wav /pfad/HyperFrames/audio/assets/sfx
```

Die Stimme wird in vollständiger Länge mit gleichem Tempo und gleicher Tonhöhe verarbeitet. Der Mix erhält sprachabhängige Absenkung der Musik und eine gemessene feste Pegelanpassung; am Ende wird Stille bis zur Bildlänge ergänzt.

## Export und Prüfung

```sh
npx --yes hyperframes@0.9.12 check --json
npx --yes hyperframes@0.9.12 snapshot --review
npx --yes hyperframes@0.9.12 render --fps 30 --quality high --workers 3 --output renders/captured-full.mp4
```

Der ausgelieferte Film wird anschließend mit dem kanonischen Mix als H.264/AAC-MP4 mit Faststart versehen und vollständig dekodiert. `scripts/qc_film.py` prüft Bildrate, Framezahl, Ton, Dauer, schwarze Frames und Stimme/Mix-Ausrichtung. Kontaktbögen kommen aus der tatsächlichen MP4. Die verwendeten Quellaufnahmen bleiben lokal; keine Audio-API erhält die Nutzerdatei.

Musikcredits beim Weiterveröffentlichen beibehalten. Pegelmessung und betrachtete Einzelbilder ersetzen keine kritische Echtzeit-Hörabnahme; die tatsächlichen Prüfschritte und verbleibenden Einschränkungen stehen im Qualitätsbericht.
