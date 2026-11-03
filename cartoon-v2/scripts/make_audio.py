"""Original user performance, restrained original city/vehicle/cloth/sole sound."""
from pathlib import Path
import numpy as np
import subprocess,wave,json,shutil,sys
R=Path(__file__).resolve().parents[1];O=R/'public/cartoon-v2';O.mkdir(exist_ok=True,parents=True)
if len(sys.argv)!=2:raise SystemExit('Usage: .venv/bin/python scripts/make_audio.py /path/to/original.mp3')
source=Path(sys.argv[1])
SR=48000;N=SR*30;rng=np.random.default_rng(9030)
raw=subprocess.check_output(['ffmpeg','-v','error','-t','30','-i',str(source),'-af','highpass=f=55','-ar',str(SR),'-ac','1','-f','f32le','-'])
v=np.frombuffer(raw,dtype='<f4').copy();v=np.pad(v,(0,max(0,N-len(v))))[:N]
# Same moderate fixed gain as the previously measured canonical voice. It gives
# about -17 LUFS mono / -14 LUFS centered in stereo for this supplied performance.
v*=.7577047328658622
v*=min(1,.79/max(.001,float(np.max(np.abs(v)))))
fx=np.zeros((N,2));cues=[]
def noise(n,lo,hi):
 a=rng.normal(0,1,n);spec=np.fft.rfft(a);f=np.fft.rfftfreq(n,1/SR);mask=np.maximum(0,np.minimum(1,(f-lo)/max(lo,1)))*np.maximum(0,np.minimum(1,(hi-f)/(hi*.3)))
 b=np.fft.irfft(spec*mask,n=n);return b/max(.001,float(np.std(b)))
def add(t,a,pan,name):
 at=round(t*SR);a=a[:N-at];fx[at:at+len(a),0]+=a*np.sqrt((1-pan)/2);fx[at:at+len(a),1]+=a*np.sqrt((1+pan)/2);cues.append({'time':t,'duration':len(a)/SR,'name':name})
# Low, non-musical outdoor air.
t=np.arange(N)/SR;air=noise(N,110,1300)*.0033
fx[:,0]+=air*(.8+.2*np.sin(t*.45));fx[:,1]+=air*(.8+.2*np.cos(t*.45))
# A short perceptual pressure change on entering the premonition.
t=np.arange(int(.65*SR))/SR;add(1.48,(np.sin(2*np.pi*(155*t+32*t*t))*.014+noise(len(t),250,1200)*.002)*np.sin(np.pi*t/.65)**2,0,'Wahrnehmungswechsel')
# Tire friction belongs to the close-up of the complete car's rear wheel.
t=np.arange(int(1.05*SR))/SR;a=(np.sin(2*np.pi*(1210*t+18*np.sin(t*7)))*.023+noise(len(t),1600,5200)*.011)*np.sin(np.pi*t/1.05)**1.2
add(7.04,a,.35,'Bremsendes Fahrzeug in der Vision')
for at,length,amp,name in [(10.02,.3,.009,'Kleidung bei Rückkehr'),(15.00,.22,.009,'Gewichtsverlagerung'),(22.35,.28,.007,'Telefon kontrollieren')]:
 tt=np.arange(round(length*SR))/SR;add(at,noise(len(tt),350,2200)*np.sin(np.pi*tt/length)**2*amp,-.18,name)
t=np.arange(int(.17*SR))/SR;add(16.2,(np.sin(2*np.pi*92*t)*.022+noise(len(t),130,1900)*.012)*np.exp(-t*28),-.18,'Fuß setzt wieder auf dem Gehweg auf')
# First audible before entering the crossing, then clearly passing left -> right.
dur=5.1;t=np.arange(int(dur*SR))/SR;u=t/dur;env=np.sin(np.pi*u)**1.8
phase=2*np.pi*(118*t+11*t*t-1.9*t*t*t)
engine=(np.sin(phase)*.043+np.sin(phase*2)*.012+noise(len(t),100,2100)*.028)*env
at=round(14.1*SR);pan=np.clip((t-2.5)/1.7,-.95,.95)
fx[at:at+len(t),0]+=engine*np.sqrt((1-pan)/2);fx[at:at+len(t),1]+=engine*np.sqrt((1+pan)/2)
cues.append({'time':14.1,'duration':dur,'name':'Annäherung links, Vorbeifahrt, Entfernung rechts'})
# Time-varying, smooth speech ducking.
en=np.convolve(np.abs(v)[::48],np.ones(50)/50,mode='same');en=np.interp(np.arange(N),np.arange(len(en))*48,en)
fx*= (1-.42*np.clip(en/.06,0,1))[:,None]
fade=np.minimum(1,np.minimum(np.arange(N)/SR/.035,(30-np.arange(N)/SR)/.13));v*=fade;fx*=fade[:,None]
mix=v[:,None]+fx;scale=min(1,.89/max(.001,float(np.abs(mix).max())));v*=scale;fx*=scale;mix*=scale
for name,a in [('voice.wav',v),('foley.wav',fx),('mix.wav',mix)]:
 with wave.open(str(O/name),'wb') as w:w.setframerate(SR);w.setnchannels(1 if a.ndim==1 else 2);w.setsampwidth(2);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
(R/'docs/audio-cues.json').write_text(json.dumps({'source':source.name,'source_start':0,'source_end':30,'speed':1,'mix_peak':float(np.abs(mix).max()),'cues':cues},ensure_ascii=False,indent=2)+'\n')
print('Voice + original location-based foley ready; peak',np.abs(mix).max())
