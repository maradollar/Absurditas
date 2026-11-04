# Produktionsspezifikation · Eine Minute voraus

Die vom Nutzer gelieferte Mark-Aufnahme ist die Uhr. Quelle: 302,132188 s, Mono 44,1 kHz, SHA-256 `d54ed8be995d71499cfd792b74270e03743a26c5a00c287bd1e6ab546c62d893`. Kein Tempo- oder Tonhöhenwechsel. Nachlauf bis 303,000 s; 9090 Frames bei 30 FPS. Ausgabe 1920 × 1080, 16:9, H.264/AAC, 48 kHz Stereo.

## Ausgewählte Geschichte

Der Blick rettet die Hauptfigur an der Ampel, erleichtert zunächst ihren Alltag und wird im Gespräch mit ihrem Freund zum Problem. Die Auflösung ist eine andere Entscheidung im gegenwärtigen Moment. Der Nutzer hat diese Sprecherfassung aufgenommen; diese Geschichte und ihre Reihenfolge sind damit die Produktionsgrundlage. Es werden keine neuen Erzählertexte erfunden.

## Weltregeln und Logik

- Ein Blick zeigt einen subjektiven möglichen Zustand genau 60 Sekunden nach dem gegenwärtigen Moment. Nur eigene Wahrnehmungen sind zugänglich.
- Andere Entscheidungen können den gesehenen Verlauf verändern. Eine Vision ermöglicht keine weitere Vision; wiederholtes Auslösen verlängert den Horizont nicht.
- Der Hook enthält eine Zeitellipse im Warten bei Rot. Fiktive Ereigniszeit: erster Blick T=0, Grün ungefähr T=56, möglicher Schritt T=58, Fahrzeug/Unfall ungefähr T=60. Die Filmzeit ist kürzer als diese erzählte Minute; kein Countdown behauptet Echtzeit.
- Die Füße der Hauptfigur bleiben im tatsächlichen Verlauf hinter dem Bordstein. Nur die angehobene Schrittvorbereitung reicht kurz in die Luft über den Rand; der Fuß wird auf dem Gehweg abgesetzt. Fahrzeugbahn liegt auf der Straße und hinter der Figur.
- Zukunftsbilder werden mit einem kurzen Übergang, einer kühlen Wahrnehmungsnuance und der wiederkehrenden Kennzeichnung „VORAUSBLICK +60 SEKUNDEN“ eingeführt. Rückkehr stellt den tatsächlichen Zustand wieder her.
- Die Tasse wird vom vorderen Tischrand nach innen bewegt, bevor das Tablett den leeren Unterteller streift. Die verschobene Tasse liegt hinter der Tablettbahn.
- Die Nachricht ist vor den Vorausblicken ein noch nicht versendeter Entwurf. Die tatsächliche Sendung erfolgt erst um 190,08 s. Die vorher sichtbaren Antworten gehören zu gekennzeichneten Visionen.
- Der Abschied des Freundes ist eine Vision. Nach der Rückkehr sitzt er wieder; Aufmerksamkeit und Entschuldigung ändern den folgenden Verlauf.

## Bild und Bewegung

Die Palette, Schrift, Figurenidentität und Ausschlüsse stehen in `DESIGN.md`. Eine gemeinsame deterministische SVG-Figurensteuerung versorgt die 22 gespielten Szenen. Füße, Knie, Schultern, Ellbogen, Hände, Kopf, Augen und Mund haben eigene Geometrie. Gangphasen werden aus der zurückgelegten Entfernung berechnet; Standfüße halten während ihrer Stützphase. Greifaktionen und Gegenstände sind auf dieselben Zielpunkte und Zeitkurven abgestimmt.

Der sitzende Körper endet an der Sitzfläche. Aufstehen hebt zuerst den Oberkörper; danach beginnt das Gehen. Das Tablett und sein tragender Arm haben dieselbe Höhe. Das Handy verdeckt die haltende Hand teilweise, überlappt aber keine Tasse. Regen wird durch einen festen Bereich außerhalb der Markise begrenzt. Schrift auf Nachrichten ist gesetzt, nicht bildgeneriert.

Die Hauptübergänge sind Crossfades von 0,34 s mit geringen Abständen zur vorherigen Einstellung; die ersten Wahrnehmungsschnitte verwenden 0,18 s. Eingang, Kamera, Blick und Geste werden versetzt geführt. Ruhe nach einer Entscheidung ist beabsichtigt; sie enthält weiterhin Atmung, Blinzeln und Blickbewegungen. Die 36 kurzen Textakzente teilen eine eigene HyperFrames-Komposition; sie ersetzen nicht die Handlung.

## Zeitplan

Der tatsächliche Szenenplan steht maschinenlesbar in `production/scenes.json`, die Akzente in `production/text-cues.json` und die lokal ermittelten Wortzeitpunkte in `production/alignment.json`. Maßgeblich sind die exportierten Bilder und die unveränderte Aufnahme; Erkennungstext ist kein neuer Sprechertext.

## Ton

Drei lizenzierte Musikausschnitte: Spannung unter Hook/Regeln, hellere Alltagsphase, ruhigeres Piano unter dem Beziehungsteil. Die Frage des Freundes und die Entschuldigung erhalten zusätzliche Absenkungen. Reifen, Vorbeifahrt, Fuß, Stoff/Telefon, Regen, Wahrnehmungswechsel und Nachrichten-/Abo-Akzente werden an sichtbare Ursachen gebunden. Unpassende Suchtreffer wurden nicht eingesetzt: ein gefundener melodischer Ton ist kein Regen, ein UI-Klick ist kein Laufgeräusch.

Die Aufnahme bleibt vollständig. Der letzte gesprochene Satz endet etwa bei 301,60 s; der Ton und das Bild haben bis 303 s Ausklang. Musikcredits stehen im Schlussbild, in Dateimetadaten und in `assets/audio/CREDITS.md`. Musik-/Effektdateien und die Originalstimme bleiben lokale Inputs; öffentlich geliefert wird der vollständige gemischte Film.

## Prüfgrenzen

HyperFrames `check`, tatsächliche PNG-Betrachtung, dichte Kontaktprüfungen der Bewegungen und technische Analyse der kodierten MP4 sind erforderlich. Ein Algorithmus, der nur CSS-Tweens misst, kann die über GSAP-Objektparameter gezeichneten SVG-Bewegungen als Stillstand melden; solche Warnungen werden gegen echte Bildfolgen geprüft und dokumentiert. Eine technische Pegelmessung wird nicht als kritisches Anhören ausgegeben.
