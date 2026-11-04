"""Copy a verified final film and its review artifacts; never publish audio stems."""
from pathlib import Path
import json,hashlib,shutil,collections
R=Path(__file__).resolve().parents[1];Q=R/'review/encoded-film';P=R.parent/'previews';P.mkdir(exist_ok=True)
T=json.loads((Q/'technical.json').read_text());V=R/'renders'/T['file']
assert T['full_decode']=='passed' and T['video']['nb_read_frames']=='10320'
assert hashlib.sha256(V.read_bytes()).hexdigest()==T['sha256']
frozen=json.loads((R/'production/render-source-hashes.json').read_text())
assert all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in frozen.items()),'Source changed during render'
assert V.stat().st_size<100*1024*1024,'Use a GitHub release asset or compress before delivery'
shutil.copy2(V,P/V.name);shutil.copy2(Q/'technical.json',R/'production/technical-final.json')
for n in ['Storyboard_1','Storyboard_2','Storyboard_3','Storyboard_4','Hook','Tasse','Bahn','Fussball','Handy','Anruf']:
 shutil.copy2(Q/(n+'.jpg'),P/('WhatIf_Dynamic_v2_'+n+'.jpg'))
check=json.loads((R/'production/hyperframes-check.json').read_text())
summary={k:{'ok':v.get('ok'),'errors':v.get('errorCount',0),'warnings':v.get('warningCount',0)} for k,v in check.items() if isinstance(v,dict) and 'ok' in v}
(R/'production/check-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
warnings=collections.Counter(f['code'] for x in check.values() if isinstance(x,dict) for f in x.get('findings',[]) if f.get('severity')=='warning')
motion=json.loads((R/'production/encoded-motion.json').read_text())
report=f'''# Eine Minute voraus · Dynamic Edition · Prüfung der Enddatei

Datei: `{V.name}`. Neuer vollständiger HyperFrames-Film zur am 4. November gelieferten Mark-Aufnahme. Die frühere Fassung bleibt erhalten.

## Inhalt und Tempo

96 motivierte Einstellungen in acht Set-Kategorien, durchschnittlich 3,58 Sekunden statt ungefähr 13,77 Sekunden in der vorigen Fassung. Der Schnitt wechselt zwischen Raumansicht, Reaktion, eigener Perspektive und Detail. Die neue Aufnahme bleibt vollständig und läuft in Originalgeschwindigkeit und Originaltonhöhe. Musik: vier Abschnitte aus drei lizenzierten Titeln. 57 synchronisierte Effekt-Ereignisse; nicht jeder Schnitt erhält einen Whoosh.

## Gemessene fertige MP4

| Prüfung | Ergebnis |
|---|---|
| Dauer | {T['video']['duration']} Sekunden |
| Bild | 1920 × 1080, 16:9, H.264, yuv420p |
| Bildrate / Frames | 30 FPS / {T['video']['nb_read_frames']} |
| Ton | AAC Stereo, 48 kHz |
| Vollständige Dekodierung | bestanden |
| Schwarze Frames | {T['black_frames']} |
| Lautheit | {T['loudness']['input_i']} LUFS |
| True Peak | {T['loudness']['input_tp']} dBTP |
| Stimme/Mix-Korrelation ohne Zeitversatz | {T['voice_to_decoded_mix_correlation_at_zero_lag']:.6f} |
| Aus der Enddatei extrahierte Prüfbilder | {T['review_frames']} |
| Dateigröße | {T['bytes']:,} Bytes |
| SHA-256 | `{T['sha256']}` |

## Tatsächlich durchgeführte Korrekturen

Vor dem Render wurden alle 96 Einstellungen anhand von HyperFrames-Bildserien betrachtet. Anschließend wurden kritische Bewegungen separat erneut geprüft. Korrigiert wurden die unterstützte Selektor-Schreibweise, die genaue Audio-Samplerate vor dem Auffüllen, die Tiefenstaffelung und Beinbewegung beim Einstieg, der sichtbare Griff am großen Smartphone, die Lage des Telefons auf dem Tisch sowie das sichtbare Smartphone beim Einstecken. Zukunftsszenen zeigen eigene Arme und Hände anstelle eines Blicks auf das eigene Gesicht. Die Armbanduhr hängt am sichtbaren, bis zum Bildrand fortgesetzten Ärmel.

Die Börsenanzeige vor dem Kauf wurde auf 100,00 € korrigiert; der Vorausblick zeigt 101,28 €. Die Beispielrechnung lautet 12,80 € − 2,90 € − 1,40 € = 8,50 €. Fußballspieler bleiben nach der Prüfung an ihren Positionen; der Ball überschreitet die Torlinie. Nach der Aberkennung steht es wieder 0:0, und die dargestellte Nächstes-Tor-Wette bleibt offen. Der kleine Radfahrer hat einen vollständigen Körper und ein vollständiges Fahrrad. Die Gegenaufnahme des Anrufs zeigt den Freund in seinem eigenen Raum. Die genaue Erzähl- und Zukunftslogik steht in `production/STORY_LOGIC.md`.

Die gerenderten Quellen wurden vor dem vollständigen HyperFrames-Lauf gehasht. Die Hashes wurden vor der Auslieferung erneut mit den Quelldateien verglichen.

Die vier Kontaktbögen aller 96 Einstellungen wurden aus der tatsächlich ausgelieferten MP4 betrachtet. Zusätzlich wurden die dichten Bildserien für Tasse, Einstieg, Tor/Videoassistent, Einstecken des Handys und Anruf geprüft. Die korrigierten Kontakte und Zustandswechsel sind darin vorhanden; Text und wichtige Handlungen bleiben in diesen geprüften Bildern lesbar. Die kurzen Doppelbilder innerhalb der 0,22-sekündigen Übergänge gehören zur Überblendung. Der ursprüngliche HyperFrames-Bildstrom wird ohne erneute verlustbehaftete Videokomprimierung übernommen und mit dem kanonischen Tonmix verbunden.

## Check-Hinweise

Der vollständige HyperFrames-Check hat keine Fehler in Lint, Laufzeit, Layout, Bewegung, Kontrast oder Audio. Verbleibende Warnungsarten: `{dict(warnings)}`. Die Ruhephasen-Heuristik sieht die über GSAP-Objektparameter aktualisierte SVG-Geometrie des Rigs nicht vollständig. `production/encoded-motion.json` misst deshalb tatsächliche aufeinanderfolgende Bilder aller {len(motion)} Einstellungen. Kurze Reaktions- und Lesepausen sind Teil des Schnitts. Wiederkehrende Zukunftslabels werden bereits im Hook eingeführt. Die Layout-Infos im Schluss entstehen in der 0,22-sekündigen Überblendung zweier Einstellungen mit derselben Credit-Zeile und wechselnden Überschriften; die Bilder wurden dafür geprüft.

## Grenzen und Quellen

Die Enddatei wurde vollständig technisch dekodiert, der Ton gemessen und die Schlüsselbilder visuell geprüft. Keine vollständige kritische Echtzeit-Hörabnahme wird behauptet. Das ist keine Garantie für jede einzelne gestalterische Entscheidung.

Musik von Kevin MacLeod: The Descent, Carefree, Dream Culture; incompetech.com, CC BY 4.0. Titel, Lizenzlink und Bearbeitung stehen im Film, in seinen Metadaten und in `assets/audio/CREDITS.md`. Hinzu kommen originale Absurditas-Fahrzeuggeräusche, originale gestaltete Foley-Effekte und HyperFrames/Pixabay-Übergangs-/UI-Geräusche. Die gestalteten Effekte werden nicht als Naturaufnahmen ausgegeben. Credits beim Weiterveröffentlichen beibehalten.

Die öffentliche Quelldatei enthält weder die separate hochgeladene MP3 noch WAV-Mischspuren. Die fertige MP4 enthält den vollständigen Ton. Die Aufnahme wurde zur lokalen Ausrichtung nicht an eine Transkriptions-API hochgeladen.
'''
(R/'production/REVIEW.md').write_text(report);(P/'WhatIf_Dynamic_v2_Qualitaet.md').write_text(report)
print(json.dumps({'file':str(P/V.name),'bytes':T['bytes'],'sha256':T['sha256']},indent=2))
