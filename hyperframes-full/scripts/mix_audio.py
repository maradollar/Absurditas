"""Place licensed music, supplied Mark performance and existing original foley.

No user recording is uploaded. The original performance keeps its full timebase.
"""
from pathlib import Path
import json,subprocess,wave,sys,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];A=R/'assets/audio';SR=48000;DURATION=303;N=SR*DURATION
if len(sys.argv)<2:raise SystemExit('Usage: python scripts/mix_audio.py /path/to/Mark.mp3 [existing-foley.wav] [hyperframes-sfx-directory]')
SOURCE=Path(sys.argv[1]);FOLEY=Path(sys.argv[2]) if len(sys.argv)>2 else R.parent/'cartoon-v2/public/cartoon-v2/foley.wav'
BUNDLE=Path(sys.argv[3]) if len(sys.argv)>3 else Path('/tmp/absurditas-hyperframes-npm/_npx/8a100992a21bdc5c/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx')
def ff(*args):return subprocess.check_output(['ffmpeg','-v','error',*map(str,args)])
def decode(p,start=0,duration=None,mono=False):
 args=['-ss',str(start),'-i',str(p)]
 if duration is not None:args+=['-t',str(duration)]
 a=np.frombuffer(ff(*args,'-ar',SR,'-ac',1 if mono else 2,'-f','f32le','-'),dtype='<f4').copy()
 return a if mono else a.reshape(-1,2)
