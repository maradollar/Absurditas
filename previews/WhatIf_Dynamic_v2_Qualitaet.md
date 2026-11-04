# Eine Minute voraus · Dynamic Edition · Prüfung der Enddatei

Datei: `WhatIf_Eine_Minute_Voraus_HyperFrames_Dynamic_v2_1080p.mp4`. Neuer vollständiger HyperFrames-Film zur am 4. November gelieferten Mark-Aufnahme. Die frühere Fassung bleibt erhalten.

## Inhalt und Tempo

96 motivierte Einstellungen in acht Set-Kategorien, durchschnittlich 3,58 Sekunden statt ungefähr 13,77 Sekunden in der vorigen Fassung. Der Schnitt wechselt zwischen Raumansicht, Reaktion, eigener Perspektive und Detail. Die neue Aufnahme bleibt vollständig und läuft in Originalgeschwindigkeit und Originaltonhöhe. Musik: vier Abschnitte aus drei lizenzierten Titeln. 57 synchronisierte Effekt-Ereignisse; nicht jeder Schnitt erhält einen Whoosh.

## Gemessene fertige MP4

| Prüfung | Ergebnis |
|---|---|
| Dauer | 344.000000 Sekunden |
| Bild | 1920 × 1080, 16:9, H.264, yuv420p |
| Bildrate / Frames | 30 FPS / 10320 |
| Ton | AAC Stereo, 48 kHz |
| Vollständige Dekodierung | bestanden |
| Schwarze Frames | 0 |
| Lautheit | -14.53 LUFS |
| True Peak | -2.40 dBTP |
| Stimme/Mix-Korrelation ohne Zeitversatz | 0.992236 |
| Aus der Enddatei extrahierte Prüfbilder | 636 |
| Dateigröße | 80,258,998 Bytes |
| SHA-256 | `f9140e5ea3c7369f0cda14118f1845c042465d94fd0dd0a3424772e2156cc61b` |

## Tatsächlich durchgeführte Korrekturen

Vor dem Render wurden alle 96 Einstellungen anhand von HyperFrames-Bildserien betrachtet. Anschließend wurden kritische Bewegungen separat erneut geprüft. Korrigiert wurden die unterstützte Selektor-Schreibweise, die genaue Audio-Samplerate vor dem Auffüllen, die Tiefenstaffelung und Beinbewegung beim Einstieg, der sichtbare Griff am großen Smartphone, die Lage des Telefons auf dem Tisch sowie das sichtbare Smartphone beim Einstecken. Zukunftsszenen zeigen eigene Arme und Hände anstelle eines Blicks auf das eigene Gesicht. Die Armbanduhr hängt am sichtbaren, bis zum Bildrand fortgesetzten Ärmel.

Die Börsenanzeige vor dem Kauf wurde auf 100,00 € korrigiert; der Vorausblick zeigt 101,28 €. Die Beispielrechnung lautet 12,80 € − 2,90 € − 1,40 € = 8,50 €. Fußballspieler bleiben nach der Prüfung an ihren Positionen; der Ball überschreitet die Torlinie. Nach der Aberkennung steht es wieder 0:0, und die dargestellte Nächstes-Tor-Wette bleibt offen. Der kleine Radfahrer hat einen vollständigen Körper und ein vollständiges Fahrrad. Die Gegenaufnahme des Anrufs zeigt den Freund in seinem eigenen Raum. Die genaue Erzähl- und Zukunftslogik steht in `production/STORY_LOGIC.md`.

Die gerenderten Quellen wurden vor dem vollständigen HyperFrames-Lauf gehasht. Die Hashes wurden vor der Auslieferung erneut mit den Quelldateien verglichen.

Die vier Kontaktbögen aller 96 Einstellungen wurden aus der tatsächlich ausgelieferten MP4 betrachtet. Zusätzlich wurden die dichten Bildserien für Tasse, Einstieg, Tor/Videoassistent, Einstecken des Handys und Anruf geprüft. Die korrigierten Kontakte und Zustandswechsel sind darin vorhanden; Text und wichtige Handlungen bleiben in diesen geprüften Bildern lesbar. Die kurzen Doppelbilder innerhalb der 0,22-sekündigen Übergänge gehören zur Überblendung. Der ursprüngliche HyperFrames-Bildstrom wird ohne erneute verlustbehaftete Videokomprimierung übernommen und mit dem kanonischen Tonmix verbunden.

## Check-Hinweise

Der vollständige HyperFrames-Check hat keine Fehler in Lint, Laufzeit, Layout, Bewegung, Kontrast oder Audio. Verbleibende Warnungsarten: `{'dead_stretch': 30, 'line_unread': 2}`. Die Ruhephasen-Heuristik sieht die über GSAP-Objektparameter aktualisierte SVG-Geometrie des Rigs nicht vollständig. `production/encoded-motion.json` misst deshalb tatsächliche aufeinanderfolgende Bilder aller 96 Einstellungen. Kurze Reaktions- und Lesepausen sind Teil des Schnitts. Wiederkehrende Zukunftslabels werden bereits im Hook eingeführt. Die Layout-Infos im Schluss entstehen in der 0,22-sekündigen Überblendung zweier Einstellungen mit derselben Credit-Zeile und wechselnden Überschriften; die Bilder wurden dafür geprüft.

## Grenzen und Quellen

Die Enddatei wurde vollständig technisch dekodiert, der Ton gemessen und die Schlüsselbilder visuell geprüft. Keine vollständige kritische Echtzeit-Hörabnahme wird behauptet. Das ist keine Garantie für jede einzelne gestalterische Entscheidung.

Musik von Kevin MacLeod: The Descent, Carefree, Dream Culture; incompetech.com, CC BY 4.0. Titel, Lizenzlink und Bearbeitung stehen im Film, in seinen Metadaten und in `assets/audio/CREDITS.md`. Hinzu kommen originale Absurditas-Fahrzeuggeräusche, originale gestaltete Foley-Effekte und HyperFrames/Pixabay-Übergangs-/UI-Geräusche. Die gestalteten Effekte werden nicht als Naturaufnahmen ausgegeben. Credits beim Weiterveröffentlichen beibehalten.

Die öffentliche Quelldatei enthält weder die separate hochgeladene MP3 noch WAV-Mischspuren. Die fertige MP4 enthält den vollständigen Ton. Die Aufnahme wurde zur lokalen Ausrichtung nicht an eine Transkriptions-API hochgeladen.
