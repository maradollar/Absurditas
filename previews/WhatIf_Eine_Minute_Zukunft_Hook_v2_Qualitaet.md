# Qualitätsbericht · Cartoonfilm V2

Produziert wurde ausschließlich der 30-Sekunden-Hook. Der verwendete Master-Prompt und seine Referenzanalyse liegen im Quellcodeprojekt unter `docs/`.

## Gestaltung und Handlung

Schwarzer runder Kopf, weiße reduzierte Mimik, orangefarbener Hoodie, kräftige Konturen, helle Stadt und weiche Lichtkanten übertragen die zuletzt bereitgestellten Referenzen in eigenständige Vektoren. Die Hauptfigur trägt in allen Einstellungen dieselbe Kleidung. Die blaue Hoodie-Variante, Regeltafeln, Playeroberflächen und Tagesanzeigen aus den Screenshots wurden nicht übernommen.

Acht verbundene Kameraeinstellungen verwenden dieselben Straßenkoordinaten. Vision und Gegenwart teilen Café, Bordstein, Überweg, Ampeln und Fahrzeugbahn. Die Figur wartet vor dem Bordstein, hebt den Fuß zum Losgehen und setzt ihn wieder auf dem Gehweg auf. Ein von links kommendes Auto fährt bei roter Fahrzeugampel über denselben Überweg und verlässt rechts das Bild. Die Vision zeigt den Körper an dieser Fahrspur. Die Straße bleibt bis zum Schluss erhalten. Es gibt keinen Countdown, keine Kartenansicht, keine Geisterposition und keine wechselnden Erklärfolien.

## Originalstimme und Ton

Die erneut hochgeladene MP3 hat denselben SHA-256-Hash wie die zuvor tatsächlich lokal transkribierte Aufnahme. Die vorhandenen Wortzeitpunkte wurden deshalb wiederverwendet; eine erneute Transkription wurde nicht behauptet. Der durchgehende Originalabschnitt 0–30 s bleibt im ursprünglichen Sprechtempo. Ein geringer Hochpass, ein fester Pegel und kurze Randblenden werden angewandt. Die vollständige vierminütige Datei wird nicht separat veröffentlicht.

Geräusche sind für diese Fassung deterministisch synthetisiert: leise Straßenluft, Wahrnehmungswechsel, Reifenreibung am tatsächlich sichtbaren Rad, Kleidung, ein Fußaufsatz und ein von links nach rechts vorbeifahrendes Fahrzeug. Sprachabhängiges Ducking hält die Geräusche unter der Stimme. Keine bezahlte API und keine fremden Stock-Samples wurden eingesetzt.

## Tatsächlich ausgeführte Prüfrunden und Verbesserungen

1. Zwölf Schlüsselbilder in voller Auflösung sowie die separat registrierte Entscheidungsszene gerendert und ausgewählte Bilder visuell betrachtet. Dabei waren der Hoodie zu kurz und die Blickrichtung zu frontal. Hoodie-/Armproportionen verlängert, Kopf-/Blickausrichtung deutlicher gemacht und eine sichtbare seitliche Straße ergänzt. Die eigenständige Liegepose wurde unabhängig vom Stehrig gezeichnet.
2. Einen vollständigen 900-Frame-Prüfrender in halber Auflösung erstellt. Den Sekundenkontaktbogen sowie dichte Schritt- und Fahrzeugfolgen visuell betrachtet. Die Telefon-Nahaufnahme betonte den unscharfen Kopf zu stark; der Bildausschnitt wurde auf das Telefon zentriert und enger gefasst. Der Farbstich der Vision wurde reduziert, damit der Hoodie orange erkennbar bleibt. Die Hand führt das intakte Telefon in der Schlussreaktion deutlicher zum Blick.
3. Vollständigen 1080p-Endrender erstellt und technisch geprüft. Den finalen Kontaktbogen, die Autofolge und ausgewählte vollauflösende Details tatsächlich betrachtet. Anschließend das eigenständig nutzbare Quellcodeprojekt im Exportverzeichnis erneut vollständig mit seinem dokumentierten Renderbefehl ausgeführt. Beide daraus erzeugten MP4-Dateien sind SHA-256-identisch.

## Bewegungs- und Raumprüfung

Zusätzlich zur Bildsichtung wurde die tatsächlich verwendete Animationsfunktion ausgewertet. Diese Zahlen prüfen die geometrische Inszenierung, keine vollständige menschliche Biomechanik:

- Drift des hinteren Stützfußes im Entscheidungsabschnitt: 0 px.
- Aufgesetzter vorderer Fuß bei Y 973.5 liegt sicher vor dem als Y 954 definierten Bordstein.
- Maximale Anhebung des vorderen Fußes: 41.4 px; anschließend Rückkehr zum ursprünglichen Standpunkt.
- Fahrzeugbahn läuft durchgehend nach rechts und kehrt nicht um.
- Fahrzeugfront erreicht den Überweg bei Frame 519 / 17.30 s.
- Fahrzeugheck hat den Überweg bei Frame 546 / 18.20 s verlassen. Die Stelle ist bei „Genau dort …“ wieder frei.
- Die Raddrehung wird aus tatsächlich zurückgelegter Fahrzeugstrecke und Radradius abgeleitet.

## Technisch gemessen an der fertigen MP4

| Eigenschaft | Ergebnis |
|---|---|
| Video | H.264 / yuv420p |
| Größe | 1920 × 1080 / 16:9 |
| Bildrate / Zahl | 30 FPS / 900 vollständig decodierte Frames |
| Bild-, Ton- und Containerdauer | jeweils 30.000000 s |
| Ton | AAC / Stereo / 48 kHz |
| Schwarze Frames | 0 erkannt, alle Frames verkleinert geprüft |
| Lautheit | -14.07 LUFS integriert |
| True Peak | -2.26 dBTP |
| Sprachspur-/Endmix-Korrelation | 0.999151 |
| Prüfbilder | 93 automatisch extrahiert |
| TypeScript | bestanden |
| Vollständige Decodierung | bestanden |

Die Korrelation prüft Erhalt und Lage der festgehaltenen Sprachspur im Endmix. Sie ist keine Bewertung von Verständlichkeit oder künstlerischer Klangqualität. Nahezu identische benachbarte Bilder der verkleinerten Differenzprüfung kommen an ruhigen Haltepunkten vor und bedeuten nicht automatisch einen eingefrorenen Film.

## Grenzen der Prüfung

Die gerenderten Standbilder und geordneten Bewegungsfolgen wurden wirklich visuell betrachtet. Eine durchgehende Echtzeit-Videowiedergabe und eine kritische Hörprüfung waren hier nicht verfügbar. Klang wurde technisch auf Pegel, Übersteuerung und Zeitlage geprüft. Automatische Messwerte ersetzen kein Hörurteil.

Die Kulisse ist eine schematische, fiktionale Stadt; die Inszenierung ist ein Gedankenexperiment. Das Rig unterstützt die für diesen Hook benötigten Posen und Handlungen. Die nächste Weiterarbeit richtet sich nach Nutzerfeedback; ein Langvideo wurde nicht produziert.
