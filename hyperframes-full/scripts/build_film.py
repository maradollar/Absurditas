"""Author the full HyperFrames film as editable HTML/SVG sub-compositions."""
from pathlib import Path
import json,html,math,re

R=Path(__file__).resolve().parents[1];DURATION=303.0
INK='#17151d';CREAM='#fff4dc';AMBER='#ffc255';HOOD='#ffa308'
def esc(x):return html.escape(str(x),quote=True)
def tag(name,attrs='',inside=''):return f'<{name} {attrs}>{inside}</{name}>'
def path(d,fill='none',stroke=None,sw=3,extra=''):
 return f'<path d="{d}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '')+f' {extra}/>'
def rect(x,y,w,h,fill,rx=0,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'
def text(x,y,t,size=30,fill=INK,weight=800,anchor='start',extra=''):return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(t)}</text>'
def ellipse(x,y,rx,ry,fill,extra=''):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'
def g(content,extra=''):return f'<g {extra}>{content}</g>'
def window(x,y,w=100,h=145):
 return g(rect(-7,-7,w+14,h+17,'#e9dfcc')+rect(0,0,w,h,'#b6d4e2')+path(f'M{w/2} 0V{h}',stroke='#efe6d7',sw=7)+path(f'M8 15L{w-15} 9V29L8 40Z','#d4e7e6')+path(f'M-13 {h+12}H{w+13}',stroke='#baaa93',sw=7),f'transform="translate({x} {y})"')
def defs(p):
 return f'''<defs>
 <linearGradient id="{p}-sky" x2="0" y2="1"><stop stop-color="#c5d1d0"/><stop offset="1" stop-color="#eee1c8"/></linearGradient>
 <linearGradient id="{p}-road" x2="0" y2="1"><stop stop-color="#929795"/><stop offset="1" stop-color="#7d8589"/></linearGradient>
 <radialGradient id="{p}-shade"><stop offset=".5" stop-color="#493b31" stop-opacity="0"/><stop offset="1" stop-color="#493b31" stop-opacity=".13"/></radialGradient>
 <linearGradient id="{p}-hood" x2="1" y2="0"><stop stop-color="#ffb52b"/><stop offset=".6" stop-color="#ffa308"/><stop offset="1" stop-color="#ed9108"/></linearGradient>
 <clipPath id="{p}-rain-clip"><rect x="1360" y="-200" width="1000" height="1600"/></clipPath>
 <pattern id="{p}-paper" width="11" height="13" patternUnits="userSpaceOnUse"><circle cx="2" cy="4" r=".7" fill="#fff4dc" opacity=".065"/></pattern>
 </defs>'''
def tree(x,y,s=1):
 return g(path('M-12 0L-6-158L9-186L17 0Z','#87755b')+path('M0-112L-46-191M3-145L50-197',stroke='#87755b',sw=12)+g(path('M-91-165Q-130-202-93-239Q-94-292-41-291Q-11-328 31-300Q86-315 99-271Q139-253 117-211Q131-164 79-151Q27-118-11-145Q-57-127-91-165Z','#7c9f77')+path('M-73-240Q-49-283-15-268Q15-294 45-271',stroke='#98b38a',sw=15),'data-part="tree-crown"'),f'transform="translate({x} {y}) scale({s})"')
def lamp(p,green=False):
 return g(path('M0 0V-294',stroke='#585c5f',sw=13)+rect(-34,-321,68,139,'#303b40',12)+rect(-25,-312,50,56,'#6d403b',5,extra='data-part="lamp-red-bg"')+rect(-25,-247,50,56,'#304b42',5,extra='data-part="lamp-green-bg"')+g(ellipse(0,-297,6,6,'#ff8875')+path('M-8-286H8V-272H4V-257H-2V-272H-8Z','#ff8875'),'data-part="lamp-red"')+g(ellipse(0,-234,6,6,'#b9f2bb')+path('M-1-224L7-218L17-215L14-208L3-213L0-204L11-193L5-187L-6-200L-14-188L-21-193L-10-212L-17-205L-23-210Z','#b9f2bb'),'data-part="lamp-green" style="opacity:0"'),f'transform="translate(1270 650) scale(.94)"')
