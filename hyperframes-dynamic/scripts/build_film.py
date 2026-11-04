"""Word-aligned, faster cinematic cartoon edition. No generated voice or slideshow."""
from pathlib import Path
import json,re,math,difflib,hashlib
from art import *
from worlds import room,kitchen,office,station,train,living,laptop,phone_large,food,envelope,van,wall_clock
R=Path(__file__).resolve().parents[1];DURATION=344.0

# Each tuple is a motivated new camera setup, insert or location, tied to narration.
# No single wide view is held for a chapter.
PLAN=[
('', 'street','ground',(950,833,3.4),True,'ASPHALT.'),
('Neben dir liegt','street','broken',(872,855,4.0),True,'ZERBROCHEN.'),
('Bremsen kreischen','street','brake',(1470,790,2.5),True,'BREMSEN.'),
('Du stehst noch','street','return',(900,554,1.04),False,''),
('Das war kein Albtraum','street','realize',(820,454,1.85),False,'KEIN ALBTRAUM.'),
('Du hast gesehen','street','watch',(920,668,2.1),False,'GLEICH PASSIERT ES.'),
('Als die Ampel','street','green',(1060,580,1.12),False,'GRÜN.'),
('Ein Lieferwagen','street','pass',(1010,620,1.08),False,''),
('Der Fahrer hat Rot','street','driver',(1150,722,2.15),False,'ER HAT ROT.'),
('Du lebst weil','street','relief',(820,465,1.62),False,''),
('Was wäre wenn','street','question',(960,555,1.02),False,'1 MINUTE VORAUS?'),
('Zuerst klingt','kitchen','confident',(900,570,1.04),False,'IMMER EINEN SCHRITT VORAUS.'),
('Doch es gibt eine Regel','street','rule',(840,490,1.42),False,'EINE REGEL.'),
('Du siehst keine ganze Minute','street','moment',(1040,690,1.5),True,'EIN AUSSCHNITT.'),
('Du bekommst einen kurzen Ausschnitt','street','perspective',(950,746,1.8),True,'DEINE PERSPEKTIVE.'),
('genau 60 Sekunden später','street','watchfuture',(920,668,2.1),True,'GENAU +60 SEKUNDEN.'),
('Er zeigt was passieren würde','street','path',(950,575,1.06),True,''),
('Änderst du deine Entscheidung','street','choose',(950,575,1.06),False,'DU ÄNDERST DEN KURS.'),
('Nachsehen kannst du','street','noreset',(820,480,1.6),False,'KEIN ZURÜCKSPULEN.'),
('Du probierst es aus','kitchen','establish',(950,558,1.0),False,''),
('In der Küche siehst du Kaffee','kitchen','spill',(980,747,2.05),True,''),
('Dein Ärmel hängt','kitchen','sleeve',(829,740,2.65),False,'DEIN ÄRMEL.'),
('Diesmal schiebst du sie weg','kitchen','move',(812,744,2.5),False,''),
('Eine Minute später streift','kitchen','brush',(845,737,2.3),False,'DIE STELLE BLEIBT FREI.'),
('Keine Tasse','kitchen','dry',(1120,656,2.4),False,'LAPTOP GERETTET.'),
('Draußen zeigt dein Vorausblick','station','missed',(1100,560,1.25),True,'KNAPP VERPASST.'),
('Also läufst du los','station','run',(940,585,1.02),False,''),
('und steigst rechtzeitig ein','station','board',(1150,865,2.1),False,'GESCHAFFT.'),
('Zwei Entscheidungen','station','depart',(960,570,1.0),False,'ZWEI BESSERE ERGEBNISSE.'),
('Bei der Arbeit','office','boss',(965,570,1.0),False,''),
('Im Vorausblick suchst du','office','search',(1120,625,2.4),True,'WO IST DIE ZAHL?'),
('Jetzt öffnest du','office','answer',(1120,625,2.4),False,'RECHTZEITIG.'),
('Eine Kollegin','office','joke',(1040,525,1.18),False,''),
('Du lachst trotzdem','office','laugh',(640,463,1.85),False,'DU KENNST DIE POINTE.'),
('Dann kommt die Frage','stock','money',(930,563,1.05),False,'REICH WERDEN?'),
('Du öffnest einen Aktienkurs','stock','chart',(1120,629,2.35),False,''),
('Ein Blick voraus','stock','rise',(1120,629,2.35),True,'DER PREIS STEIGT.'),
('Du kaufst','stock','buy',(1120,629,2.35),False,'KAUFEN.'),
('Kurz darauf erscheint','stock','profit',(1120,629,2.35),False,'ERSTER GEWINN.'),
('Du versuchst es wieder','stock','repeat',(945,567,1.1),False,''),
('Doch Gebühren','stock','fees',(1120,629,2.35),False,'DIE KOSTEN BLEIBEN.'),
('Den Kurs hast du','stock','net',(1120,629,2.35),False,'KURS ≠ NETTOGEWINN.'),
('Und die Lotto','stock','lotto',(1230,715,2.0),False,'ZIEHUNG: HEUTE ABEND.'),
('Dein Blick reicht','stock','horizon',(1170,680,1.85),True,'NUR DIE NÄCHSTE MINUTE.'),
('Beim Fußball','living','football',(960,555,1.0),False,''),
('Du siehst einen Stürmer','living','goalvision',(1070,488,1.42),True,'TOR?'),
('Du setzt auf das Tor','living','bet',(960,580,1.0),False,''),
('Der Ball geht rein','living','goal',(1070,488,1.42),False,'TOR!'),
('Dann meldet sich','living','var',(960,478,1.45),False,''),
('Abseits','living','offside',(1050,488,1.42),False,'ABSEITS.'),
('Dein Ausschnitt hatte','living','limited',(960,555,1.0),False,'DER AUSSCHNITT WAR ZU KURZ.'),
('Die Wette ist längst','living','pending',(960,580,1.0),False,'ABGEGEBEN. NICHT GEWONNEN.'),
('Du hast etwas Richtiges','living','reaction',(620,760,1.7),False,'RICHTIG GESEHEN. FALSCH GEDEUTET.'),
('Genau hier wird','stock','overconfident',(640,466,1.75),False,'ZU SICHER.'),
('Also vergisst du','stock','information',(1120,629,2.35),False,'WAS FEHLT IM BILD?'),
('An der nächsten Kreuzung','street','crossing',(960,550,1.05),False,''),
('Freie Straße','street','empty',(1175,715,1.55),True,'EIN FREIER MOMENT.'),
('Dann hältst du inne','street','stop',(840,610,1.35),False,''),
('Du hast einen einzigen Moment','street','single',(1160,705,1.4),True,'EIN MOMENT ≠ EINE MINUTE.'),
('Nicht alles was','street','side',(1550,525,1.65),False,''),
('Du steckst das Handy weg','street','pocket',(900,710,1.9),False,''),
('und schaust nach links','street','look',(820,460,1.6),False,'LINKS. RECHTS. MITDENKEN.'),
('Bis hierhin hast du','cafe','arrival',(960,560,1.0),False,''),
('Jetzt sitzt dir','cafe','friend',(1300,457,1.65),False,''),
('Du schaust voraus','cafe','job',(1330,500,1.65),True,'JOB VERLOREN.'),
('Sofort suchst du','cafe','thinking',(640,457,1.9),False,'DIE PERFEKTE ANTWORT?'),
('Du prüfst eine Reaktion','cafe','hurt',(1315,475,1.65),True,''),
('Also versuchst du eine andere','cafe','tryagain',(1330,490,1.65),True,'NOCH EIN VERSUCH.'),
('Während du mögliche Gespräche','cafe','distracted',(980,550,1.08),False,''),
('Dein Freund erzählt','cafe','talk',(1330,470,1.65),False,''),
('Dein Blick wandert weg','cafe','away',(640,467,1.8),False,''),
('hörst du mir überhaupt zu','cafe','question',(1330,480,1.6),False,'HÖRST DU MIR ZU?'),
('Diesen Satz hattest du','cafe','shock',(640,470,1.85),False,''),
('dass du den Menschen','cafe','distance',(980,550,1.0),False,'DER ECHTE MOMENT GEHT VERLOREN.'),
('Eine Überraschung','cafe','gift',(1150,775,2.5),True,'KEINE ÜBERRASCHUNG MEHR.'),
('Ein Witz wartet','office','jokereprise',(1390,485,1.8),True,''),
('Du kennst Nachrichten','dinner','message',(960,580,1.0),True,'SCHON GELESEN.'),
('Reaktionen bevor','cafe','reactions',(1315,475,1.65),True,''),
('Jeder Blick macht','dinner','compulsion',(640,450,1.8),False,'NUR NOCH EIN BLICK.'),
('Am Abend sitzt','dinner','dinner',(960,560,1.0),False,''),
('Du könntest prüfen','dinner','temptation',(1090,755,2.1),False,'WAS KOMMT GLEICH?'),
('Nur kurz','dinner','hesitate',(640,468,1.85),False,'NUR ZUR SICHERHEIT?'),
('Eine Minute einfach','dinner','wait',(1020,740,2.1),False,''),
('Früher musstest du','dinner','uncertainty',(960,550,1.05),False,'UNSICHERHEIT ZULASSEN.'),
('Genau das versuchst du','dinner','decide',(640,467,1.75),False,''),
('Du rufst deinen Freund','dinner','call',(960,580,1.0),False,''),
('Ohne seine Antwort','dinner','speaker',(1100,740,2.0),False,'OHNE VORAUSZUSCHAUEN.'),
('Vorhin war ich abgelenkt','dinner','apology',(640,470,1.8),False,''),
('Erzähl mir bitte','cafe','friendcall',(1315,480,1.6),False,''),
('Zum ersten Mal heute','dinner','listen',(640,470,1.8),False,'DU HÖRST ZU.'),
('Eine Minute Vorsprung','street','saved',(960,555,1.02),False,'VORSPRUNG RETTET LEBEN.'),
('Trotzdem hat sie','dinner','life',(960,555,1.02),False,'WIE WILLST DU LEBEN?'),
('Würdest du ständig','dinner','choice',(640,470,1.65),False,'IMMER? NUR BEI GEFAHR?'),
('Oder würdest du','dinner','release',(960,555,1.02),False,'ODER WIEDER LOSWERDEN?'),
('Schreib deine Entscheidung','dinner','comment',(960,555,1.02),False,'DEINE ENTSCHEIDUNG?'),
('und abonnier den Kanal','dinner','subscribe',(960,555,1.02),False,'ABONNIEREN')
]

