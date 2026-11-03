# What-if · Hook V3 · Qualitätsprüfung

Ergebnis: `WhatIf_Eine_Minute_Zukunft_Hook_v3_30s.mp4`.

V3 ergänzt die vorhandene Cartoon-Straßenhandlung um 14 gezielte Textmomente mit Manrope 800, maskierten Wort-Reveals, Unterstreichungen, bildbezogenen Fokusgrafiken und kurzen eigenen Soundakzenten. Die Stimme und die Handlung verwenden den bestehenden 30-Sekunden-Abschnitt. Die großen Texte lassen die Vorbeifahrt frei.

## Tatsächlich geprüft

| Prüfung | Ergebnis |
|---|---|
| TypeScript | bestanden |
| Remotion und Schriftpaket | 4.0.540, identische Versionen |
| Bild | 1920 × 1080, 16:9, H.264, yuv420p |
| Bildrate / Anzahl | 30 FPS / 900 Frames |
| Dauer Video, Audio, Container | jeweils 30,000 Sekunden |
| Ton | AAC, Stereo, 48 kHz |
| Vollständige Dekodierung | bestanden |
| Schwarze Frames | 0 |
| Gemessene Lautheit | -14.07 LUFS |
| Gemessener True Peak | -2.46 dBTP |
| Sprachkorrelation zum dekodierten Mix | 0.998857 |
| Dateigröße | 8,469,368 Bytes |
| SHA-256 | `9381d79435eeccfe06309f3f4c08c9b2b14325b788b40fa47536b29b3dd0f1e1` |

Die Sprachkorrelation prüft die vorhandene Aufnahme an ihrem ursprünglichen Zeitraster. Sie ist kein Ersatz für eine Hörprüfung. Die Quelle wurde nicht umgesprochen oder beschleunigt. Die neuen Effekte folgen den Text-Cues; sie werden unter der Sprache weich abgesenkt.

## Visuell betrachtet

Vor dem Export wurden 14 Grafik-Schlüsselmomente direkt in Remotion gerendert. Anschließend wurden Kontaktbögen aus der tatsächlichen finalen MP4 betrachtet: sämtliche 14 Textmomente, 30 dicht aufeinanderfolgende Anfangsbilder und 22 Bilder der Vorbeifahrt. Geprüft wurden Textgrenzen und Kontrast, freie Gesichter, maskierte Ein-/Ausgänge, Telefonklammern, grüne Ampel sowie der Pfeil zur Gefahrenstelle. Der Quellcode erzeugt zusätzlich einen Kontaktbogen über die gesamten 30 Sekunden, einen Schnittbogen und eine dichte Schrittfolge.

Der Viewer erlaubt Einzelbildbetrachtung. Eine vollständige kritische Echtzeitwiedergabe mit Hörkontrolle hat nicht stattgefunden. Der Bericht beansprucht daher technische Prüfung und visuelle Stichproben, keine abschließende Hörabnahme.

## Nachvollziehbare Dateien

- `cartoon-v2/src/graphics-v3/`: neue Text- und Grafikebene.
- `cartoon-v2/scripts/make_accents_v3.py`: lokale Erzeugung der zusätzlichen Sounds und des Mixes.
- `cartoon-v2/scripts/render_v3.sh`: Export und Prüfung.
- `cartoon-v2/docs/technical-v3.json`: Messwerte der kodierten Datei.
- `cartoon-v2/docs/audio-cues-v3.json`: Soundzeitpunkte und Mischpegel.
- `cartoon-v2/docs/V3_TEXT_UND_GRAFIK.md`: Gestaltung und Zeitplan.

Separate Audiospuren werden lokal aus der bereitgestellten Original-MP3 regeneriert; sie sind nicht Teil des GitHub-Quellcodes. Die fertige MP4 enthält den vollständigen gemischten Ton. V2 bleibt als eigene Komposition und Datei erhalten.
