import React from 'react';
import {AbsoluteFill,Series,useVideoConfig,staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {OpeningShot,VisionShot,PhoneShot,WheelShot,ReturnShot,GreenShot,DecisionShot,RealisationShot} from './Shots';
export const CartoonFilm:React.FC=()=>{const {fps}=useVideoConfig();return <AbsoluteFill>
 <Series>
 <Series.Sequence name="Warten am Bordstein" durationInFrames={45} premountFor={fps}><OpeningShot/></Series.Sequence>
 <Series.Sequence name="Zukunft am selben Überweg" durationInFrames={85} premountFor={fps}><VisionShot/></Series.Sequence>
 <Series.Sequence name="Beschädigtes Telefon auf dem Asphalt" durationInFrames={69} premountFor={fps}><PhoneShot/></Series.Sequence>
 <Series.Sequence name="Das tatsächliche bremsende Fahrzeug" durationInFrames={61} premountFor={fps}><WheelShot/></Series.Sequence>
 <Series.Sequence name="Zurück auf dem Gehweg" durationInFrames={129} premountFor={fps}><ReturnShot/></Series.Sequence>
 <Series.Sequence name="Zeitellipse und grüne Ampel" durationInFrames={65} premountFor={fps}><GreenShot/></Series.Sequence>
 <Series.Sequence name="Schrittabbruch und Vorbeifahrt" durationInFrames={200} premountFor={fps}><DecisionShot/></Series.Sequence>
 <Series.Sequence name="Erkenntnis in derselben Straße" durationInFrames={246} premountFor={fps}><RealisationShot/></Series.Sequence>
 </Series>
 <Audio name="ElevenLabs · Originalabschnitt 0–30 Sekunden" src={staticFile('cartoon-v2/voice.wav')} premountFor={fps}/>
 <Audio name="Ortsbezogene Geräusche" src={staticFile('cartoon-v2/foley.wav')} premountFor={fps}/>
 </AbsoluteFill>};
