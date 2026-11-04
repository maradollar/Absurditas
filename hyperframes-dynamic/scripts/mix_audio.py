"""Original Mark performance + licensed music + synchronized original and bundled foley."""
from pathlib import Path
import subprocess,json,hashlib,wave,sys
import numpy as np
R=Path(__file__).resolve().parents[1];A=R/'assets/audio';SR=48000;D=344.;N=round(D*SR)
SOURCE=Path(sys.argv[1]);B=Path(sys.argv[2]);FOLEY=R.parent/'cartoon-v2/public/cartoon-v2/foley.wav'
scenes=json.loads((R/'production/scenes.json').read_text());S={s['action']:s for s in scenes}
def decode(p,ss=None,dur=None):
 cmd=['ffmpeg','-v','error']
 if ss is not None:cmd+=['-ss',str(ss)]
 cmd+=['-i',str(p)]
 if dur is not None:cmd+=['-t',str(dur)]
 return np.frombuffer(subprocess.check_output(cmd+['-ar',str(SR),'-ac','2','-f','f32le','-']),dtype='<f4').reshape(-1,2).copy()
def wav(name,x):
 with wave.open(str(A/name),'wb') as f:
  f.setparams((1 if x.ndim==1 else 2,2,SR,0,'NONE','not compressed'));f.writeframes((np.clip(x,-.999,.999)*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(SOURCE),'-ac','1','-ar',str(SR),'-af','loudnorm=I=-17:TP=-3:LRA=9,aresample=48000,asetpts=PTS-STARTPTS,apad=whole_len=16512000,atrim=end_sample=16512000',str(A/'voice.wav')],check=True)