def norm(s):
 s=s.casefold().replace('sechzig','60');return re.sub(r'[^\wäöüß]','',s)
def align():
 data=json.loads((R/'production/alignment.json').read_text());words=[w for s in data for w in s['words']];ns=[norm(w['word']) for w in words]
 cursor=0;out=[]
 for i,(phrase,world,action,cam,future,accent) in enumerate(PLAN):
  if not phrase:start=0;score=1
  else:
   target=[norm(x) for x in phrase.split()];candidates=[]
   for j in range(cursor,len(ns)-len(target)+1):
    score=difflib.SequenceMatcher(None,''.join(target),''.join(ns[j:j+len(target)])).ratio();candidates.append((score,-j,j))
   score,_,j=max(candidates);assert score>=.80,(phrase,score)
   cursor=j+max(1,len(target)-1);start=max(0,round((words[j]['start']-.06)*30)/30)
  out.append({'id':f's{i+1:03d}-{action}','start':round(start,5),'world':world,'action':action,'camera':cam,'future':future,'accent':accent,'anchor':phrase,'match':score})
 for i,s in enumerate(out):
  end=out[i+1]['start'] if i+1<len(out) else DURATION
  s['end']=round(min(DURATION,end+.22),5);s['duration']=round(s['end']-s['start'],5)
  assert s['duration']>1.05,(s['id'],s['duration'])
 return out