def street(p):
 bg=rect(-1800,-1000,5400,2800,f'url(#{p}-sky)')
 for i in range(7):
  x=i*355-150;bg+=rect(x,65+i%3*35,285,560,'#c8c5b9')
  for j in range(3):bg+=rect(x+25+j*77,170,42,95,'#bfd0cd',extra='opacity=".55"')
 bg+=rect(-120,230,600,395,'#deceb6')+rect(540,155,585,470,'#e9dbc5')+path('M1125 155L1185 196V625H1125Z','#c4b49a')+rect(1190,225,270,400,'#ded0ba')
 for x in [-10,160,330]:bg+=window(x,290,90,130)
 for x in [585,780,975]:bg+=window(x,223,105,123)
 for x in [1225,1355]:bg+=window(x,286,73,106)
 bg+=rect(-20,470,400,160,'#b6d4e2')+path('M-35 471H407L385 434H-23Z','#d0a550')+path('M117 481V628M277 481V628',stroke='#eee2cd',sw=13)
 bg+=rect(582,411,490,212,'#b6d4e2')+path('M582 411V625M744 411V625M914 411V625M1073 411V625',stroke='#f0e4d1',sw=13)
 bg+=path('M554 411H1104L1081 365H570Z','#be7d66')+rect(554,409,550,18,'#9d6655')+rect(769,306,135,42,'#af977b',5)+text(837,336,'CAFÉ',25,CREAM,700,'middle',extra='letter-spacing="4"')
 bg+=rect(1208,458,225,166,'#bed8dd')+path('M1190 455H1455L1439 415H1209Z','#688e8c')+path('M1320 464V624',stroke='#eee2cd',sw=11)
 bg+=path('M1460 660L1525 296H1650L1827 660Z','#a4a7a1')+path('M1610 350L1632 407M1649 449L1670 503M1690 551L1712 609',stroke='#d9d2bd',sw=5)+rect(1830,265,300,365,'#e4d6bd')+tree(1890,635,1.1)
 bg+=rect(-150,624,2250,40,'#c7c2b6')+path('M-150 655H2100',stroke='#e8dfcc',sw=13)+rect(-200,665,2400,280,f'url(#{p}-road)')+path('M-200 754H2100',stroke='#d9d2bd',sw=5,extra='stroke-dasharray="81 60" opacity=".7"')
 for i in range(8):
  t=(i+.05)/8;u=t+.07
  coords=[]
  for v in [t,u]:
   y=937+(668-937)*v;x=970+(1150-970)*v;w=260+(179-260)*v;coords.append(((x-w/2,y),(x+w/2,y)))
  a,b=coords;bg+=f'<polygon points="{a[0][0]},{a[0][1]} {a[1][0]},{a[1][1]} {b[1][0]},{b[1][1]} {b[0][0]},{b[0][1]}" fill="#eee9d9"/>'
 bg+=path('M555 680L528 925',stroke='#e9e2ce',sw=10)+rect(-200,950,2400,650,'#bfb8a8')+path('M-200 946H2150',stroke='#eee4cd',sw=13)+path('M-200 957H2150',stroke='#8b8880',sw=6)
 for x in range(-100,2300,260):bg+=path(f'M{x} 960L{x-80} 1200',stroke='#aaa291',sw=1.6)
 bg+=path('M-100 1045H2150',stroke='#aaa291',sw=1.6)
 bg+=g(path('M0 0V-320',stroke='#596066',sw=13)+rect(-34,-380,68,160,'#343b40',15)+ellipse(0,-349,19,19,'#df7961')+ellipse(0,-297,18,18,'#5d5349')+ellipse(0,-248,18,18,'#43564b'),'transform="translate(535 650)"')+lamp(p)
 return bg
def cafe(p,exterior=False):
 if exterior:
  b=rect(-500,-500,3000,2000,'#d6cdbb')+rect(0,160,1090,680,'#e9dbc6')+rect(130,355,780,480,'#bed9de')
  b+=path('M140 360V840M470 360V840M905 360V840M140 580H905',stroke='#f0e6d3',sw=17)+path('M1060 840V340H1295V840Z','#b49d83')+rect(1090,375,170,460,'#b5d0d5')+path('M1215 610V650',stroke='#74695e',sw=9)
  b+=rect(-200,840,2300,550,'#bfb7a6')+path('M-100 1020H2100',stroke='#e8dfcc',sw=12)+rect(-100,1027,2200,400,'#8c9294')+tree(1680,836,.95)
  b+=path('M80 340H1330L1250 180H160Z','#537d78')+rect(80,335,1250,35,'#426761')
  for x in range(140,1280,130):b+=path(f'M{x} 180L{x-60} 337',stroke='#a4b6a0',sw=36)
  b+=text(710,290,'CAFÉ',62,CREAM,800,'middle',extra='letter-spacing="10"')+path('M90 370V845M1320 370V845',stroke='#575b53',sw=12)
  return b
 b=rect(-700,-500,3300,2100,'#e6d8c2')+rect(-80,785,2100,600,'#b39b80')
 for x in range(-100,2200,250):b+=path(f'M{x} 789L{x-110} 1200',stroke='#9e866d',sw=2)
 b+=path('M-200 888H2100M-200 1030H2100',stroke='#a48b71',sw=2)
 b+=rect(75,120,540,595,'#f6ead4',10)+rect(96,141,498,551,'#bfd7dd')+path('M342 145V694M99 421H592',stroke='#eee2c9',sw=13)
 b+=g(rect(105,465,480,220,'#d5c2a5')+path('M107 515H580L558 476H123Z','#ae7460')+rect(150,538,370,130,'#bed6db'),'opacity=".7"')
 b+=rect(740,185,390,270,'#58766e',14)+rect(753,198,364,244,'#3b5b54',9)+text(935,268,'HEUTE',34,CREAM,700,'middle')+path('M812 300H1055M812 344H1000M812 387H1040',stroke='#d0dbbd',sw=8,extra='opacity=".65"')
 b+=rect(1490,126,365,657,'#b09a80',12)+rect(1511,148,323,602,'#b7d1d5',5)+path('M1774 440V496',stroke='#715d48',sw=10)+text(1670,234,'CAFÉ',35,CREAM,700,'middle')
 b+=path('M1220 330H1450',stroke='#86715c',sw=16)
 for x in [1260,1375]:b+=path(f'M{x-18} 330Q{x-15} 251 {x} 241Q{x+36} 260 {x+29} 330Z','#61846c')+path(f'M{x} 319Q{x-40} 274 {x-48} 293M{x+3} 300Q{x+36} 260 {x+48} 281',stroke='#54745e',sw=12)+rect(x-25,317,57,58,'#b47e62',5)
 b+=path('M760 0V87M1385 0V87',stroke='#766656',sw=5)
 for x in [760,1385]:b+=path(f'M{x-86} 126Q{x-60} 56 {x} 68Q{x+60} 56 {x+86} 126Z','#c99d58')+ellipse(x,126,86,14,'#ebc37b')
 return b
