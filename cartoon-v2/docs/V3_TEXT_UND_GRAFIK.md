# V3 · Text und Grafik im Hook

Neueste Vorgabe: „mehr grafiken gerade im hook oder visuals die das gesagte betonen, nutze bold text und smoothe animation mit text animations und sounds“.

## Gestaltung

Die durchgehend ausgespielte V2-Straßenhandlung und die ersten 30 Sekunden der bereitgestellten ElevenLabs-Stimme bilden weiterhin die Grundlage. V3 legt gezielte typografische Akzente über diese Handlung. Manrope 800 wird aus der mitgelieferten lokalen Datei mit `@remotion/fonts` vor dem Rendern geladen. Cremeweiß, warmes Gelb und Grün greifen den Cartoon-Look auf; dunkle Konturen halten den Text über der Kulisse lesbar.

Wörter steigen mit einem maskierten, gedämpften Reveal ein. Ihre Einsätze folgen den bereits lokal ermittelten Wortzeitpunkten. Unterstreichungen zeichnen sich anschließend; die Texte gleiten kurz aus. Alle Bewegungen hängen vom Remotion-Frame ab, ohne CSS-Animation, Zufall im Browser oder Echtzeittimer.

Die Texte stehen überwiegend im freien oberen Bildbereich und zum Schluss links neben der größer werdenden Figur. Während des eigentlichen Passierens der Kreuzung ist der Bildraum von großen Texten frei.

| Zeitraum | Akzent | Zusätzliche Grafik |
|---|---|---|
| 0,58–1,43 s | EINE AMPEL. | Gezeichnete Unterstreichung |
| 1,48–2,65 s | PLÖTZLICH. | Kurzer Strahlenimpuls neben dem Text |
| 2,80–4,28 s | AUF DEM ASPHALT. | Unterstreichung |
| 5,34–6,50 s | ZERBROCHEN. | Klammern und Rissakzent folgen dem tatsächlichen Telefon samt Kamerabewegung |
| 7,10–8,55 s | QUIETSCHENDE REIFEN. | Gestaffelte Wortanimation über dem echten Fahrzeugrad |
| 9,60–10,45 s | VERSCHWUNDEN. | Kurzes Ausgleiten |
| 12,94–14,32 s | 1 MINUTE SPÄTER. | Klarer Zeitsprung ohne Countdown |
| 14,52–15,48 s | GRÜN. | Impuls an der tatsächlichen grünen Fußgängerampel |
| 16,14–17,23 s | NICHT LOS. | Zwei betonte Wort-Einsätze |
| 19,32–21,37 s | GENAU DORT. | Animierter Pfeil und flache Markierung an der Gefahrenstelle |
| 22,84–24,15 s | ZUKUNFT GESEHEN. | Freistehender Text neben der Figur |
| 24,32–25,53 s | VERÄNDERT. | Grün gezeichneter Haken |
| 25,72–28,03 s | WAS WÄRE, WENN …? | Gestaffelte Frage |
| 28,58–30,00 s | 1 MINUTE VORAUS. | Gezeichnete Schlussbetonung in der laufenden Szene |

## Ton und Reproduktion

`scripts/make_accents_v3.py` synthetisiert die kurzen Text-, Glas-, Fokus- und Übergangsakzente lokal und deterministisch. Die Dateien `accent-v3.wav` und `mix-v3.wav` werden nur lokal erzeugt. Das Original-Voiceover behält Tempo, Tonhöhe, Startpunkt und Pegel. Die V2-Ortsgeräusche bleiben im Mix. Grafikakzente werden anhand der Sprachenergie weich abgesenkt. Der Code benötigt keinen zusätzlichen ElevenLabs-Aufruf und keine kostenpflichtige Sound-API.

`src/graphics-v3/cues.json` hält die gemeinsamen Hauptzeitpunkte für die zusätzlichen Texte und Sounds. `Emphasis.tsx` enthält die einzeln verfassten Textgruppen und die zum Bildraum passenden Zusatzgrafiken. `CartoonFilmV3.tsx` kombiniert sie mit dem bestehenden Film. V2-Quelldateien und V2-Ausgabe bleiben verfügbar.

Frischer Checkout: im Projektordner nach `npm ci`, Python-Setup und lokalem `make_audio.py /pfad/zur/Originalaufnahme.mp3` den Befehl `npm run render:v3` ausführen. Er erstellt die zusätzlichen WAVs, prüft TypeScript, rendert die 900 Frames, muxiert den fertigen Mix und prüft die kodierte MP4. Die separaten Audiospuren gehören nicht zum GitHub-Quellcode; sie werden aus der lokalen Originaldatei regeneriert.

## Prüfung

`scripts/qc_v3.py` übernimmt die vollständige technische Prüfung des tatsächlich kodierten Videos und erstellt zusätzliche Kontaktbögen aller Textmomente sowie der dichten Anfangsbewegung. Technische Messung und visuelle Einzelbildprüfung ersetzen keine kritische Hörprüfung oder vollständige Echtzeitwiedergabe. Die gemessenen Ergebnisse werden nach dem finalen Export in einem gesonderten V3-Qualitätsbericht dokumentiert.