def broken_phone():
 return g(rect(-67,-121,134,242,INK,18)+rect(-58,-105,116,205,'#a6c3ce',10)+path('M-54-76L51 76M-55 13L53-54M-2-6L-34 91M-2-6L37 36M-31-38L22-81',stroke=CREAM,sw=4), 'data-anim="broken-phone" transform="translate(870 857) rotate(-13) scale(.72 .35)"')

def screen_overlay(action):
 # These labels belong to the physical laptop screen, not a floating slide.
 b=''
 if action in ['search','answer','information']:
  b+=rect(-188,-190,376,165,'#e8eee2',5)
  if action=='search':b+=text(0,-128,'DATEI NICHT GEFUNDEN',23,'#a15f53',800,'middle')+path('M-115-80H90M-115-56H40',stroke='#bfcdc1',sw=7)
  elif action=='answer':b+=text(-157,-142,'UMSATZ · Q3',23,'#507e7c')+text(-157,-83,'47.280 €',43,INK)
  else:b+=text(0,-131,'NUR EIN ZEITPUNKT',24,INK,800,'middle')+path('M-143-78H145',stroke='#bdcabc',sw=6)+rect(21,-106,18,56,AMBER,3)
 if action in ['buy','profit','fees','net']:
  b+=rect(-188,-191,376,166,'#e8eee2',5)+text(-161,-159,'BEISPIEL · 10 ANTEILE',17,'#507e7c')
  if action=='buy':b+=text(0,-112,'100,00 €',36,INK,800,'middle')+rect(-107,-89,214,49,'#507e7c',8)+text(0,-54,'KAUF AUSGEFÜHRT',19,CREAM,800,'middle')
  elif action=='profit':b+=text(0,-112,'+12,80 €',44,'#386650',800,'middle')+text(0,-62,'VOR KOSTEN',21,'#507e7c',700,'middle')
  else:
   for y,label,amount in [(-128,'Kursgewinn','+12,80 €'),(-99,'Gebühren','−2,90 €'),(-70,'Ausführung','−1,40 €')]:b+=g(text(-160,y,label,20,INK,600)+text(162,y,amount,21,INK,800,'end'),'data-anim="cost-row"')
   b+=path('M-162-58H162',stroke='#849e8e',sw=2)+text(-160,-33,'NETTO',20,'#386650')+text(163,-30,'+8,50 €',27,'#386650',800,'end')
 return g(b,'transform="translate(1120 761)"')

