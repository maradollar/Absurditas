"""Local optional word timing. Audio is kept local; only the free model is downloaded."""
from pathlib import Path
import subprocess,sys,json,os
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:raise SystemExit('Usage: .venv/bin/python scripts/align_whatif.py /path/to/voice.mp3')
os.environ.setdefault('HF_HOME',str(ROOT/'.models/hf'))
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
from faster_whisper import WhisperModel
# Supported ndarray input avoids a PyAV 19 API mismatch in faster-whisper 1.2.1.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',sys.argv[1],'-t','42','-ac','1','-ar','16000','-f','f32le','-'])
audio=np.frombuffer(raw,dtype='<f4')
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,num_workers=1)
segments,_=model.transcribe(audio,language='de',beam_size=5,word_timestamps=True,condition_on_previous_text=False)
result=[]
for s in segments:
 result.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]})
 print(f'{s.start:.2f}–{s.end:.2f} {s.text}')
out=ROOT/'docs/voice-alignment.json';out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
