import React from 'react';
import {AbsoluteFill, Easing, cancelRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/fonts';
import cues from './cues.json';
import {tween} from '../cartoon-v2/math';

loadFont({family:'ManropeV3',url:staticFile('fonts/Manrope.ttf'),weight:'800'}).catch(cancelRender);

const C={cream:'#fff4dc',amber:'#ffc255',mint:'#b9f2bb',ink:'#17151d'};
const out=Easing.bezier(0.16,1,0.3,1);
const progress=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:out});
type Cue=keyof typeof cues;
type Word={text:string;at:number;x:number;y?:number;size:number;color?:string};
type PhraseProps={cue:Cue;x:number;y:number;words:Word[];underline?:{x:number;y:number;width:number;at:number;color?:string}};

/** One authored phrase per JSX node; the small word instances share one reveal template. */
const Phrase:React.FC<PhraseProps>=({cue,x,y,words,underline})=>{
 const f=useCurrentFrame(),{fps}=useVideoConfig();const c=cues[cue];
 if(f<c.from*fps||f>=c.to*fps)return null;
 const exit=progress(f,c.to*fps-7,c.to*fps);
 return <g data-cue={cue} transform={`translate(${x} ${y-exit*14})`} opacity={1-exit}>
  {words.map((w,i)=>{const p=progress(f,w.at*fps,w.at*fps+11);const yy=w.y??0;return <g key={i}>
   <defs><clipPath id={`v3-mask-${cue}-${i}`}><rect x={w.x-15} y={yy-w.size-12} width="1500" height={w.size+24}/></clipPath></defs>
   <g clipPath={`url(#v3-mask-${cue}-${i})`} opacity={progress(f,w.at*fps,w.at*fps+4)}>
    <text data-word={w.text} x={w.x} y={yy+(1-p)*w.size*.70} fontSize={w.size} fontWeight="800" letterSpacing={-w.size*.035} fill={w.color??C.cream} stroke={C.ink} strokeWidth={Math.max(3,w.size*.039)} strokeLinejoin="round" paintOrder="stroke" filter="url(#v3-type-shadow)">{w.text}</text>
   </g>
  </g>})}
  {underline&&<path d={`M${underline.x} ${underline.y} Q${underline.x+underline.width*.45} ${underline.y+7} ${underline.x+underline.width} ${underline.y-2}`} pathLength="1" stroke={underline.color??C.amber} strokeWidth="9" fill="none" strokeLinecap="round" strokeDasharray="1" strokeDashoffset={1-progress(f,underline.at*fps,underline.at*fps+13)}/>} 
 </g>;
};

/** A phone-local bracket follows the real phone/camera transform, not a floating UI. */
const PhoneAccent:React.FC=()=>{const f=useCurrentFrame(),{fps}=useVideoConfig();const c=cues.broken;if(f<c.from*fps||f>c.to*fps)return null;const p=progress(f,c.from*fps,c.from*fps+12),fade=1-progress(f,c.to*fps-8,c.to*fps);return <g opacity={p*fade}>
 <g transform={`translate(960 540) scale(${tween(f,130,198,4.8,5.2)}) translate(-838 ${-tween(f,130,198,879,883)}) translate(838 879) rotate(-13) matrix(.9 .12 -.39 .42 0 0)`}>
 <path d="M-35-31V-59H-9M10-59H36V-31M36 30V59H10M-9 59H-35V30" fill="none" stroke={C.amber} strokeWidth={1.8} strokeLinecap="round"/>
 <path d="M-3-5L-16-25L-12-39M-3-5L16-29M-3-5L20 4M-3-5L-10 15L-19 29M-10 15L9 35" pathLength="1" stroke={C.cream} strokeWidth="2.1" fill="none" strokeDasharray="1" strokeDashoffset={1-p}/>
 </g></g>};

