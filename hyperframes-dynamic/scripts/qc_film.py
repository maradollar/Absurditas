"""Inspect the delivered MP4 itself: decode, timing, audio and scene/keyframe boards."""
from pathlib import Path
import argparse,subprocess,json,wave,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--duration',type=float,default=344);p.add_argument('--output',default='review/encoded-film');args=p.parse_args()
V=Path(args.video).resolve();O=R/args.output;O.mkdir(parents=True,exist_ok=True);D=args.duration;F=round(D*30)
def read(*a):return subprocess.check_output(list(map(str,a)))
pr=json.loads(read('ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',V));v=next(x for x in pr['streams'] if x['codec_type']=='video');a=next(x for x in pr['streams'] if x['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']),v['pix_fmt'])==('h264',1920,1080,'30/1',F,'yuv420p')
assert (a['codec_name'],a['channels'],a['sample_rate'])==('aac',2,'48000')
assert all(abs(float(t)-D)<.04 for t in [v['duration'],a['duration'],pr['format']['duration']])
subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],check=True)
raw=read('ffmpeg','-v','error','-i',V,'-vf','scale=160:90','-pix_fmt','rgb24','-f','rawvideo','-');frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,90,160,3);assert len(frames)==F
means=frames.mean(axis=(1,2,3));assert means.min()>10
dif=np.abs(np.diff(frames.astype(np.int16),axis=0)).mean(axis=(1,2,3))
rawsound=read('ffmpeg','-v','error','-i',V,'-vn','-ar','48000','-ac','2','-f','f32le','-');sound=np.frombuffer(rawsound,dtype='<f4').reshape(-1,2)
peak=float(np.abs(sound).max());assert .05<peak<1
with wave.open(str(R/'assets/audio/voice.wav')) as f:voice=np.frombuffer(f.readframes(round(D*48000)),dtype='<i2').astype(np.float32)/32768
n=min(len(voice),len(sound));corr=float(np.corrcoef(voice[:n],sound[:n].mean(axis=1))[0,1]);assert corr>.95
lm=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-14.5:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
loud=json.loads(lm.stderr[lm.stderr.rfind('{'):lm.stderr.rfind('}')+1]);assert float(loud['input_tp'])<=-.8
scenes=json.loads((R/'production/scenes.json').read_text());times=[0,D-1/30]+list(np.arange(0,D,3))
for s in scenes:times.extend([s['start'],s['start']+.35,(s['start']+s['end']-.22)/2,s['end']-.25])
for lo,hi in [(64.8,76.7),(88.9,91.6),(155.8,163.3),(196.8,200.2),(304,309)]:times+=list(np.arange(lo,min(hi,D),.2))
indices=sorted(set(max(0,min(F-1,round(t*30))) for t in times if t<D))
def selector(ns):
 if len(ns)==1:return f'eq(n,{ns[0]})'
 m=len(ns)//2;return f'({selector(ns[:m])}+{selector(ns[m:])})'
subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-i',str(V),'-vf',f"select='{selector(indices)}'",'-fps_mode','vfr','-threads','1',str(O/'frame-%04d.png')],check=True)
lookup={n:O/f'frame-{i+1:04d}.png' for i,n in enumerate(indices)};font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
def near(t):return min(indices,key=lambda i:abs(i/30-t))
def board(nums,name):
 nums=list(dict.fromkeys(nums));im=Image.new('RGB',(1860,((len(nums)+3)//4)*292+12),'#17151d');dr=ImageDraw.Draw(im)
 for j,k in enumerate(nums):
  x=12+j%4*462;y=12+j//4*292
  with Image.open(lookup[k]) as z:im.paste(z.resize((450,253)),(x,y))
  dr.text((x,y+259),f'{k/30:07.3f} s · {k:05d}',fill='#fff4dc',font=font)
 im.save(O/name,quality=95)
mids=[near((s['start']+s['end']-.22)/2) for s in scenes]
for i in range(0,len(mids),24):board(mids[i:i+24],f'Storyboard_{i//24+1}.jpg')
board([near(t) for t in [0,1.5,4.7,7.7,10.1,12.1,14.6,17.9,20.9,23.2,26.1,30.5]],'Hook.jpg')
for lo,hi,name in [(64.8,76.7,'Tasse.jpg'),(88.9,91.6,'Bahn.jpg'),(155.8,163.3,'Fussball.jpg'),(196.8,200.2,'Handy.jpg'),(304,309,'Anruf.jpg')]:board([i for i in indices if lo<=i/30<=hi],name)
motion=[]
for s in scenes:
 st=round((s['start']+.35)*30);en=round((s['end']-.3)*30)
 if en>st:motion.append({'id':s['id'],'start':s['start'],'end':s['end'],'mean_adjacent_pixel_change':float(dif[st:en].mean()),'changed_frames_fraction':float((dif[st:en]>.002).mean())})
report={'file':V.name,'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size,'video':{k:v[k] for k in ['codec_name','width','height','r_frame_rate','duration','nb_read_frames','pix_fmt']},'audio':{k:a[k] for k in ['codec_name','sample_rate','channels','duration']},'full_decode':'passed','black_frames':int((means<10).sum()),'minimum_frame_mean_rgb':float(means.min()),'audio_peak':peak,'voice_to_decoded_mix_correlation_at_zero_lag':corr,'loudness':{k:loud[k] for k in ['input_i','input_tp','input_lra']},'review_frames':len(indices),'critical_listening':False}
(O/'technical.json').write_text(json.dumps(report,indent=2)+'\n');(O/'frame-index.json').write_text(json.dumps(indices)+'\n');(R/'production/encoded-motion.json').write_text(json.dumps(motion,indent=2)+'\n')
print(json.dumps(report,indent=2))