def chair(x):return g(path('M-73-96V-242Q-70-268-43-268H56Q81-266 81-242V-92Z','#786650',INK,3)+rect(-87,-114,190,20,'#947b5b',5)+path('M-64-99L-86 22M76-99L99 22',stroke='#6d5b49',sw=13),f'transform="translate({x} 940)"')
def table():return path('M820 790L790 1080M1320 790L1360 1080',stroke='#75604c',sw=21)+ellipse(1075,791,356,62,'#936f4e')+ellipse(1075,779,356,53,'#bf9b70')+path('M744 798Q1060 867 1404 800',stroke='#866346',sw=9)
def cup(name,x=830,y=755,flip=-1):
 return g(ellipse(0,36,48,13,'#716354','opacity=".17"')+path('M-29-24H28L23 26Q0 39-24 26Z','#fff0d2',INK,2.5)+path(f'M{flip*28}-13Q{flip*60}-14 {flip*49} 13Q{flip*38} 24 {flip*27} 12',stroke='#efe0bd',sw=12)+ellipse(0,-24,29,9,'#efdebd')+ellipse(0,-24,22,5,'#6d4334',extra='data-part="coffee-level"')+path('M-18-9V15',stroke='#fff9ea',sw=4),f'data-prop="{name}" transform="translate({x} {y})"')
def car(p):
 b=ellipse(0,70,390,27,'#4d5058','opacity=".2"')+path('M-380 19L-356-59Q-350-82-311-84H-181L-96-201Q-83-224-53-226H152Q182-226 206-194L284-83L365-65Q390-62 399-18L403 45H-382Z','#b26959',INK,4)
 b+=path('M-146-87L-74-193H19V-87Z','#5b6e78',INK,5)+path('M43-193H145Q164-192 178-173L239-87H43Z','#566b76',INK,5)+path('M-341-56H-295V-17H-348Z','#d77d67')+path('M356-48L383-41L390-10H355Z','#f8dc9d')+path('M-265-62H304V24H-267Z','#b26b5c')+path('M30-63V27M260-63V28',stroke='#8d554d',sw=3)+path('M67-42H107',stroke='#dd9b83',sw=5)
 for x in [-233,238]:
  wheel=ellipse(0,0,58,58,'#303640')+ellipse(0,0,42,42,'#62717b')+ellipse(0,0,31,31,'#b0bab8')
  for a in range(0,360,60):wheel+=path(f'M{math.cos(math.radians(a))*9} {math.sin(math.radians(a))*9}L{math.cos(math.radians(a))*29} {math.sin(math.radians(a))*29}',stroke='#667681',sw=8)
  wheel+=ellipse(0,0,10,10,'#c3c6bf');b+=g(wheel,f'data-part="wheel" data-wheel-x="{x}" transform="translate({x} 34)"')
 return g(b,'data-prop="car" transform="translate(2400 805) scale(1.1)"')
