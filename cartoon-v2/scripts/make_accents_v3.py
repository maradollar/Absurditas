"""Deterministic original graphic accents. All audio stays local until MP4 export."""
from pathlib import Path
import json, wave
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'public/cartoon-v2'
SR=48000; N=SR*30; rng=np.random.default_rng(60311)
def read(name):
    with wave.open(str(DEST/name),'rb') as w:
        assert w.getframerate()==SR and w.getsampwidth()==2
        a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
        return a.reshape(-1,w.getnchannels())
voice=read('voice.wav');foley=read('foley.wav')
assert len(voice)==len(foley)==N
accent=np.zeros((N,2));events=[]
cues=json.loads((ROOT/'src/graphics-v3/cues.json').read_text())
def band(n,low,high):
    s=np.fft.rfft(rng.normal(size=n)); hz=np.fft.rfftfreq(n,1/SR)
    mask=np.clip((hz-low)/max(low,.1),0,1)*np.clip((high-hz)/(high*.25),0,1)
    a=np.fft.irfft(s*mask,n=n); return a/max(.0001,np.std(a))
def sound(kind,gain):
    length={'tick':.14,'reveal':.34,'low':.28,'glass':.29,'sweep':.36,'reverse':.31,'double':.42,'chime':.39}[kind]
    t=np.arange(round(SR*length))/SR
    if kind=='tick':
        a=(np.sin(2*np.pi*720*t)*.7+band(len(t),900,4300)*.18)*np.exp(-t*43)
    elif kind=='reveal':
        a=band(len(t),650,5300)*np.sin(np.pi*t/length)**2*.35
        a+=np.sin(2*np.pi*(290*t+360*t*t))*.24*np.exp(-t*12)
    elif kind=='low':
        a=(np.sin(2*np.pi*(112*t-54*t*t))*.8+band(len(t),250,1300)*.09)*np.exp(-t*18)
    elif kind=='glass':
        a=(np.sin(2*np.pi*1690*t)+.4*np.sin(2*np.pi*2413*t)+.23*np.sin(2*np.pi*3371*t))*.42*np.exp(-t*24)
    elif kind in ('sweep','reverse'):
        env=np.sin(np.pi*t/length)**2
        a=band(len(t),450,4200)*env*.32
        if kind=='reverse':a*=t/length
    elif kind=='chime':
        a=(np.sin(2*np.pi*784*t)*.6+np.sin(2*np.pi*1176*t)*.26+np.sin(2*np.pi*1568*t)*.14)*np.exp(-t*12)
    else:
        a=np.sin(2*np.pi*587.33*t)*np.exp(-t*16)*.5
        delayed=np.maximum(0,t-.10)
        a+=np.sin(2*np.pi*880*delayed)*np.exp(-delayed*15)*.55*(t>=.10)
    # Short rounded attack; no clicks at the sample boundary.
    a*=np.minimum(1,t/.006)*np.minimum(1,(length-t)/.025)
    return a*gain*6.3
def add(at,kind,gain,pan,label):
    a=sound(kind,gain);start=round(at*SR);n=min(len(a),N-start);a=a[:n]
    accent[start:start+n,0]+=a*np.sqrt((1-pan)/2)
    accent[start:start+n,1]+=a*np.sqrt((1+pan)/2)
    events.append({'time':at,'duration':n/SR,'type':kind,'visual':label})
for key,cue in cues.items():
    add(cue['from'],cue['sound'],cue['gain'],-.22 if key!='there' else .22,key)
for at,label in [(.78,'AMPEL'),(3.2,'ASPHALT'),(7.7,'REIFEN'),(16.26,'LOS'),(29.12,'VORAUS')]:
    add(at,'tick',.013,-.16,label)
# Graphic accents automatically make room for speech; the supplied performance
# stays at its canonical speed, pitch, start sample and gain.
env=np.convolve(np.abs(voice[::48,0]),np.ones(65)/65,mode='same')
env=np.interp(np.arange(N),np.arange(len(env))*48,env)
accent*= (1-.53*np.clip(env/.055,0,1))[:,None]
accent*=np.minimum(1,(30-np.arange(N)/SR)/.13)[:,None]
accent=np.clip(accent,-1,1)
pcm=(accent*32767).astype('<i2');accent=pcm.astype(float)/32768
mix=voice+foley+accent
assert np.abs(mix).max()<.92, 'Mix requires deliberate gain adjustment'
for name,a in [('accent-v3.wav',accent),('mix-v3.wav',mix)]:
    with wave.open(str(DEST/name),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
report={'sample_rate':SR,'duration':30,'voice_changed':False,'source':'Original locally synthesized sound effects','speech_ducking':True,'accent_peak':float(np.abs(accent).max()),'mix_peak':float(np.abs(mix).max()),'events':events}
(ROOT/'docs/audio-cues-v3.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='events'},ensure_ascii=False))