def illustration(s):
 p=s['id'];w=s['world'];a=s['action'];du=s['duration'];b=defs(p);fig='';fg='';extra=''
 if w=='street':
  b+=street(p)+van()
  if not s['future'] and a not in ['ground','broken','brake','moment','perspective','empty','single','side','watch','watchfuture']:fig+=actor('hero',820,970,.94)
  if a in ['ground','broken']:fg+=broken_phone()
  if a in ['crossing','stop','pocket']:fg+=phone()
  if a in ['watch','watchfuture']:
   fg+=g(path('M-850 100L-120 36L146 34',stroke=HOOD,sw=71)+ellipse(146,33,34,34,INK)+rect(-51,-24,118,100,INK,19)+rect(-40,-13,96,77,'#ecdfbe',13)+text(8,36,'08:00' if s['future'] else '07:59',25,INK,800,'middle'),'transform="translate(900 688)" data-anim="watch"')
  if a in ['moment','perspective','single','empty']:
   extra+=path('M150 350V285H280M1640 285H1770V350M1770 730V795H1640M280 795H150V730',stroke=AMBER,sw=9,extra='data-anim="finder"')
  if a in ['path','choose']:
   fg+=path('M815 1000Q840 922 950 787Q1050 710 1160 688',stroke=AMBER if a=='path' else '#83ba8f',sw=9,extra='stroke-dasharray="17 19" data-anim="route"')
  if a=='side':
   bike=ellipse(-43,0,25,25,INK)+ellipse(43,0,25,25,INK)+ellipse(-43,0,19,19,'#c6d2cc')+ellipse(43,0,19,19,'#c6d2cc')+path('M-43 0L-14-43L5 0H-43M-14-43H27L43 0M5 0L27-43L33-64H47',stroke='#527b77',sw=7)+ellipse(-3,-102,14,14,INK)+path('M-15-88L9-93L25-68L5-51L-20-70Z','#437daf')+path('M9-80L24-65L35-62M-4-56L-21-31L0-8M5-53L20-28L-4-9',stroke=INK,sw=9)
   fg+=g(bike,'transform="translate(1560 485)" data-anim="cyclist"')
 elif w in ['kitchen','office','stock','dinner','cafe']:
  b+=(room(p,True) if a=='friendcall' else cafe(p)) if w=='cafe' else kitchen(p,w=='dinner') if w in ['kitchen','dinner'] else office(p)
  b+=chair(640)
  if w=='cafe':b+=chair(1340)
  if a not in ['message','call']:fig+=actor('hero',640,970,.95,seated=True)
  if w=='cafe':fig+=actor('friend',1340,970,.95,'#437daf',True)
  if w=='office' and a in ['boss','joke','jokereprise']:fig+=actor('colleague',1400,970,.90,'#8a637a')
  fg+=table()
  if w in ['kitchen','stock','office']:
   screen=laptop('report' if w in ['office','kitchen'] else 'chart')
   if a in ['money','chart','repeat']:screen=screen.replace('101,28 €','100,00 €')
   fg+=screen+screen_overlay(a)
  if w in ['kitchen','cafe']:fg+=cup('cup',830,755)+cup('friend-cup',1245,755,1)
  if w=='kitchen':fg+=g(path('M0 0Q68-32 179 0Q132 41 32 34Z','#744735')+path('M30 0Q90 14 144 7',stroke='#a5754c',sw=8),'transform="translate(849 764)" data-anim="coffee-spill" style="opacity:0"')
  if w=='stock' and a in ['lotto','horizon']:
   fg+=g(rect(-145,-104,290,169,'#fff0d2',8)+text(0,-58,'LOTTO',34,'#507e7c',800,'middle')+text(0,-9,'ZIEHUNG 20:00',27,INK,800,'middle')+text(0,35,'JETZT 14:28' if a=='lotto' else '+60 s: 14:29',24,'#507e7c',700,'middle'),'transform="translate(1290 720) rotate(-7)"')
  if w=='cafe':fg+=envelope()
  if a=='gift':fg+=g(rect(-85,-95,170,119,'#bd8067',10)+rect(-95,-107,190,27,'#cf9b7b',6)+rect(-12,-108,24,132,AMBER)+path('M0-109Q-97-165-57-174Q-19-169 0-109Q25-179 62-171Q91-154 0-109Z',AMBER,INK,3),'transform="translate(1040 750)"')
  if w=='dinner':
   fg+=food()
   if a not in ['message','call']:fg+=g(rect(-50,-98,100,197,INK,12)+rect(-41,-81,82,165,'#abbfc3',6),'transform="translate(870 770) rotate(-10) scale(1 .32)" data-anim="table-phone"')
   if a in ['message','call']:
    fg+=phone_large('message' if a=='message' else 'call')+g(path('M1000 1100L1112 810L1120 680',stroke=HOOD,sw=97)+ellipse(1120,676,44,44,INK),'data-anim="phone-grip"')
  if a=='friendcall':
   # A real call from the friend's room, rather than returning to a shared cafe.
   fig=actor('friend',1340,970,.95,'#437daf',True)
   fg+=g(rect(-25,-45,50,92,'#344b54',7,extra='stroke="#fff4dc" stroke-width="3"')+rect(-17,-31,34,59,'#abc8ce',4),'transform="translate(1420 425) rotate(13)"')
 elif w=='station':
  b+=station(p)
  if a=='board':
   tr=train();inside=actor('hero-inside',960,970,.9)
   tr=tr.replace('<g data-anim="door-left"',inside+'<g data-anim="door-left"',1);b+=tr
   fig+=actor('hero',960,970,.9)
  else:
   b+=train()
   if a=='run':fig+=actor('hero',420,970,.9)
 elif w=='living':
  b+=room(p,True) if a=='reaction' else living(p)
  if a in ['football','reaction','limited']:
   fig+=actor('hero',620,1190,.82,seated=True)
  if a in ['bet','pending']:
   fg+=phone_large('bet')+g(path('M1000 1100L1112 810L1120 680',stroke=HOOD,sw=97)+ellipse(1120,676,44,44,INK),'data-anim="phone-grip"')
   if a=='pending':extra+=g(rect(490,850,940,107,INK,18)+text(960,921,'TOR ABERKANNT · WETTE WEITER OFFEN',38,CREAM,800,'middle'),'data-anim="pending-label"')
 # Spatial world and foreground share the camera. Graphic accents stay in screen space.
 body=g(b+fig+fg,f'data-anim="camera"')
 body+=rect(0,0,1920,1080,AMBER,extra=f'opacity="{.065 if s["future"] else 0}" data-anim="future-tint"')+extra
 body+=rect(0,0,1920,1080,f'url(#{p}-shade)')
 return '<svg viewBox="0 0 1920 1080" width="1920" height="1080" aria-hidden="true" data-layout-ignore>'+body+'</svg>'