const SceneAccents:React.FC=()=>{
 const f=useCurrentFrame(),{fps}=useVideoConfig();
 const burst=progress(f,1.48*fps,1.48*fps+13)*(1-progress(f,2.18*fps,2.55*fps));
 const green=progress(f,14.52*fps,14.52*fps+9)*(1-progress(f,15.23*fps,15.48*fps));
 const at=19.32*fps,draw=progress(f,at,at+23),fade=1-progress(f,21.10*fps,21.37*fps);
 const arrowHead=progress(f,at+16,at+24)*fade;
 const changed=progress(f,24.4*fps,24.4*fps+15)*(1-progress(f,25.28*fps,25.53*fps));
 return <>
  <g stroke={C.amber} strokeWidth="7" strokeLinecap="round" opacity={burst}>{[0,1,2,3,4,5,6,7].map(i=><path key={i} d={`M${1007+Math.cos(i*Math.PI/4)*(23+22*burst)} ${163+Math.sin(i*Math.PI/4)*(23+22*burst)} l${Math.cos(i*Math.PI/4)*18} ${Math.sin(i*Math.PI/4)*18}`}/>)}</g>
  <PhoneAccent/>
  <g opacity={green} fill="none" stroke={C.mint} strokeWidth="5"><circle cx="1270" cy="439.5" r={30+green*28}/><circle cx="1270" cy="439.5" r={37+green*50} opacity=".45"/></g>
  <g fill="none" stroke={C.amber} strokeLinecap="round" strokeLinejoin="round" opacity={fade}>
   <path d="M1532 274C1490 438 1190 490 1054 800" stroke={C.ink} strokeWidth="11" pathLength="1" strokeDasharray="1" strokeDashoffset={1-draw}/>
   <path d="M1532 274C1490 438 1190 490 1054 800" strokeWidth="5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-draw}/>
   <path d="M1047 772L1054 800L1082 787" stroke={C.ink} strokeWidth="11" opacity={arrowHead}/><path d="M1047 772L1054 800L1082 787" strokeWidth="5" opacity={arrowHead}/>
   <ellipse cx="1035" cy="850" rx="83" ry="23" strokeWidth="5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(f,at+16,at+32)}/>
  </g>
  <g opacity={changed} transform="translate(148 397)"><circle r="24" fill={C.mint} stroke={C.ink} strokeWidth="4"/><path d="M-10 0L-3 8L12-9" fill="none" stroke={C.ink} strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(f,24.4*fps,24.4*fps+15)}/></g>
 </>;
};

export const EmphasisLayer:React.FC=()=> <AbsoluteFill style={{pointerEvents:'none'}}>
 <svg width="1920" height="1080" viewBox="0 0 1920 1080" style={{position:'absolute',fontFamily:'ManropeV3, sans-serif'}}>
 <defs><filter id="v3-type-shadow" x="-20%" y="-50%" width="140%" height="200%"><feDropShadow dx="0" dy="5" stdDeviation="3" floodColor="#17151d" floodOpacity=".24"/></filter></defs>
 <Phrase cue="ampel" x={140} y={158} words={[{text:'EINE',at:.58,x:0,size:66},{text:'AMPEL.',at:.78,x:0,y:112,size:124,color:C.amber}]} underline={{x:0,y:132,width:392,at:.95}}/>
 <Phrase cue="suddenly" x={140} y={195} words={[{text:'PLÖTZLICH.',at:1.48,x:0,size:126,color:C.amber}]} underline={{x:0,y:24,width:742,at:1.7}}/>
 <Phrase cue="asphalt" x={140} y={157} words={[{text:'AUF DEM',at:2.8,x:0,size:70},{text:'ASPHALT.',at:3.2,x:0,y:114,size:124}]} underline={{x:3,y:137,width:555,at:3.5}}/>
 <Phrase cue="broken" x={140} y={192} words={[{text:'ZERBROCHEN.',at:5.34,x:0,size:114,color:C.amber}]}/>
 <Phrase cue="tyres" x={140} y={152} words={[{text:'QUIETSCHENDE',at:7.1,x:0,size:72},{text:'REIFEN.',at:7.7,x:0,y:114,size:126,color:C.amber}]}/>
 <Phrase cue="gone" x={140} y={196} words={[{text:'VERSCHWUNDEN.',at:9.6,x:0,size:95}]}/>
 <Phrase cue="later" x={140} y={154} words={[{text:'1 MINUTE',at:12.94,x:0,size:102,color:C.amber},{text:'SPÄTER.',at:13.32,x:0,y:108,size:112}]}/>
 <Phrase cue="green" x={140} y={207} words={[{text:'GRÜN.',at:14.52,x:0,size:138,color:C.mint}]} underline={{x:2,y:24,width:353,at:14.7,color:C.mint}}/>
 <Phrase cue="stop" x={140} y={161} words={[{text:'NICHT',at:16.14,x:0,size:110,color:C.amber},{text:'LOS.',at:16.26,x:0,y:113,size:132}]}/>
 <Phrase cue="there" x={1180} y={217} words={[{text:'GENAU',at:19.32,x:0,size:80},{text:'DORT.',at:19.6,x:286,size:80,color:C.amber}]}/>
 <Phrase cue="future" x={140} y={318} words={[{text:'ZUKUNFT',at:22.84,x:0,size:87,color:C.amber},{text:'GESEHEN.',at:23.18,x:0,y:103,size:90}]}/>
 <Phrase cue="changed" x={140} y={325} words={[{text:'VERÄNDERT.',at:24.32,x:0,size:84,color:C.mint}]}/>
 <Phrase cue="question" x={140} y={306} words={[{text:'WAS WÄRE,',at:25.72,x:0,size:78},{text:'WENN …?',at:26.14,x:0,y:104,size:90,color:C.amber}]}/>
 <Phrase cue="ahead" x={140} y={300} words={[{text:'1 MINUTE',at:28.58,x:0,size:105,color:C.amber},{text:'VORAUS.',at:29.12,x:0,y:117,size:112}]} underline={{x:3,y:144,width:482,at:29.3}}/>
 <SceneAccents/>
 </svg>
 </AbsoluteFill>;
