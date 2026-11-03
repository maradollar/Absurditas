"""Run encoded-film checks and add dense word-reveal/safe-area review boards."""
from pathlib import Path
import subprocess,sys,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
VIDEO=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'out/WhatIf_Eine_Minute_Zukunft_Hook_v3_30s.mp4'
OUT=ROOT/'out/qc-v3';OUT.mkdir(exist_ok=True)
subprocess.run([sys.executable,str(ROOT/'scripts/qc.py'),str(VIDEO),str(OUT)],check=True)
indices=[32,58,110,176,244,304,414,448,503,606,712,747,806,892]
select='+'.join(f'eq(n,{n})' for n in indices)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(VIDEO),'-vf',f"select='{select}'",'-fps_mode','vfr',str(OUT/'type-%02d.png')],check=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
width=560;h=315;cols=3;rows=(len(indices)+cols-1)//cols
board=Image.new('RGB',(cols*(width+14)+14,rows*(h+38)+14),'#17151d');draw=ImageDraw.Draw(board)
for i,n in enumerate(indices):
    x=14+i%cols*(width+14);y=14+i//cols*(h+38)
    with Image.open(OUT/f'type-{i+1:02d}.png') as im:board.paste(im.resize((width,h)),(x,y))
    draw.text((x,y+h+6),f'{n/30:.2f} s  |  Frame {n}',font=font,fill='#fff4dc')
board.save(OUT/'Text_und_Grafik.jpg',quality=95)
review=[14,17,20,23,26,29,32,35,44,47,50,53,56,59,62,65,68,71,74,77,80,83,86,89,92,95,98,101,104,107]
select='+'.join(f'eq(n,{n})' for n in review)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(VIDEO),'-vf',f"select='{select}'",'-fps_mode','vfr',str(OUT/'hook-%02d.png')],check=True)
board=Image.new('RGB',(5*396+12,6*255+12),'#17151d');draw=ImageDraw.Draw(board)
for i,n in enumerate(review):
    x=12+i%5*396;y=12+i//5*255
    with Image.open(OUT/f'hook-{i+1:02d}.png') as im:board.paste(im.resize((384,216)),(x,y))
    draw.text((x,y+222),f'{n/30:.2f} s | {n}',font=font,fill='#fff4dc')
board.save(OUT/'Hook_Textbewegung.jpg',quality=95)
print('V3 typography and hook-motion review boards ready')
