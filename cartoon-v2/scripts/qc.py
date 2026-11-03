"""QC of the encoded 30-second YouTube deliverable, plus reproducible review boards."""
from pathlib import Path
import subprocess,json,sys,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
VIDEO=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'out/WhatIf_Eine_Minute_Zukunft_Hook_v2_30s.mp4'
OUT=VIDEO.parent/'qc';OUT.mkdir(exist_ok=True)
def cmd(*args):return subprocess.check_output(list(args))
probe=json.loads(cmd('ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(VIDEO)))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],int(v['nb_read_frames']),v['pix_fmt'])==(1920,1080,'h264','30/1',900,'yuv420p')
for duration in [probe['format']['duration'],v['duration'],a['duration']]:assert abs(float(duration)-30)<.001
assert a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000'
subprocess.run(['ffmpeg','-v','error','-i',str(VIDEO),'-f','null','-'],check=True)
raw=cmd('ffmpeg','-v','error','-i',str(VIDEO),'-vf','scale=160:90','-pix_fmt','rgb24','-f','rawvideo','-')
frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,90,160,3)
means=frames.mean(axis=(1,2,3));diff=np.abs(np.diff(frames.astype(float),axis=0)).mean(axis=(1,2,3))
assert len(frames)==900 and means.min()>10
sound=cmd('ffmpeg','-v','error','-i',str(VIDEO),'-vn','-f','f32le','-ac','2','-ar','48000','-')
sound=np.frombuffer(sound,dtype='<f4').reshape(-1,2);peak=float(np.abs(sound).max());assert .02<peak<1
with wave.open(str(ROOT/'public/cartoon-v2/voice.wav')) as w:
 voice=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
n=min(len(voice),len(sound));corr=float(np.corrcoef(voice[:n],sound[:n].mean(axis=1))[0,1]);assert corr>.97
rms=[float(np.sqrt(np.mean(sound[i*48000:(i+1)*48000]**2))) for i in range(30)]
indices=sorted(set(list(range(0,900,30))+[899,44,45,90,129,130,165,198,199,224,259,260,320,388,389,436,453,454,464,475,486,505,515,530,540,548,577,600,653,654,700,720,850]+list(range(435,496,3))+list(range(435,589,7))))
select='+'.join(f'eq(n,{n})' for n in indices)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(VIDEO),'-vf',f"select='{select}'",'-fps_mode','vfr',str(OUT/'frame-%03d.png')],check=True)
lookup={n:OUT/f'frame-{i+1:03}.png' for i,n in enumerate(indices)}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
def board(nums,name,cols=5,width=384):
 h=round(width*1080/1920);rows=(len(nums)+cols-1)//cols
 im=Image.new('RGB',(cols*(width+12)+12,rows*(h+39)+12),'#072d39');d=ImageDraw.Draw(im)
 for i,n in enumerate(nums):
  x=12+i%cols*(width+12);y=12+i//cols*(h+39)
  with Image.open(lookup[n]) as fr:im.paste(fr.resize((width,h)),(x,y))
  d.text((x,y+h+6),f'{n/30:05.2f} s  |  {n:03}',font=font,fill='#ffedce')
 im.save(OUT/name,quality=95)
board(list(range(0,900,30))+[899],'Kontaktbogen_30s.jpg')
board([44,45,90,129,130,165,198,199,224,259,260,320,388,389,436,453,454,530,577,653,654,720,850,899],'Bildanschluesse.jpg',4,440)
board(list(range(435,496,3)),'Schrittfolge.jpg',4,440)
board(list(range(435,589,7)),'Autobewegung.jpg',4,440)
p=subprocess.run(['ffmpeg','-hide_banner','-i',str(VIDEO),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
loudness=json.loads(p.stderr[p.stderr.rfind('{'):p.stderr.rfind('}')+1])
report={'file':VIDEO.name,'video':{k:v[k] for k in ['codec_name','width','height','r_frame_rate','duration','nb_read_frames','pix_fmt']},'audio':{k:a[k] for k in ['codec_name','channels','sample_rate','duration']},'container_duration':probe['format']['duration'],'full_decode':'passed','black_frames':int((means<10).sum()),'minimum_mean_rgb':float(means.min()),'adjacent_frame_change_max':float(diff.max()),'near_identical_low_resolution_pairs':int((diff<.01).sum()),'audio_peak':peak,'voice_to_decoded_mix_correlation':corr,'audio_rms_per_second':rms,'loudness_measured':{k:loudness[k] for k in ['input_i','input_tp','input_lra']},'images_extracted':len(indices),'note':'Visual frame inspection and word alignment do not constitute critical listening or full real-time playback.'}
(OUT/'frame-index.json').write_text(json.dumps(indices)+'\n')
(OUT/'technical.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
