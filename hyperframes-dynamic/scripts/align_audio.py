"""Local word timing for the supplied full-length German recording. No audio upload."""
from pathlib import Path
import json,os,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('HF_HOME',str(ROOT.parent/'.models/hf'))
os.environ.setdefault('HF_HUB_OFFLINE','1')
from faster_whisper import WhisperModel
source=Path(sys.argv[1]);out=ROOT/'production';out.mkdir(exist_ok=True)
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-ac','1','-ar','16000','-f','f32le','-'])
audio=np.frombuffer(raw,dtype='<f4')
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,num_workers=1,local_files_only=True)
segments,_=model.transcribe(audio,language='de',beam_size=5,word_timestamps=True,condition_on_previous_text=False)
result=[]
for s in segments:
 result.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]})
 print(f'{s.start:.2f}–{s.end:.2f} {s.text}',flush=True)
(out/'alignment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Local alignment complete',len(audio)/16000,'seconds',flush=True)