def write_scene(s):
 name=s['id'];du=s['duration'];headline=s['accent'];large=len(headline)<21
 accent=f'<div class="accent-space"><div class="accent-mask"><h2 class="accent" style="font-size:{100 if large else 76}px">{esc(headline)}</h2><span class="accent-line"></span></div></div>' if headline else ''
 future='<div class="future-label"><strong>VORAUSBLICK</strong><span>+60 SEKUNDEN</span></div>' if s['future'] else ''
 credits=''
 if s['start']>325:
  credits='<div class="credits"><p>Musik: The Descent · Carefree · Dream Culture — Kevin MacLeod (incompetech.com)</p><p>CC BY 4.0 · creativecommons.org/licenses/by/4.0/ · Ausschnitte, Blenden, Pegelanpassung</p></div>'
 cfg={**s,'duration':du}
 h=f'''<template id="{name}-template"><div id="{name}" data-composition-id="{name}" data-start="0" data-duration="{du}" data-width="1920" data-height="1080" class="shot" style="width:1920px;height:1080px;position:relative;overflow:hidden;background:#d8c8af">{illustration(s)}{accent}{future}{credits}<script>window.__timelines=window.__timelines||{{}};window.__timelines[{json.dumps(name)}]=window.DynamicScene(document.getElementById({json.dumps(name)}),{json.dumps(cfg,ensure_ascii=False)});</script></div></template>'''
 (R/'compositions'/f'{name}.html').write_text(h)

