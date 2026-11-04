"""Original illustrated sets. Shared coordinates preserve physical contact between shots."""
from art import *

def wall_clock(x,y,label='08:00'):
 return g(rect(-100,-43,200,86,INK,13)+text(0,15,label,44,CREAM,800,'middle',extra='data-anim="wall-time"'),f'transform="translate({x} {y})"')

def laptop(mode='chart'):
 b=path('M-224 0L-205-246H205L225 0Z','#3c5158',INK,6)+rect(-188,-229,376,204,'#e8eee2',8)
 b+=rect(-188,-229,376,35,'#507e7c',6)+ellipse(-168,-211,5,5,'#ffc255')+text(-150,-203,'FIKTIV · BEISPIEL',15,CREAM,800)
 for y in [-165,-120,-75]:b+=path(f'M-167 {y}H166',stroke='#bacac1',sw=1)
 if mode=='chart':
  b+=text(-160,-168,'101,28 €',24,'#386650')+path('M-163-63L-126-88L-91-74L-55-127L-13-107L22-157L60-139L103-177L161-189',stroke='#41846a',sw=7,extra='data-anim="graph"')
 else:
  b+=text(-160,-151,'UMSATZ · Q3',23,'#507e7c')+g(text(-160,-92,'47.280 €',44,INK)+rect(-160,-62,198,11,'#bfd0c2',4),'data-anim="answer"')
 b+=path('M-241 0H240L302 42H-301Z','#a6b4b2',INK,4)+path('M-186 7H185M-215 20H217',stroke='#6b7d81',sw=5)+path('M-45 26H48',stroke='#677c81',sw=9)
 return g(b,'data-prop="laptop" transform="translate(1120 761)"')

def room(p,night=False):
 b=rect(-700,-500,3400,2200,'#cdbda6' if not night else '#938578')+rect(-100,785,2300,650,'#ad9275')
 for x in range(-100,2200,180):b+=path(f'M{x} 785L{x-140} 1200',stroke='#92785e',sw=2)
 b+=path('M-100 914H2100M-100 1065H2100',stroke='#92785e',sw=2)
 b+=rect(105,180,500,500,'#f1e4cb',12)+rect(126,202,459,457,'#b6d4e2' if not night else '#344757',4)
 if night:
  b+=ellipse(471,297,38,38,'#f6e7b6')
  for i in range(17):b+=ellipse(147+(i*67)%410,223+(i*43)%350,2,2,'#fff4dc')
 else:
  for x in [160,300,480]:b+=rect(x,390,70,268,'#b3c6c8')
 b+=path('M355 205V660M128 431H585',stroke='#f1e4cb',sw=13)
 b+=path('M99 160H618',stroke='#776452',sw=14)+path('M105 177L55 690H143L187 177Z','#507e7c')+path('M537 177L580 690H650L610 177Z','#507e7c')
 b+=rect(1310,230,520,395,'#c5ad8d',12)+rect(1330,252,480,336,'#e6d7bf',6)
 b+=path('M1342 384H1790',stroke='#9d8264',sw=10)
 for i,c in enumerate(['#a96a53','#507e7c','#d0a550','#437daf']):b+=rect(1390+i*83,290,48,83,c,5)
 b+=path('M1560 0V94',stroke='#635548',sw=8)+path('M1470 166Q1485 80 1560 83Q1635 80 1650 166Z','#c69c56')+ellipse(1560,166,90,17,'#f9d694')
 return b

def kitchen(p,night=False):
 b=room(p,night)+rect(682,230,530,112,'#eadbc1',10)+rect(692,240,245,92,'#d8c3a2',8)+rect(947,240,254,92,'#d8c3a2',8)
 b+=path('M914 267V302M971 267V302',stroke='#85715a',sw=7)+rect(690,550,560,195,'#507e7c',8)+rect(676,530,590,29,'#f4e4c8',6)
 b+=path('M1055 525V464Q1077 430 1096 457V481',stroke='#879c9c',sw=9)+ellipse(1067,541,79,9,'#738c89')
 b+=wall_clock(959,430,'19:42' if night else '08:03')
 return b

