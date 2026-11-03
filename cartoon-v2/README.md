# What-if · Eine Minute Zukunft · Cartoonfilm V2

Eine in einer einzigen Straßenwelt gespielte 30-Sekunden-Cartoonszene. Schwarzer runder Kopf, weiße Mimik, orangefarbener Hoodie, warme Stadt. Zukunftsvision, beschädigtes Telefon, tatsächliches Fahrzeugrad, Rückkehr, Schrittabbruch und Vorbeifahrt verwenden dieselben Weltkoordinaten. Kein Countdown, Lageplan oder Erklärkarten.

1920 × 1080 · 16:9 · 30 FPS · 900 Frames · H.264 / AAC.

## Installieren

Getestete Umgebung: Linux x86_64, Node 24.22.1, Python 3.12.14, FFmpeg/FFprobe 7.1.5. Remotion 4.0.540, React 19.2.4, TypeScript 5.9.3. Versionspins stehen im npm-Lockfile; für die Bild-/Tonprüfung werden NumPy 2.5.4 und Pillow 13.0.0 verwendet.

Im Ordner `cartoon-v2`:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci
NODE_USE_ENV_PROXY=1 npx remotion browser ensure
.venv/bin/python scripts/make_audio.py /pfad/zur/Originalaufnahme.mp3
```

In der verwalteten Cloud den vorhandenen Proxy beibehalten. Falls npm ihn nicht automatisch nutzt, `npm ci` mit `npm_config_https_proxy="$HTTPS_PROXY" npm_config_proxy="$HTTP_PROXY"` ausführen. Keine TLS-Prüfung abschalten und keine Zugangsdaten in Dateien speichern.

Die einzelnen Installationswerkzeuge sind bereits in der Produktionsumgebung vorhanden. Der Export wurde mit den vorhandenen Paketen und dem offiziellen Remotion-Browser tatsächlich gerendert. Lokale Verknüpfungen zu installierten Paketen gehören nicht zu den veröffentlichten Quelldateien.

## Studio und Rendering

```sh
npm run studio -- --no-open
npm run render
```

Komposition: `WhatIfCartoonV2`. Acht verbundene Einstellungs-Kompositionen befinden sich unter `Cartoon-V2-Shots`. Sie verwenden dieselben Komponenten und können im Studio einzeln geöffnet werden.

Der Renderbefehl prüft TypeScript, rendert mit drei parallelen Browserseiten, muxiert den kanonischen Originalstimmen-Mix genau auf 30 Sekunden und prüft die tatsächliche MP4. Jeder fehlgeschlagene Unterbefehl bricht den Ablauf ab.

Ergebnis: `out/WhatIf_Eine_Minute_Zukunft_Hook_v2_30s.mp4`.
Kontaktbogen und Messwerte: `out/qc/`.

Den vorhandenen Checkout direkt nutzen. Cloud-Aufgaben sind bereits isoliert; keinen weiteren Worktree anlegen, außer der Nutzer verlangt dies ausdrücklich. Live-Prozesse überstehen keinen Umgebungsneustart; Studio bei Bedarf erneut starten.

## Ton

Separate Audiodateien werden nicht mit dem GitHub-Quellcode veröffentlicht. Vor dem Rendern erzeugt `scripts/make_audio.py` die benötigten WAV-Dateien lokal aus der vom Nutzer bereitgestellten Original-MP3. Verwendet werden ausschließlich die ersten 30 Sekunden. Ein ElevenLabs-Zugang ist nicht nötig. Das veröffentlichte MP4 enthält den fertig gemischten Ton.

Die Aufnahme wurde nicht umgesprochen und nicht beschleunigt. Ein geringer Hochpass, ein fester Pegel und kurze Randblenden werden angewandt. Die erste und letzte Phrase bleiben vollständig im 30-Sekunden-Abschnitt.

Vor dem ersten Rendern die Tondateien aus der lokalen Originaldatei erzeugen:

```sh
.venv/bin/python scripts/make_audio.py /pfad/zur/Originalaufnahme.mp3
```

Optional neue Wortzeitpunkte lokal ermitteln: `faster-whisper==1.2.1` installieren und `scripts/align_voice.py` mit der Originaldatei ausführen. Das kostenlose Modell `small` wird heruntergeladen; Audio wird lokal verarbeitet. Für diese Produktion konnten bestehende tatsächlich ermittelte Zeitpunkte weiterverwendet werden, weil beide Uploads SHA-256-identisch sind. Es wurde keine bezahlte API aufgerufen.

## Struktur und Grenzen

`src/cartoon-v2/Actor.tsx` enthält Rig, Mimik und eigenständige Liegepose; `Street.tsx` die gemeinsame Kulisse; `Props.tsx` Telefon, Ampeln und Auto; `Shots.tsx` die acht Kameraeinstellungen; `CartoonFilm.tsx` Bild-/Ton-Timeline; `math.ts` Zeitkurven, IK und Fahrzeugbahn.

Die Referenzbilder wurden in der Unterhaltung visuell analysiert. Ihre Playeroberflächen und Datumsanzeigen wurden nicht übernommen. Eigenständige Vektoren bilden die Figur und Stadt. Manrope liegt samt SIL-OFL-Lizenz bei; weitere Bibliotheken behalten ihre jeweiligen Lizenzbedingungen.

Die Qualitätsprüfung unterscheidet technische Messung, visuell betrachtete Bilder und nicht erfolgte kritische Hörprüfung/Echtzeitwiedergabe. Details stehen in `docs/QUALITAET.md`.

Nur dieser Hook ist produziert. Vor einem Langvideo ist Nutzerfeedback vorgesehen.