def phone():
 b=rect(-61,-117,122,234,'#242932',15)+rect(-53,-100,106,198,'#d7e1dd',8)+rect(-18,-109,36,6,'#87999e',3)+ellipse(0,107,4,4,'#7a8a91')
 def ui(mode,outgoing,incoming='',cool=False):
  q=rect(-51,-98,102,27,'#507e7c',5)+text(0,-80,'LEO',12,CREAM,800,'middle')
  q+=rect(-42,-49,87,54,'#e7bd6a',8)+text(-35,-29,outgoing[0],10,INK,600)
  if len(outgoing)>1:q+=text(-35,-14,outgoing[1],10,INK,600)
  if incoming:
   q+=rect(-44,19,86,47,'#cbd9d2' if cool else '#a7ccad',8)
   q+=text(-36,38,incoming[0],11,INK,700)
   if len(incoming)>1:q+=text(-36,53,incoming[1],11,INK,700)
  else:q+=rect(-44,62,87,24,'#fff5df',5)+text(-35,78,'SENDEN',10,'#507e7c',800)
  return g(q,f'data-ui="{mode}" style="opacity:{1 if mode==0 else 0}"')
 b+=g(rect(-51,-98,102,196,'#a9c6ce',8)+path('M-42-75L33-9M-41-40L40 22',stroke='#d9e8e3',sw=6),'data-ui="5" style="opacity:0"')
 b+=ui(0,['Typisch du.'])+ui(1,['Typisch du.'],['Nicht','witzig.'],True)+ui(2,['Alles okay','bei dir?'])+ui(3,['Alles okay','bei dir?'],['Danke dir!'])+ui(4,['Alles okay','bei dir?'],['Gesendet.'])
 b+=g(path('M-3-8L-37-69L-24-97M-3-8L43-65M-3-8L48 9M-3-8L-18 42L-42 71M-18 42L30 94M-3-8L-46 0',stroke=CREAM,sw=3),'data-part="phone-cracks" style="opacity:0"')
 return g(b,'data-prop="phone" transform="translate(856 655)" style="opacity:0"')
def actor(name,x=820,y=970,s=.9,color=HOOD,seated=False,apron=False):
 # Every limb exists in authored markup; runtime only changes its coordinates.
 b=ellipse(0,14,106,14,'#675d51','opacity=".18"')
 for side in ['back','front']:
  b+=path('M0-202L0-100L0 0',stroke='#efd6ad',sw=27,extra=f'data-part="{side}-leg-rim"')+path('M0-202L0-100L0 0',stroke=INK,sw=22,extra=f'data-part="{side}-leg"')+path('M-20 0Q0-12 22 0L34 11H-23Z',INK,INK,2,extra=f'data-part="{side}-shoe"')
 body=''
 for side in ['back','front']:
  arm=path('M0 0L1 1',stroke='#ffe0af',sw=48,extra=f'data-part="{side}-arm-rim"')+path('M0 0L1 1',stroke=INK,sw=44,extra=f'data-part="{side}-arm-outline"')+path('M0 0L1 1',stroke=color,sw=37,extra=f'data-part="{side}-arm"')
  if side=='back':body+=arm
  else:frontarm=arm
 body+=path('M-61-472Q-62-523-10-526Q42-529 66-482L52-451Z','#dd8d09' if color==HOOD else color,INK,4)
 body+=path('M-66-488Q-20-503 21-495Q65-491 74-457L85-208Q0-196-91-211L-79-456Q-84-479-66-488Z','#ffe0af','#ffe0af',9)
 body+=path('M-66-488Q-20-503 21-495Q65-491 74-457L85-208Q0-196-91-211L-79-456Q-84-479-66-488Z',color,INK,4)
 body+=path('M-65-457V-223',stroke='#ffd488' if color==HOOD else '#83a7ba',sw=4)
 if apron:body+=path('M-53-407H48L68-213H-70Z','#627b6d')+path('M-38-446L-43-402M35-446L38-403',stroke='#627b6d',sw=14)
 else:body+=path('M-52-258H49L62-219H-65Z','#de8c0c' if color==HOOD else '#34658f')+path('M-25-474L-28-327M24-474L27-327',stroke=CREAM,sw=5)+path('M-28-330V-316M27-330V-316',stroke=CREAM,sw=8)
 body+=path('M-14-529H14V-480H-14Z',INK)+frontarm
 for side in ['back','front']:body+=g(ellipse(-4,-4,23,23,'#ffe0af')+ellipse(0,0,21,21,INK),f'data-part="{side}-hand"')
 face=ellipse(-5,-4,96,96,'#ffe0af')+ellipse(0,0,94,94,INK)
 eyes=ellipse(-23,-9,7.5,10,CREAM,extra='data-part="eye-left"')+ellipse(23,-9,7.5,10,CREAM,extra='data-part="eye-right"')+path('M-33-35L-15-37M14-37L32-35',stroke=CREAM,sw=5,extra='data-part="brows"')+path('M-11 29Q0 35 13 28',stroke=CREAM,sw=4,extra='data-part="mouth"')
 face+=g(eyes,'data-part="gaze"');body+=g(face,'data-part="head" transform="translate(0 -600)"')
 b+=g(body,'data-part="body"')
 b+=ellipse(0,0,3,3,'#ab5c37','data-part="stain" style="opacity:0"')
 return g(b,f'data-actor="{name}" data-color="{color}" data-seat="{1 if seated else 0}" transform="translate({x} {y}) scale({s})" data-x="{x}" data-y="{y}" data-scale="{s}"')