def office(p):
 b=room(p)+rect(730,150,482,279,'#a58c70',12)+rect(749,171,444,239,'#e8dfcd',4)
 b+=text(790,225,'PROJEKTPLAN',28,'#507e7c')
 for i in range(4):b+=rect(788,251+i*32,190+i*25,12,['#b9c5b3','#e4be70'][i%2],3)
 b+=rect(1450,580,290,172,'#a88c6e',9)+path('M1590 585V744',stroke='#856c53',sw=3)
 b+=tree(1790,780,.55)
 return b

def station(p):
 b=rect(-600,-500,3400,2200,'#d6d8cd')+rect(-300,190,2600,440,'#bccac8')
 for x in range(-100,2200,300):b+=path(f'M{x} 0L{x+110} 510',stroke='#98a6a5',sw=26)
 b+=rect(-200,200,2500,40,'#697e7c')+rect(104,90,650,100,'#304c4e',10)+text(140,155,'S1 · ZENTRUM',44,CREAM)
 b+=rect(-200,768,2400,105,'#505c62')+rect(-200,858,2400,700,'#b5aea0')+path('M-200 864H2200',stroke='#efc25a',sw=13)
 for x in range(-200,2300,155):b+=path(f'M{x} 880L{x-90} 1200',stroke='#999486',sw=2)
 return b

def train():
 b=rect(-1100,285,3900,544,'#6a9393',35)+rect(-1100,326,3900,71,'#f0e6cf')+rect(-1100,707,3900,94,'#476c6d')
 for x in [-900,-460,-20,420,1430,1870,2310]:
  b+=rect(x,431,321,225,'#a9c8d4',24)+path(f'M{x+30} 452L{x+265} 452L{x+105} 636H{x+30}Z','#c2dbe0')
 b+=rect(1021,398,300,413,'#344e53',8)+rect(1040,429,262,372,'#899d99',4)
 door=rect(0,0,145,405,'#e5dfcc',5)+rect(18,33,109,230,'#8baab5',13)+path('M116 278V338',stroke='#70868a',sw=6)
 b+=g(door,'data-anim="door-left" transform="translate(1027 402)"')+g(door,'data-anim="door-right" transform="translate(1172 402)"')
 b+=path('M-1000 806H2700',stroke='#314c50',sw=9)
 return g(b,'data-anim="train"')

def living(p):
 b=room(p,True)+rect(311,215,1298,604,'#39484b',25)+rect(331,235,1258,564,'#101e22',10)
 b+=rect(340,245,1240,544,'#496d4f',6)+path('M352 698L502 302H1418L1568 698Z','#5e955e')
 b+=path('M354 698L502 302H1418L1568 698ZM960 302V698M1252 350H1401L1520 650H1214Z',stroke='#d7e7bb',sw=5)
 b+=ellipse(960,490,80,97,'none',extra='stroke="#d7e7bb" stroke-width="4"')
 b+=path('M1397 402H1480V558H1397ZM1397 402L1374 424V578L1397 558M1480 402L1459 424H1374M1459 424V578H1374',stroke='#f4ead1',sw=7)
 for x in range(1376,1482,17):b+=path(f'M{x} 424V558',stroke='#d7e7bb',sw=1)
 for y in range(430,557,20):b+=path(f'M1376 {y}H1479',stroke='#d7e7bb',sw=1)
 for x,y,c in [(1070,500,'#f5b24b'),(1225,448,'#437daf'),(1190,590,'#437daf'),(1370,497,'#ba6c61')]:
  b+=g(ellipse(0,-19,12,12,INK)+path('M-16 0H16L18 37H-18Z',c)+path('M-9 34L-17 62M9 34L18 62',stroke=INK,sw=9),f'transform="translate({x} {y})" data-anim="player"')
 b+=g(ellipse(0,7,13,5,'#395743')+ellipse(0,0,11,11,CREAM)+path('M-5-5L4-6L8 2L0 7L-7 2Z',INK),'data-anim="ball" transform="translate(1100 536)"')
 b+=rect(366,263,278,60,INK,8)+text(396,304,'HEIM',23,CREAM)+text(517,305,'0 : 0',32,CREAM,800,extra='data-anim="score"')
 b+=g(rect(710,410,520,133,INK,18)+text(970,496,'VAR · PRÜFUNG',48,CREAM,800,'middle'),'data-anim="var" style="opacity:0"')
 b+=rect(620,835,680,38,'#78634f',10)+path('M674 865L650 1080M1250 865L1270 1080',stroke='#685643',sw=22)
 b+=path('M-150 1060L210 896H1720L2100 1060Z','#5a696c')
 return b