def main():
 scenes=align();(R/'production/scenes.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2)+'\n')
 for s in scenes:write_scene(s)
 hosts=''.join(f'<div id="host-{s["id"]}" class="clip scene-host" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-width="1920" data-height="1080" data-track-index="{i%2+1}" style="z-index:{i+1}"></div>' for i,s in enumerate(scenes))
 css='''@font-face{font-family:Manrope;src:url('assets/fonts/Manrope.ttf') format('truetype');font-weight:200 800;font-display:block}*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#d8c8af;font-family:Manrope,sans-serif}#film{width:1920px;height:1080px;position:relative;overflow:hidden}.scene-host{position:absolute;inset:0;width:1920px;height:1080px}.shot svg{position:absolute;inset:0;font-family:Manrope,sans-serif}.accent-space{position:absolute;inset:0;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;width:100%;height:100%;padding:78px 116px;gap:12px;pointer-events:none}.accent-mask{max-width:1330px;overflow:hidden;padding:8px 12px 18px 4px}.accent{margin:0;max-width:1280px;line-height:1.09;letter-spacing:-.045em;font-weight:800;color:#ffc255;-webkit-text-stroke:5px #17151d;paint-order:stroke fill;text-shadow:0 4px 3px #17151d33}.accent-line{display:block;margin-top:14px;width:320px;height:7px;border-radius:5px;background:#ffc255;transform-origin:left center}.future-label{position:absolute;inset:64px 102px auto auto;background:#17151d;border:2px solid #ffc255;border-radius:16px;padding:15px 23px;display:flex;flex-direction:column;gap:6px;color:#fff4dc;align-items:center}.future-label strong{color:#ffc255;font-size:28px;letter-spacing:2px}.future-label span{font-size:28px;font-weight:800}.credits{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:0 65px 18px;gap:3px;pointer-events:none}.credits p{margin:0;line-height:1.25;font-size:28px;font-weight:600;color:#fff4dc;-webkit-text-stroke:3px #17151d;paint-order:stroke fill}'''
 root=f'''<!doctype html><html lang="de" data-resolution="landscape"><head><meta charset="utf-8"><meta name="viewport" content="width=1920,height=1080"><script src="assets/vendor/gsap.min.js"></script><script src="assets/actor-rig.js"></script><script src="assets/stage.js"></script><style>{css}</style></head><body><div id="film" data-composition-id="whatif-dynamic" data-start="0" data-duration="{DURATION}" data-width="1920" data-height="1080" data-fps="30">{hosts}<audio id="mark-voice" src="assets/audio/voice.wav" data-start="0" data-duration="{DURATION}" data-track-index="20" data-volume="1"></audio><audio id="music-fx" src="assets/audio/score-fx.wav" data-start="0" data-duration="{DURATION}" data-track-index="21" data-volume="1"></audio></div><script>window.__timelines=window.__timelines||{{}};window.__timelines['whatif-dynamic']=gsap.timeline({{paused:true}});</script></body></html>'''
 (R/'index.html').write_text(root)
 lengths=[s['duration']-.22 for s in scenes[:-1]]+[scenes[-1]['duration']]
 (R/'production/edit-summary.json').write_text(json.dumps({'duration':DURATION,'shots':len(scenes),'mean_shot_seconds':sum(lengths)/len(lengths),'min_shot_seconds':min(lengths),'max_shot_seconds':max(lengths),'worlds':sorted(set(s['world'] for s in scenes)),'future_rule':'Single moment, own perspective, now + 60 seconds; conditional on current course.'},indent=2)+'\n')
 print('Authored',len(scenes),'shots; mean',round(sum(lengths)/len(lengths),2),'seconds; total',DURATION)
 print('Lowest anchor match',min(s['match'] for s in scenes))
if __name__=='__main__':main()