def fallen():
 b=ellipse(270,99,360,33,'#46474b','opacity=".23"')
 b+=path('M310 61L425 31L556 45M310 81L425 102L556 100',stroke=INK,sw=23)+path('M548 35L580 46V58H542Z',INK)+path('M549 91L584 99V111H542Z',INK)
 b+=path('M94 18L144 115L198 102',stroke=INK,sw=39)+path('M94 18L144 115L198 102',stroke=HOOD,sw=31)
 b+=path('M63-4Q116-18 163-3L314 23L311 95L153 103L85 83Q66 55 63-4Z',HOOD,INK,4)+path('M90 11L153 23M91 28L152 43',stroke=CREAM,sw=5)+path('M77 26L112 68L72 112',stroke=INK,sw=39)+path('M77 26L112 68L72 112',stroke=HOOD,sw=31)+ellipse(72,112,22,22,INK)+ellipse(201,102,21,21,INK)
 b+=ellipse(-5,-3,94,94,'#ffe0af')+ellipse(0,0,92,92,INK)+path('M-31-8q10 8 20 0M12-8q10 8 20 0M-10 29Q0 34 12 28',stroke=CREAM,sw=4)
 return g(b,'data-prop="fallen" transform="translate(856 787) scale(.83)"')
def extras(kind,p):
 b=''
 if kind in ['cafe','messages','repeat','conversation','departure','restore','choice','finish','money','horizon']:
  b+=chair(640)+chair(1340)
  b+=actor('hero',640,970,.95,seated=True)
  if kind not in ['money','horizon','messages']:b+=actor('friend',1340,970,.95,'#437daf',True)
  b+=table()+ellipse(830,790,57,13,'#e9d8b7','data-prop="saucer"')+cup('cup',830,755)+cup('friend-cup',1245,755,1)+phone()
  if kind=='cafe':b+=actor('waiter',-400,1040,1.08,'#f1e1c1',False,True)
  b+=g(ellipse(0,0,112,17,'#8b999d')+path('M-100 0Q0 20 100 0',stroke='#d7dcda',sw=6)+rect(-23,-24,38,28,'#e5d1ae',4),'data-prop="tray" transform="translate(-200 785)" style="opacity:0"')
  b+=path('M0 0C-50 0-90 50-110 70',stroke='#704937',sw=10,extra='data-prop="spill" style="opacity:0"')
  if kind in ['money','horizon']:
   laptop=path('M-170 0L-150-184H146L167 0Z','#47575d',INK,5)+rect(-136,-168,266,145,'#c8dfd9',7)+path('M-128-51L-94-73L-54-58L-23-101L13-82L50-134L89-117L120-146',stroke='#508671',sw=7)+path('M-186 0H184L220 30H-221Z','#9caaa9',INK,3)+text(0,-139,'BEISPIEL',15,'#43685d',800,'middle')
   b+=g(laptop,'data-prop="laptop" transform="translate(1070 762)"')
   for i in range(3):b+=g(rect(-32,-40-i*9,64,23,'#caa155',8)+ellipse(0,-40-i*9,32,8,'#efd58a')+path('M-26-32V-19',stroke='#a87e38',sw=2),f'transform="translate({850+i*70} 763)"')
   b+=g(rect(-75,-70,150,117,'#fff0d2',4)+text(0,-33,'LOTTO',22,'#507e7c',800,'middle')+text(0,5,'?  ?  ?',28,INK,800,'middle'),'data-prop="ticket" transform="translate(1335 750) rotate(-11)" style="opacity:0"')
  bubble=text(1340,260,'Hörst du mir zu?',39,INK,800,'middle')
  b+=g(rect(1110,196,460,106,CREAM,24)+path('M1280 300L1302 338L1320 300Z',CREAM)+bubble,'data-prop="question-bubble" style="opacity:0"')
  apology=rect(230,190,570,150,CREAM,28)+path('M603 338L644 376L646 335Z',CREAM)+text(515,249,'Entschuldige.',40,INK,800,'middle')+text(515,303,'Erzähl noch mal.',40,INK,800,'middle')
  b+=g(apology,'data-prop="apology-bubble" style="opacity:0"')
 elif kind=='rain':
  b+=actor('hero',710,970,.94)+actor('passer',1750,975,.75,'#8a637a')
  rain=''
  for i in range(110):
   x=1390+(i*127)%1000;y=-200+(i*173)%1300
   rain+=path(f'M{x} {y}l-25 73',stroke='#dcebee',sw=3,extra='opacity=".65"')
  b+=g(g(rain,'data-prop="rain" style="opacity:0"'),f'clip-path="url(#{p}-rain-clip)"')+g(ellipse(0,0,160,11,'#a3bec5','opacity=".44"')+ellipse(160,30,90,6,'#a3bec5','opacity=".35"'),'data-prop="puddle" transform="translate(1590 974)" style="opacity:0"')
 else:
  b+=car(p)
  if kind in ['vision','phone','wheel']:b+=fallen()+phone()
  else:b+=actor('hero',820,970,.9)+phone()
  if kind in ['rules','limits']:b+=actor('friend',1390,970,.9,'#437daf')
  b+=g(path('M-10 0Q0-34 19-14Q32 9 0 27Z','#c99449')+path('M-7 20L21-16',stroke='#a57936',sw=2),'data-prop="leaf" transform="translate(1730 380)"')
  b+=g(ellipse(1035,850,85,24,'none',extra=f'stroke="{AMBER}" stroke-width="5"')+path('M1470 240Q1450 481 1054 800M1046 775L1054 800L1080 785',stroke=AMBER,sw=6),'data-prop="danger" style="opacity:0"')
 return b

