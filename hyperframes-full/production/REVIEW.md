# What-if · vollständiger HyperFrames-Film · Qualitätsbericht

Datei: `WhatIf_Eine_Minute_Voraus_HyperFrames_1080p.mp4`. Der vollständige Film wurde mit HyperFrames 0.9.12 aus HTML/SVG-Kompositionen und GSAP gerendert. Die neue Mark-Aufnahme ist vollständig enthalten; Tempo und Tonhöhe bleiben erhalten. Musik, Regen, Fahrzeug- und Übergangseffekte sind im ausgelieferten Film gemischt. Der Abo-Aufruf gehört zur aufgenommenen Schlusszeile und zur Animation.

## Gemessene Enddatei

| Prüfung | Ergebnis |
|---|---|
| Dauer | 303.000000 Sekunden |
| Bild | 1920 × 1080, 16:9, H.264, yuv420p |
| Bildrate / Frames | 30 FPS / 9090 |
| Audio | AAC, Stereo, 48 kHz |
| Vollständige Dekodierung | bestanden |
| Schwarze Frames | 0 |
| Gemessene Lautheit | -14.52 LUFS |
| Gemessener True Peak | -2.06 dBTP |
| Stimme / dekodierter Mix bei gleichem Zeitraster | Korrelation 0.997530 |
| Extrahierte Prüfbilder | 328 |
| Dateigröße | 91,523,607 Bytes |
| SHA-256 | `433575419604bf81c3f48e35bccd1dacefa0c768dd9062a89a51d7657e0df364` |

## Tatsächlich angesehen und korrigiert

Vor dem Vollfilm wurden mehrere HyperFrames-Bildserien aller Schauplätze und ein tatsächlich kodierter 40-Sekunden-Hook geprüft. Dabei wurden die Standbeine, die Sitzflächen, der Griff am Handy und an der Tasse, der Abstand zwischen Handy und Tasse, die Tiefenstaffelung des Kellners, der Regenbereich außerhalb der Markise sowie überlagernde Dialog- und Nahaufnahme-Texte korrigiert. Die Frage des Freundes, sein Aufstehen/Gehen, die Entschuldigung, das Senden der Nachricht und der Abo-Text wurden an die lokalen Wortzeitpunkte angepasst.

Die korrigierte Handy-Nahaufnahme wurde anschließend erneut betrachtet. Die Kompositionsstände wurden vor den Renderläufen gehasht. Zwei Regel-Einstellungen wurden anschließend mit HyperFrames erneut gerendert, um die Nebenfigur eindeutig auf den Gehweg zu setzen. Der Vergleich bestätigt: Nur diese beiden Kompositionen änderten sich; die übrigen Kompositionen sind bytegleich. Die Korrektur wurde über den vollständigen Szenenbereich einschließlich der Übergänge bildgenau eingesetzt. Kontaktbögen aus der tatsächlichen Enddatei decken den ganzen Film sowie Schritt/Vorbeifahrt, Tasse/Tablett, Abschiedsvision und Handy/Entschuldigung ab. Die Kontaktbögen der Enddatei wurden anschließend tatsächlich betrachtet: Gesamtverlauf und Hook, Tassenbewegung und Vorbeigehen des Kellners, Aufstehen und Abschied des Freundes sowie Ablegen des Handys und Entschuldigung. Die zwei korrigierten Regel-Einstellungen zeigen beide Figuren auf dem Gehweg. In diesen geprüften Schlüsselbildern sind die relevanten Handlungen lesbar, die Gesichter bleiben von den Textakzenten frei, und der Abo-Aufruf ist im Schlussbild vorhanden. Eine vollständige kritische Echtzeit-Hörabnahme ist damit nicht verbunden.

## HyperFrames-Check und Warnungen

`production/hyperframes-check.json` enthält den vollständigen Check. Laufzeit, Layout, Bewegung und Kontrast haben keine Fehler. Die Typografiespur enthält bewusst alle 36 global zur Aufnahme synchronisierten Akzente in einer eigenen Komposition; die Warnung zur Dichte der Spur ist eine Quellcode-Struktur-Empfehlung.

Die Gestaltungsheuristik markiert 22 Abschnitte als mögliche Ruhephasen. Das Rig animiert SVG-Geometrie über GSAP-Objektparameter; diese Änderungen erscheinen nicht als gewöhnliche CSS-Tweens. Die Meldung „nothing changes“ ist daher kein Nachweis eines eingefrorenen Bilds. `production/motion-warning-review.json` vergleicht dazu echte, aus dem kodierten Film extrahierte Bilder. Bewusste Reaktions- und Lesepausen bleiben Teil des Films.

Sechs weitere Hinweise betreffen die kurze erneute Einblendung der bereits eingeführten Kennzeichnung „VORAUSBLICK +60 SEKUNDEN“. Diese ist ein wiederkehrender Zustandsmarker; sie führt bei späteren kurzen Blicken keinen neuen Lesetext ein. Die letzte solche Einblendung um 270 s ist nicht die Schlusszeile des Films. Der eigentliche Schluss und Abo-Aufruf bleiben bis 303 s sichtbar.

## Grenzen der Prüfung

Die Datei wurde vollständig technisch dekodiert, der Ton gemessen und die Schlüsselbilder wurden visuell betrachtet. Die Sprachkorrelation dient der Ausrichtungsprüfung. Es wurde keine vollständige kritische Echtzeitwiedergabe mit Hörabnahme durchgeführt; eine solche wird hier nicht behauptet. Die Bewertungen sind keine Garantie, dass jede gestalterische Entscheidung dem persönlichen Geschmack entspricht.

## Musik und Quellen

The Descent, Carefree und Dream Culture von Kevin MacLeod (incompetech.com), CC BY 4.0, mit Ausschnitten, Blenden und Pegelanpassung. Zuordnung und Lizenz stehen auch im Film und in seinen Metadaten. Weitere Quellen: CC0-Regenaufnahme von Wikimedia Commons, HyperFrames/Pixabay-Übergangs- und UI-Effekte sowie bestehendes originales Absurditas-Foley. Details: `hyperframes-full/assets/audio/CREDITS.md`.

Der öffentliche Quellstand enthält keine separate hochgeladene MP3 und keine WAV-Mischspuren. Die fertige MP4 enthält den vollständigen gemischten Ton. Frühere Vorschauen sind erhalten.
