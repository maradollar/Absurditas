"""Check the actual encoded film and extract reproducible visual-review boards."""
from pathlib import Path
import argparse,subprocess,json,wave,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--duration',type=float,default=303);p.add_argument('--output',default='review/encoded-film');args=p.parse_args()
R=Path(__file__).resolve().parents[1];V=Path(args.video).resolve();O=(R/args.output).resolve();O.mkdir(parents=True,exist_ok=True)
D=args.duration;F=round(D*30)
def read(*args):return subprocess.check_output(list(map(str,args)))
probe=json.loads(read('ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',V));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],int(v['nb_read_frames']),v['pix_fmt'])==(1920,1080,'h264','30/1',F,'yuv420p')
for t in [v['duration'],a['duration'],probe['format']['duration']]:assert abs(float(t)-D)<.04,(t,D)
assert a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000'
subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],check=True)
raw=read('ffmpeg','-v','error','-i',V,'-vf','scale=160:90','-pix_fmt','rgb24','-f','rawvideo','-')
frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,90,160,3);assert len(frames)==F
means=frames.mean(axis=(1,2,3));assert means.min()>10
diff=np.abs(np.diff(frames.astype(np.int16),axis=0)).mean(axis=(1,2,3));del raw
raw=read('ffmpeg','-v','error','-i',V,'-vn','-ar','48000','-ac','2','-f','f32le','-');sound=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
peak=float(np.abs(sound).max());assert 0.05<peak<1
with wave.open(str(R/'assets/audio/voice.wav')) as w:voice=np.frombuffer(w.readframes(round(min(D,303)*48000)),dtype='<i2').astype(np.float32)/32768
n=min(len(voice),len(sound));corr=float(np.corrcoef(voice[:n],sound[:n].mean(axis=1))[0,1]);assert corr>.95,corr
# The zero-lag voice/mix correlation, source hash, unchanged synthesis speed and
# continuous duration jointly check that the supplied performance was retained.
loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-14.5:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
loudness=json.loads(loud.stderr[loud.stderr.rfind('{'):loud.stderr.rfind('}')+1]);assert float(loudness['input_tp'])<=-.8
scenes=json.loads((R/'production/scenes.json').read_text())
times=[0,D-1/30]+list(np.arange(0,D,3))
for s in scenes:
 if s['start']<D:
  times += [s['start'],min(D-1/30,s['start']+.35),min(D-1/30,(s['start']+s['end'])/2),min(D-1/30,s['end']-.04)]
times+=list(np.arange(18.3,min(25.5,D),.2))
for aa,bb,step in [(95.4,98.2,.14),(102.8,104.8,.14),(189.3,190.8,.15),(227.5,235.5,.35),(240.2,242.2,.2),(262.4,267.5,.3),(299.8,303,.2)]:
 if aa<D:times+=list(np.arange(aa,min(bb,D),step))
indices=sorted(set(max(0,min(F-1,round(t*30))) for t in times if t<D))
def balanced_select(nums):
 if len(nums)==1:return f'eq(n,{nums[0]})'
 m=len(nums)//2;return f'({balanced_select(nums[:m])}+{balanced_select(nums[m:])})'
select=balanced_select(indices)
subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-i',str(V),'-vf',f"select='{select}'",'-fps_mode','vfr','-threads','1',str(O/'frame-%04d.png')],check=True)
lookup={n:O/f'frame-{i+1:04d}.png' for i,n in enumerate(indices)}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
def nearest(t):return min(indices,key=lambda n:abs(n-t*30))
def board(nums,name,cols=4,width=450):
 nums=list(dict.fromkeys(nums));h=round(width*1080/1920);rows=(len(nums)+cols-1)//cols
 b=Image.new('RGB',(cols*(width+12)+12,rows*(h+39)+12),'#17151d');draw=ImageDraw.Draw(b)
 for j,i in enumerate(nums):
  x=12+j%cols*(width+12);y=12+j//cols*(h+39)
  with Image.open(lookup[i]) as im:b.paste(im.resize((width,h)),(x,y))
  draw.text((x,y+h+6),f'{i/30:06.2f} s | {i:04d}',font=font,fill='#fff4dc')
 b.save(O/name,quality=95)
board([nearest(min(D-.04,(s['start']+s['end'])/2)) for s in scenes if s['start']<D]+[F-1],'Filmuebersicht.jpg')
board([nearest(t) for t in [0,1,2,4,7,10,13,16,19,20,21,22,23,24,25,27,31,36,39] if t<D],'Hook.jpg')
for aa,bb,name in [(18.3,25.5,'Schritt_und_Vorbeifahrt.jpg'),(95.4,104.8,'Tasse_und_Tablett.jpg'),(227.5,235.5,'Zukunft_Abschied.jpg'),(240.2,247.8,'Handy_und_Entschuldigung.jpg')]:
 if aa<D:board([i for i in indices if aa<=i/30<=min(bb,D)],name)
rms=[float(np.sqrt(np.mean(sound[i*48000:min((i+1)*48000,len(sound))]**2))) for i in range(int(D))]
warnings={}
check=R/'production/hyperframes-check.json'
if check.exists():
 c=json.loads(check.read_text());warnings={k:{'ok':z.get('ok'),'errors':z.get('errorCount',0),'warnings':z.get('warningCount',0)} for k,z in c.items() if isinstance(z,dict) and 'ok' in z}
report={'file':V.name,'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size,'video':{k:v[k] for k in ['codec_name','width','height','r_frame_rate','duration','nb_read_frames','pix_fmt']},'audio':{k:a[k] for k in ['codec_name','sample_rate','channels','duration']},'full_decode':'passed','black_frames':int((means<10).sum()),'minimum_frame_mean_rgb':float(means.min()),'adjacent_mean_change_max':float(diff.max()),'audio_peak':peak,'voice_to_decoded_mix_correlation_at_zero_lag':corr,'loudness':{k:loudness[k] for k in ['input_i','input_tp','input_lra']},'audio_rms_per_second':rms,'review_frames':len(indices),'hyperframes_check':warnings,'limits':'Actual encoded frames and audio levels were checked. No complete real-time critical listening is claimed.'}
(O/'frame-index.json').write_text(json.dumps(indices)+'\n');(O/'technical.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:z for k,z in report.items() if k not in ['audio_rms_per_second','hyperframes_check']},ensure_ascii=False,indent=2))