SCENES=[
 ('opening',0,1.98,'street'),('vision',1.78,5.72,'vision'),('phone',5.42,8.98,'phone'),('wheel',8.82,11.98,'wheel'),
 ('safe',11.68,17.65,'safe'),('crossing',17.34,28.48,'crossing'),('reflection',28.02,40.92,'reflection'),
 ('rule-window',40.5,56.88,'rules'),('limits',56.5,73.56,'limits'),('decision',73.2,88.68,'decision'),
 ('cafe-cup',88.24,110.8,'cafe'),('rain',110.4,130.56,'rain'),('money',130.2,148.4,'money'),('horizon',148,169.4,'horizon'),
 ('messages',169,192.05,'messages'),('repeat',191.7,203.65,'repeat'),('conversation',203.3,225.45,'conversation'),
 ('departure',225.1,238.6,'departure'),('restore',238.24,255.98,'restore'),('choice',255.6,269.05,'choice'),
 ('street-reprise',268.7,279.72,'reprise'),('finish',279.34,DURATION,'finish')]

def scene_html(s):
 name,start,end,kind=s;p=name;dur=round(end-start,5)
 indoors=kind in ['cafe','money','horizon','messages','repeat','conversation','departure','restore','choice','finish']
 bg=cafe(p) if indoors else cafe(p,True) if kind=='rain' else street(p)
 markup=f'<svg viewBox="0 0 1920 1080" width="1920" height="1080" aria-label="{esc(name)}" data-layout-ignore>{defs(p)}<g data-part="camera"><g data-part="background">{bg}</g>{extras(kind,p)}</g><rect width="1920" height="1080" fill="url(#{p}-shade)"/><rect width="1920" height="1080" fill="url(#{p}-paper)"/><rect data-part="future-wash" width="1920" height="1080" fill="#bdd3dc" opacity="0"/></svg>'
 markup+=f'<div class="vision-tag" data-part="vision-tag" data-layout-allow-overlap>VORAUSBLICK <span>+60 SEKUNDEN</span></div>'
 config={'id':name,'kind':kind,'start':start,'duration':dur}
 return f'''<template id="{name}-template"><div id="{name}-scene" data-composition-id="{name}" data-width="1920" data-height="1080" data-start="0" data-duration="{dur}">
 <style>#{name}-scene{{width:1920px;height:1080px;overflow:hidden;background:#d8c8af;font-family:Manrope,sans-serif;position:relative}}#{name}-scene .scene-content{{width:100%;height:100%;padding:0;display:flex;flex-direction:column;gap:0;box-sizing:border-box}}#{name}-scene svg{{position:absolute;inset:0}}#{name}-scene .vision-tag{{position:absolute;right:150px;top:86px;padding:15px 23px;background:#17151d;color:#ffc255;border:2px solid #ffc255;border-radius:12px;font-size:28px;font-weight:800;letter-spacing:2px;opacity:0}}#{name}-scene .vision-tag span{{display:block;margin-top:6px;font-size:28px;color:#fff4dc;letter-spacing:1px}}</style>
 <div class="scene-content">{markup}</div>
 <script>(function(){{const root=document.getElementById('{name}-scene');const tl=window.WhatIfFilm.scene(root,{json.dumps(config)});window.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;}})();</script>
 </div></template>'''

