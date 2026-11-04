"""Prepare public MP4/review artifacts after QC, without publishing audio stems."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image

R=Path(__file__).resolve().parents[1];Q=R/'review/encoded-film';P=R.parent/'previews';P.mkdir(exist_ok=True)
T=json.loads((Q/'technical.json').read_text());V=R/'renders'/T['file']
assert T['full_decode']=='passed' and T['video']['nb_read_frames']=='9090'
assert hashlib.sha256(V.read_bytes()).hexdigest()==T['sha256']
frozen=json.loads((R/'production/render-source-hashes.json').read_text())
assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in frozen.items()),'Composition changed during final render'
shutil.copy2(V,P/V.name)
for old,new in [('Filmuebersicht.jpg','WhatIf_HyperFrames_Filmuebersicht.jpg'),('Hook.jpg','WhatIf_HyperFrames_Hook.jpg'),('Tasse_und_Tablett.jpg','WhatIf_HyperFrames_Tasse_und_Tablett.jpg')]:
 shutil.copy2(Q/old,P/new)
shutil.copy2(Q/'technical.json',R/'production/technical-final.json')
indices=json.loads((Q/'frame-index.json').read_text());lookup={n:Q/f'frame-{i+1:04d}.png' for i,n in enumerate(indices)}
check=json.loads((R/'production/hyperframes-check.json').read_text());motion=[]
for f in check.get('craft',{}).get('findings',[]):
 if f.get('code')!='dead_stretch':continue
 start=f['time'];end=min(302.9,start+3)
 a=min(indices,key=lambda n:abs(n-start*30));b=min(indices,key=lambda n:abs(n-end*30))
 with Image.open(lookup[a]) as im:x=np.asarray(im.resize((256,144)),dtype=float)
 with Image.open(lookup[b]) as im:y=np.asarray(im.resize((256,144)),dtype=float)
 motion.append({'reported_start':start,'checked_times':[a/30,b/30],'mean_pixel_change':float(np.abs(x-y).mean())})
(R/'production/motion-warning-review.json').write_text(json.dumps(motion,indent=2)+'\n')
summary={k:{'ok':z.get('ok'),'errors':z.get('errorCount',0),'warnings':z.get('warningCount',0)} for k,z in check.items() if isinstance(z,dict) and 'ok' in z}
review=f'''# What-if · vollständiger HyperFrames-Film · Qualitätsbericht

Datei: `{T['file']}`. Der vollständige Film wurde mit HyperFrames 0.9.12 aus HTML/SVG-Kompositionen und GSAP gerendert. Die neue Mark-Aufnahme ist vollständig enthalten; Tempo und Tonhöhe bleiben erhalten. Musik, Regen, Fahrzeug- und Übergangseffekte sind im ausgelieferten Film gemischt. Der Abo-Aufruf gehört zur aufgenommenen Schlusszeile und zur Animation.

## Gemessene Enddatei

| Prüfung | Ergebnis |
|---|---|
| Dauer | {T['video']['duration']} Sekunden |
| Bild | 1920 × 1080, 16:9, H.264, yuv420p |
| Bildrate / Frames | 30 FPS / {T['video']['nb_read_frames']} |
| Audio | AAC, Stereo, 48 kHz |
| Vollständige Dekodierung | bestanden |
| Schwarze Frames | {T['black_frames']} |
| Gemessene Lautheit | {T['loudness']['input_i']} LUFS |
| Gemessener True Peak | {T['loudness']['input_tp']} dBTP |
| Stimme / dekodierter Mix bei gleichem Zeitraster | Korrelation {T['voice_to_decoded_mix_correlation_at_zero_lag']:.6f} |
| Extrahierte Prüfbilder | {T['review_frames']} |
| Dateigröße | {T['bytes']:,} Bytes |
| SHA-256 | `{T['sha256']}` |

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
'''
(R/'production/REVIEW.md').write_text(review);(P/'WhatIf_HyperFrames_Qualitaet.md').write_text(review)
(R/'production/check-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'file':str(P/V.name),'bytes':T['bytes'],'sha256':T['sha256'],'motion_intervals_reviewed':len(motion)},indent=2))