def phone_large(mode='bet'):
 b=rect(-170,-290,340,580,INK,35)+rect(-152,-255,304,505,'#edf0e5',20)+rect(-55,-278,110,10,'#788c8d',5)
 b+=rect(-151,-255,302,87,'#507e7c',20)+text(0,-205,'LIVE' if mode=='bet' else 'LEO',35,CREAM,800,'middle')
 if mode=='message':
  b+=rect(-129,-107,252,131,'#d6dfce',18)+text(-108,-60,'Bin gleich da.',27,INK,700)+text(-108,-16,'19:43',20,'#507e7c',600)
 elif mode=='bet':
  b+=text(0,-107,'NÄCHSTES TOR',29,INK,800,'middle')+rect(-125,-60,250,140,'#d6dfce',15)+text(0,-11,'HEIM',32,INK,800,'middle')+text(0,45,'10,00 €',38,INK,800,'middle')+rect(-125,112,250,80,'#507e7c',12)+text(0,164,'ABGEGEBEN',29,CREAM,800,'middle')
 else:
  b+=ellipse(0,-65,60,60,'#437daf')+ellipse(0,-77,23,23,INK)+path('M-38-32Q0-70 38-32V-13H-38Z',INK)
  b+=text(0,53,'LEO',39,INK,800,'middle')+g(text(0,103,'VERBUNDEN',23,'#507e7c',800,'middle'),'data-anim="connected" style="opacity:0"')
  b+=ellipse(0,182,39,39,'#a85f52')+path('M-18 182Q0 164 18 182',stroke=CREAM,sw=8)
 return g(b,'data-anim="phone-large" transform="translate(960 580)"')

def food():
 b=ellipse(1060,783,167,52,'#d0b58e')+ellipse(1060,772,154,44,'#fff0d2')+ellipse(1060,771,120,29,'#e0c092')
 for i in range(11):b+=ellipse(974+(i*43)%167,757+(i*13)%28,17,8,'#738d59' if i%3 else '#b36c50')
 b+=path('M1260 733L1298 793M1254 720L1267 740M1264 714L1277 734M1274 709L1287 729',stroke='#c6cdcb',sw=7)
 return b

def envelope(x=1330,y=730):
 return g(rect(-113,-82,226,136,'#f6e9cf',7)+path('M-112-81L0-8L112-81M-112 53L-28-26M112 53L28-26',stroke='#c7b79d',sw=3),f'transform="translate({x} {y})"')

def van():
 # A delivery van on the carriageway. Wheels share the translation and rotation.
 b=ellipse(0,68,330,28,'#4d5058','opacity=".2"')+path('M-344-190Q-344-215-315-215H80V-188H160L259-71H309Q334-67 340-28V42H-344Z','#668b88',INK,5)
 b+=path('M97-173H151L232-78H97Z','#a4c3cf',INK,5)+rect(-302,-172,335,148,'#769d96',9)+path('M59-181V31M-322 6H330',stroke='#456c6c',sw=5)+rect(287,-51,40,34,'#f5df9c',4)
 b+=ellipse(145,-132,15,15,INK)+path('M132-117L136-88H166L161-111Z',INK)
 for x in [-220,220]:
  b+=g(ellipse(0,0,57,57,INK)+ellipse(0,0,39,39,'#8faaa9')+path('M-30 0H30M0-30V30M-22-22L22 22M-22 22L22-22',stroke='#4d656a',sw=7)+ellipse(0,0,10,10,'#c2c9c2'),f'data-wheel-x="{x}" data-anim="wheel" transform="translate({x} 29)"')
 return g(b,'data-anim="van" transform="translate(-900 805)"')