with wave.open(str(A/'voice.wav')) as f:voice=np.frombuffer(f.readframes(N),dtype='<i2').astype(np.float32)/32768
assert len(voice)==N
bed=np.zeros((N,2),np.float32);fx=np.zeros_like(bed);events=[]
def place(dst,clip,at,gain=1,fade=.015,pan=0):
 clip=clip.copy();n=len(clip);r=min(n//2,round(fade*SR))
 if r:clip[:r]*=np.linspace(0,1,r)[:,None];clip[-r:]*=np.linspace(1,0,r)[:,None]
 if isinstance(pan,tuple):p=np.linspace(*pan,n)
 else:p=np.ones(n)*pan
 clip[:,0]*=np.sqrt((1-p)/2)*1.414;clip[:,1]*=np.sqrt((1+p)/2)*1.414
 st=round(at*SR);en=min(N,st+n)
 if st>=0 and en>st:dst[st:en]+=clip[:en-st]*gain
def music(name,start,end,offset,gain):
 clip=decode(A/name,offset,end-start);rms=float(np.sqrt(np.mean(clip**2)));clip*=.16/max(.001,rms);place(bed,clip,start,gain,2.0)
music('the-descent.mp3',0,64,23.3,.15)
music('carefree.mp3',61.5,175,15,.15)
music('the-descent.mp3',172.5,213,69,.12)
music('dream-culture.mp3',210,344,19.785714,.17)
def effect(file,at,gain=.10,duration=.6):
 clip=decode(B/file,dur=duration);place(fx,clip,at,gain,.018);events.append({'time':round(at,3),'duration':len(clip)/SR,'source':'HyperFrames bundled Pixabay','name':file})
def original(kind,at,duration=.18,gain=.045,pan=0):
 # Foley synthesis uses a fixed seed. These are original designed sounds, not field recordings.
 n=round(duration*SR);t=np.arange(n)/SR;rng=np.random.default_rng(9701+round(at*100));noise=rng.standard_normal(n)
 if kind=='footstep':x=(np.sin(2*np.pi*(105*t-35*t*t))*np.exp(-t*26)+np.convolve(noise,np.ones(9)/9,'same')*.28*np.exp(-t*52))
 elif kind=='cup':x=(np.sin(2*np.pi*1320*t)+.5*np.sin(2*np.pi*2153*t))*np.exp(-t*17)
 elif kind=='cloth':x=np.convolve(noise,np.ones(25)/25,'same')*np.sin(np.pi*t/duration)**2
 elif kind=='pour':x=np.convolve(noise,np.ones(7)/7,'same')*(.6+.4*np.sin(2*np.pi*17*t))*np.sin(np.pi*t/duration)**2
 elif kind=='door':x=np.convolve(noise,np.ones(31)/31,'same')*np.sin(np.pi*t/duration)**2+.18*np.sin(2*np.pi*72*t)*np.exp(-t*9)
 elif kind=='train':x=np.convolve(noise,np.ones(61)/61,'same')*.8+.13*np.sin(2*np.pi*(68*t+4*t*t))
 elif kind=='beep':x=np.sin(2*np.pi*960*t)*np.sin(np.pi*t/duration)**2
 elif kind=='kick':x=np.sin(2*np.pi*(140*t-110*t*t))*np.exp(-t*35)+noise*.2*np.exp(-t*70)
 elif kind=='crowd':x=np.convolve(noise,np.ones(14)/14,'same')*(.65+.35*np.sin(2*np.pi*3.8*t))
 else:x=np.sin(2*np.pi*420*t)*np.exp(-t*18)
 x=x.astype(np.float32);x*=gain/max(.001,float(np.abs(x).max()));place(fx,np.column_stack([x,x]),at,1,.015,pan)
 events.append({'time':round(at,3),'duration':duration,'source':'Original deterministic sound design','name':kind})
loc=decode(FOLEY)
def location(st,dur,at,gain,pan):
 clip=loc[round(st*SR):round((st+dur)*SR)];place(fx,clip,at,gain,.025,pan);events.append({'time':round(at,3),'duration':dur,'source':'Existing original Absurditas foley without voice','name':'vehicle / tyre'})
location(7.04,1.05,S['brake']['start']+.08,1.6,(.6,.1))
location(14.1,4.6,S['pass']['start'],1.7,(-.9,.9))
for s in scenes:
 if s['future'] and (s['start']==0 or not next((x['future'] for x in scenes if abs(x['end']-.22-s['start'])<.04),False)):
  effect('whoosh-short.mp3',s['start']+.02,.08,.55)
 # Only selected transitions carry a whoosh; avoid an effect on every edit.
 if s['action'] in ['return','move','run','chart','var','crossing','arrival','dinner','decide']:effect('whoosh-short.mp3',s['start']+.03,.065,.45)
 if s['action'] in ['buy','fees','net','answer']:effect('click-soft.mp3',s['start']+.35,.14,.35)
original('cloth',S['move']['start']+.36,.65,.035);original('cup',S['move']['start']+1.55,.42,.035)
original('pour',S['spill']['start']+S['spill']['duration']*.43,1.3,.047)
original('cloth',S['brush']['start']+.5,.45,.03)
run=S['run'];steps=max(4,round(540/(.9*70)))
for j in range(steps):original('footstep',run['start']+.06+j*(run['duration']-.25)/steps,.16,.045,(-.5+j/steps*.9))
original('train',S['missed']['start']+.5,max(.3,S['missed']['duration']-.7),.04)
for at in [S['board']['start']+.2,S['board']['start']+.5,S['depart']['start']+.05]:original('beep',at,.13,.035)
original('door',S['board']['start']+.05,.65,.04)
original('train',S['depart']['start']+.2,S['depart']['duration']-.3,.05,(-.3,-.8))
effect('key-press.mp3',S['answer']['start']+.5,.11,.5)
effect('notification.mp3',S['profit']['start']+.4,.095,.8)
for a in ['goalvision','goal']:
 s=S[a];original('kick',s['start']+.35,.2,.05);original('crowd',s['start']+1.1,max(.3,s['duration']-1.25),.04)
effect('error.mp3',S['offside']['start']+.15,.045,.5)
effect('notification.mp3',S['message']['start']+.3,.06,.65)
effect('click-soft.mp3',S['call']['start']+.45,.1,.35)
effect('click-soft.mp3',S['subscribe']['start']+.3,.12,.35)
for aa,bb in [(S['question']['start'],S['shock']['end']),(S['apology']['start'],S['listen']['end'])]:
 st=round(aa*SR);en=round(bb*SR);bed[st:en]*=.42
env=np.convolve(np.abs(voice[::48]),np.ones(160)/160,'same');env=np.interp(np.arange(N),np.arange(len(env))*48,env).astype(np.float32)
bed*=(1-.5*np.clip(env/.065,0,1))[:,None];fx*=(1-.24*np.clip(env/.075,0,1))[:,None]
score=bed+fx;mix=score+voice[:,None];safe=min(1,.86/max(.001,float(np.abs(mix).max())))
voice*=safe;score*=safe;mix*=safe;wav('mix.wav',mix)
loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(A/'mix.wav'),'-af','loudnorm=I=-14.5:TP=-1.8:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
m=json.loads(loud.stderr[loud.stderr.rfind('{'):loud.stderr.rfind('}')+1]);db=min(-14.5-float(m['input_i']),-1.8-float(m['input_tp']));master=10**(db/20)
voice*=master;score*=master;mix*=master
wav('voice.wav',voice);wav('score-fx.wav',score);wav('mix.wav',mix)
report={'duration':D,'source_duration':343.379563,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'speed':1,'pitch_changed':False,'source_kept_complete':True,'sample_rate':SR,'music':['The Descent','Carefree','Dream Culture'],'speech_ducking':True,'master_gain_db':db,'events':events,'critical_listening':False}
(R/'production/audio-cues.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Mixed complete voice, 4 music sections and',len(events),'synchronized effects;',D,'seconds')