def write(name,a):
 with wave.open(str(A/name),'wb') as w:
  w.setnchannels(1 if a.ndim==1 else 2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
# Canonical narration was already normalized for preview. Reproduce it directly
# from the uploaded file if this is a fresh project.
subprocess.run(['ffmpeg','-v','error','-y','-i',str(SOURCE),'-af','loudnorm=I=-17:TP=-2:LRA=9,aresample=48000,asetpts=PTS-STARTPTS,apad=whole_len=14544000,atrim=end_sample=14544000','-ac','1','-c:a','pcm_s16le',str(A/'voice.wav')],check=True)
voice=decode(A/'voice.wav',mono=True);assert len(voice)==N
bed=np.zeros((N,2),dtype=np.float32);fx=np.zeros_like(bed);events=[]
def place(dest,clip,at,gain=1,fade=.05,pan=None):
 start=round(at*SR);n=min(len(clip),N-start);a=clip[:n].astype(np.float32,copy=True)*gain
 if a.ndim==1:a=np.repeat(a[:,None],2,axis=1)
 ramp=min(round(fade*SR),n//2)
 if ramp:a[:ramp]*=np.linspace(0,1,ramp,dtype=np.float32)[:,None];a[-ramp:]*=np.linspace(1,0,ramp,dtype=np.float32)[:,None]
 if pan is not None:
  mono=a.mean(axis=1);pp=np.linspace(pan[0],pan[1],n,dtype=np.float32);a[:,0]=mono*np.sqrt((1-pp)/2);a[:,1]=mono*np.sqrt((1+pp)/2)
 dest[start:start+n]+=a
def music(name,at,end,offset,gain):
 a=decode(A/name,offset,end-at);n=len(a);fade_in=min(round(2.0*SR),n//4);fade_out=min(round(2.8*SR),n//4)
 a[:fade_in]*=np.linspace(0,1,fade_in,dtype=np.float32)[:,None];a[-fade_out:]*=np.linspace(1,0,fade_out,dtype=np.float32)[:,None]
 place(bed,a,at,gain,.03);events.append({'time':at,'end':end,'type':'music','file':name,'source_offset':offset,'gain':gain})
music('the-descent.mp3',0,90.24,23.30,.105)
music('carefree.mp3',87.84,171.0,15.0,.105)
music('dream-culture.mp3',168.5,303.0,19.785714,.13)
# A quiet musical gap gives the friend's question and the apology their space.
for start,end,low in [(215.5,222.3,.38),(240.0,247.6,.42)]:
 a=round(start*SR);b=round(end*SR);env=np.ones(b-a,dtype=np.float32)*low;ramp=min(SR,b-a)
 env[:ramp]=np.linspace(1,low,ramp);env[-ramp:]=np.linspace(low,1,ramp);bed[a:b]*=env[:,None]
location=decode(FOLEY)
def existing(old_start,dur,at,gain,name,pan=None):
 clip=location[round(old_start*SR):round((old_start+dur)*SR)]
 place(fx,clip,at,gain,.035,pan);events.append({'time':at,'duration':dur,'type':'original-location-foley','name':name})
existing(7.04,1.05,9.46,2.1,'Reifen in der Vision',(.2,.35))
existing(14.1,5.1,20.85,2.3,'Annäherung und Vorbeifahrt links nach rechts',(-.9,.9))
existing(16.2,.17,21.87,1.8,'Fuß bleibt auf dem Gehweg')
existing(10.02,.30,95.83,1.5,'Ärmel beim Versetzen der Tasse')
existing(22.35,.28,241.75,1.8,'Telefon ablegen / Kleidung')
# Actual CC0 rain recording, rather than the inappropriate melodic result
# returned by the generic effect search.
rain=decode(A/'light-rain.wav',15,20)
rain*=.027/max(.0001,float(np.sqrt(np.mean(rain**2))))
place(fx,rain[:round(6.7*SR)],113.55,.65,.6)
place(fx,rain[round(7*SR):round(15*SR)],122.20,.65,.8)
events.extend([{'time':113.55,'duration':6.7,'type':'CC0 field recording','name':'Regen in der Vision'},{'time':122.2,'duration':8,'type':'CC0 field recording','name':'Tatsächlicher Regen außerhalb der Markise'}])
def bundled(file,at,gain,limit=None):
 a=decode(BUNDLE/file,duration=limit);place(fx,a,at,gain,.025);events.append({'time':at,'duration':len(a)/SR,'type':'HyperFrames bundled Pixabay SFX','file':file})
for at,filename in [(1.80,'whoosh-short.mp3'),(11.72,'whoosh.mp3'),(92.43,'whoosh-short.mp3'),(175.65,'whoosh-short.mp3'),(186.4,'whoosh.mp3'),(225.20,'whoosh-short.mp3'),(238.4,'whoosh.mp3')]:bundled(filename,at,.12,.70)
bundled('notification.mp3',177.65,.115,.8);bundled('notification.mp3',187.3,.10,.8)
bundled('click-soft.mp3',190.12,.12,.4);bundled('click-soft.mp3',300.35,.10,.4)
# Speech-following gain is smoothed at 1 kHz, then interpolated to full rate.
env=np.convolve(np.abs(voice[::48]),np.ones(150,dtype=np.float32)/150,mode='same')
env=np.interp(np.arange(N),np.arange(len(env))*48,env).astype(np.float32)
duck=1-.50*np.clip(env/.065,0,1);bed*=duck[:,None];fx*= (1-.24*np.clip(env/.075,0,1))[:,None]
score=bed+fx;mix=score+voice[:,None]
peak=float(np.abs(mix).max());gain=min(1,.88/max(.001,peak))
voice*=gain;score*=gain;mix*=gain
write('voice.wav',voice);write('score-fx.wav',score);write('mix.wav',mix)
measure=subprocess.run(['ffmpeg','-hide_banner','-i',str(A/'mix.wav'),'-af','loudnorm=I=-14.5:TP=-1.8:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
m=json.loads(measure.stderr[measure.stderr.rfind('{'):measure.stderr.rfind('}')+1]);master_db=min(-14.5-float(m['input_i']),-1.8-float(m['input_tp']))
master=10**(master_db/20);voice*=master;score*=master;mix*=master
write('voice.wav',voice);write('score-fx.wav',score);write('mix.wav',mix)
report={'duration':DURATION,'sample_rate':SR,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_duration':302.132188,'speed':1,'pitch_changed':False,'source_kept_complete':True,'music_tracks':['The Descent','Carefree','Dream Culture'],'speech_ducking':True,'raw_mix_peak':peak,'safety_gain':gain,'master_gain_db':master_db,'measured_before_master':{'lufs':m['input_i'],'true_peak_db':m['input_tp']},'mix_peak':float(np.abs(mix).max()),'events':events,'listening':'Measured and inspected as waveform; no critical human listening claimed.'}
(R/'production/audio-cues.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='events'},ensure_ascii=False,indent=2))