# Typography cues are short semantic accents, not a complete wall of subtitles.
CUES=[
 (.50,1.65,'EINE AMPEL.',0), (1.78,3.20,'PLÖTZLICH.',0), (3.70,5.18,'AUF DEM ASPHALT.',0),
 (6.50,8.23,'ZERBROCHEN.',0), (9.46,11.25,'QUIETSCHENDE REIFEN.',0), (12.94,14.28,'VERSCHWUNDEN.',0),
 (18.74,20.00,'GRÜN.',1),(21.54,22.66,'NICHT LOS.',0),(25.32,27.90,'GENAU DORT.',0),
 (30.10,31.80,'ZUKUNFT GESEHEN.',0),(32.38,33.70,'VERÄNDERT.',1),(38.44,40.34,'1 MINUTE VORAUS.',0),
 (50.06,53.05,'60 SEKUNDEN.',0),(57.15,60.2,'KEINE GEDANKEN.',0),(61.1,63.9,'KEIN FERNBLICK.',0),
 (65.48,68.9,'KEINE ENDLOSSCHLEIFE.',0),(80.0,83.3,'DU ENTSCHEIDEST.',1),
 (89.96,91.70,'FÜHLT SICH FANTASTISCH AN.',0),(106.48,109.0,'KEIN KAFFEE AUF DIR.',1),
 (113.7,116.2,'REGEN.',0),(126.2,129.0,'GLÜCK? WISSEN.',0),(132.3,134.7,'GELD?',0),
 (148.8,152.1,'NÄCHSTE WOCHE? BLEIBT OFFEN.',0),(159.14,162.9,'IMMER VOM JETZT.',0),
 (169.4,172.1,'BEI MENSCHEN WIRD’S KOMPLIZIERT.',0),(178.94,181.0,'KURZ. KÜHL.',0),
 (187.1,188.8,'SCHON BESSER.',1),
 (222.0,224.9,'DER MOMENT LEIDET.',0),(229.1,232.0,'ER GEHT.',0),
 (249.7,253.0,'ZUKUNFT VERÄNDERT.',1),
 (259.0,263.3,'WANN HILFT DER NÄCHSTE BLICK?',0),(279.34,282.35,'1 MINUTE VORAUS.',0),
 (283.0,286.5,'DEINE ENTSCHEIDUNG.',1),(287.62,292.6,'IMMER NUTZEN? GRENZEN SETZEN?',0),
 (294.14,296.5,'SCHREIB’S IN DIE KOMMENTARE.',0),(300.28,303.0,'ABONNIEREN',1)]

