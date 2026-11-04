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
 bg+=rect(-150,624,2250,40,'#c7c2b6')+path('M-150 655H2100',stroke='#e8dfcc',sw=13)+rect(-2200,665,6400,280,f'url(#{p}-road)')+path('M-200 754H2100',stroke='#d9d2bd',sw=5,extra='stroke-dasharray="81 60" opacity=".7"')
 for i in range(8):
  t=(i+.05)/8;u=t+.07
  coords=[]
  for v in [t,u]:
   y=937+(668-937)*v;x=970+(1150-970)*v;w=260+(179-260)*v;coords.append(((x-w/2,y),(x+w/2,y)))
  a,b=coords;bg+=f'<polygon points="{a[0][0]},{a[0][1]} {a[1][0]},{a[1][1]} {b[1][0]},{b[1][1]} {b[0][0]},{b[0][1]}" fill="#eee9d9"/>'
 bg+=path('M555 680L528 925',stroke='#e9e2ce',sw=10)+rect(-2200,950,6400,650,'#bfb8a8')+path('M-200 946H2150',stroke='#eee4cd',sw=13)+path('M-200 957H2150',stroke='#8b8880',sw=6)
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
 else:body+=path('M-52-258H49L62-219H-65Z','#de8c0c' if color==HOOD else '#34658f')+path('M-25-474L-28-327M24-474L27-327',stroke=CREAM,sw=5,extra='data-part="drawstrings"')+path('M-28-330V-316M27-330V-316',stroke=CREAM,sw=8,extra='data-part="drawstrings"')
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