def main():
 for s in SCENES:(R/'compositions'/f'{s[0]}.html').write_text(scene_html(s))
 hosts=[]
 for i,(name,start,end,kind) in enumerate(SCENES):
  hosts.append(f'<div id="host-{name}" class="clip scene-host" data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="{start}" data-duration="{round(end-start,5)}" data-width="1920" data-height="1080" data-track-index="{i%2+1}" data-track-kind="graphics" style="z-index:{i+1}"></div>')
 cue_nodes=[]
 for i,(a,b,copy,positive) in enumerate(CUES):
  size=112 if len(copy)<18 else 88 if len(copy)<29 else 76
  left=(a>=169 and a<214)
  maxwidth=650 if left else 1180
  if left and len(copy)>16:size=72
  alignment='align-items:flex-end;' if 169<=a<172 else ''
  cue_nodes.append(f'<div id="em-{i}" class="clip cue" data-start="{a}" data-duration="{b-a:.5f}" data-track-index="10" data-track-kind="captions" style="z-index:100"><div class="cue-space" style="max-width:1920px;{alignment}"><div class="word-mask" style="max-width:{maxwidth}px"><h2 class="cue-type" style="font-size:{size}px;color:{"#b9f2bb" if positive else "#ffc255"}">{esc(copy)}</h2><svg class="underline" viewBox="0 0 600 20" width="440" height="16"><path d="M7 11Q270 21 590 7" stroke="currentColor" stroke-width="8" fill="none" stroke-linecap="round"/></svg></div></div></div>')
 root=f'''<!doctype html><html lang="de" data-resolution="landscape"><head><meta charset="utf-8"><meta name="viewport" content="width=1920,height=1080">
 <script src="assets/vendor/gsap.min.js"></script><script src="assets/film-runtime.js"></script>
 <style>@font-face{{font-family:Manrope;src:url('assets/fonts/Manrope.ttf') format('truetype');font-weight:200 800;font-display:block}}*{{box-sizing:border-box}}html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#d8c8af;font-family:Manrope,sans-serif}}#root{{width:1920px;height:1080px;position:relative;overflow:hidden;background:#d8c8af}}.clip.scene-host{{position:absolute;inset:0;width:1920px;height:1080px}}.cue{{position:absolute;inset:0;pointer-events:none}}.cue-space{{width:100%;height:100%;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;padding:90px 145px;gap:12px}}.word-mask{{overflow:hidden;padding:8px 13px 17px 5px}}.cue-type{{font-family:Manrope,sans-serif;font-weight:800;line-height:1.12;letter-spacing:-.045em;margin:0;-webkit-text-stroke:5px #17151d;paint-order:stroke fill;text-shadow:0 5px 4px #17151d33}}.underline{{display:block;color:#ffc255;overflow:visible;margin-top:14px}}.credits{{position:absolute;inset:0;z-index:130;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;padding:0 90px 22px;gap:5px;pointer-events:none}}.credits p{{font-size:20px;color:#fff4dc;line-height:1.3;margin:0;-webkit-text-stroke:3px #17151d;paint-order:stroke fill;font-weight:600}}</style></head><body>
 <div id="root" data-composition-id="whatif-full" data-start="0" data-duration="{DURATION}" data-width="1920" data-height="1080" data-fps="30">
 {''.join(hosts)}{''.join(cue_nodes)}
 <div id="music-credits" class="clip credits" data-start="290" data-duration="13" data-track-index="12"><p>Musik: The Descent · Carefree · Dream Culture — Kevin MacLeod (incompetech.com)</p><p>CC BY 4.0 · creativecommons.org/licenses/by/4.0/ · Ausschnitte, Blenden und Pegelanpassung</p></div>
 <audio id="mark-voice" src="assets/audio/voice.wav" data-start="0" data-duration="{DURATION}" data-track-index="20" data-volume="1"></audio>
 <audio id="music-and-effects" src="assets/audio/score-fx.wav" data-start="0" data-duration="{DURATION}" data-track-index="21" data-volume="1"></audio>
 </div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
 {''.join(f"tl.from('#em-{i} .cue-type',{{y:68,opacity:0,duration:.36,ease:'power3.out'}},{a});{{const l=document.querySelector('#em-{i} .underline path');if(l){{const n=l.getTotalLength();l.style.strokeDasharray=n;tl.fromTo(l,{{strokeDashoffset:n}},{{strokeDashoffset:0,duration:.4,ease:'power2.out'}},{a+.16});}}}}tl.to('#em-{i} .word-mask',{{opacity:0,duration:.17,ease:'sine.in'}},{b-.17});" for i,(a,b,_,_) in enumerate(CUES))}
 window.__timelines['whatif-full']=tl;</script></body></html>'''
 # Keep all synchronized typography in one independently editable caption
 # composition, following HyperFrames' source structure rather than crowding
 # the root with dozens of nested text wrappers.
 root=root.replace('font-size:28px;font-weight:800;letter-spacing:2px;opacity:0','font-size:28px;font-weight:800;letter-spacing:2px;opacity:0')
 root=root.replace('font-size:20px;color:#fff4dc','font-size:28px;color:#fff4dc')
 credits=re.search(r'(<div id="music-credits".*?</div>)\s*<audio',root,re.S).group(1)
 caption_script=re.search(r"<script>window.__timelines=.*?</script>",root,re.S).group(0).replace("window.__timelines['whatif-full']","window.__timelines['emphasis']")
 emphasis=f'<template id="emphasis-template"><div id="emphasis-scene" data-composition-id="emphasis" data-start="0" data-duration="303" data-width="1920" data-height="1080" style="width:1920px;height:1080px;position:relative">'+''.join(cue_nodes)+credits+caption_script+'</div></template>'
 (R/'compositions/emphasis.html').write_text(emphasis)
 root=root.replace(''.join(cue_nodes),'<div id="emphasis-host" class="clip scene-host" data-composition-id="emphasis" data-composition-src="compositions/emphasis.html" data-start="0" data-duration="303" data-width="1920" data-height="1080" data-track-index="10" data-track-kind="captions" style="z-index:100"></div>')
 root=root.replace(credits,'<div id="finish-light" class="clip" data-start="302.3" data-duration=".7" data-track-index="13" style="position:absolute;inset:0;z-index:200;background:#f5e3c3;opacity:0;pointer-events:none"></div>')
 root=re.sub(r"<script>window.__timelines=.*?</script>","<script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});tl.fromTo('#finish-light',{opacity:0},{opacity:.12,duration:.7,ease:'sine.inOut'},302.3);window.__timelines['whatif-full']=tl;</script>",root,flags=re.S)
 (R/'index.html').write_text(root)
 (R/'production/scenes.json').write_text(json.dumps([{'id':s[0],'start':s[1],'end':s[2],'kind':s[3]} for s in SCENES],ensure_ascii=False,indent=2)+'\n')
 (R/'production/text-cues.json').write_text(json.dumps([{'start':a,'end':b,'text':c} for a,b,c,_ in CUES],ensure_ascii=False,indent=2)+'\n')
 print('Authored',len(SCENES),'HyperFrames scenes,',len(CUES),'text accents,',DURATION,'seconds')
if __name__=='__main__':main()
