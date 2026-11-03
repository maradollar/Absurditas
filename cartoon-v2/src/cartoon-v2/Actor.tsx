import React from 'react';
import {P,Pt,ik,tween,pulse,blend} from './math';
import {Phone} from './Props';
export type Acting={hip:number;bob:number;lean:number;tilt:number;gaze:Pt;surprise:number;relief:number;frontHand:Pt;backHand:Pt;frontFoot:Pt;backFoot:Pt;clench:number;f:number};
export const acting=(f:number):Acting=>{
 const alarm=pulse(f,261,283,362),pre=pulse(f,37,45,48),lean=pulse(f,433,456,482),lift=pulse(f,445,464,486);
 const inspect=tween(f,661,713,0,1)*(1-tween(f,758,816,0,1));
 const lookCar=tween(f,486,590,-1,1);
 let gaze:Pt=[tween(f,0,34,14,21),tween(f,0,34,12,-12)];
 if(f>=260&&f<389)gaze=[tween(f,294,357,14,-20),-3];
 if(f>=389&&f<453)gaze=[20,-12];
 if(f>=453&&f<650)gaze=[lookCar*22,1];
 if(f>=650)gaze=[blend(22,17,inspect),blend(0,16,inspect)];
 const lower=tween(f,390,440,0,1);
 return {hip:lean*8-3, bob:Math.sin(f*.044)*1.5+lift*3, lean:lean*4.8-alarm*1.5,tilt:alarm*-5+lean*4+inspect*8.5,
 gaze,surprise:Math.max(alarm,pre,lift*.65),relief:tween(f,645,735,0,.8),
 frontHand:[blend(160,132,lower)+inspect*14,blend(-315,-275,lower)-alarm*25+inspect*8.54],
 backHand:[-101-alarm*10,-183-alarm*49+lean*5],
 frontFoot:[53+lift*36,-lift*46],backFoot:[-46,0],clench:alarm,f};
};
const Leg:React.FC<{hip:Pt;foot:Pt;rear?:boolean}>=({hip,foot,rear=false})=>{
 const knee=ik(hip,foot,102,102,-1);const d=`M ${hip.join(' ')} L ${knee.join(' ')} L ${foot.join(' ')}`;
 return <g>
 <path d={d} fill="none" stroke="#f2d5ad" strokeWidth="27" strokeLinecap="round" strokeLinejoin="round" transform="translate(-2 -1)" opacity={rear?.45:.75}/>
 <path d={d} fill="none" stroke={rear?'#232028':P.ink} strokeWidth="22" strokeLinecap="round" strokeLinejoin="round"/>
 <path d={`M ${foot[0]-12} ${foot[1]-8} Q ${foot[0]+7} ${foot[1]-12} ${foot[0]+20} ${foot[1]-3} L ${foot[0]+32} ${foot[1]+6} Q ${foot[0]+35} ${foot[1]+14} ${foot[0]+21} ${foot[1]+15} L ${foot[0]-17} ${foot[1]+15} Q ${foot[0]-23} ${foot[1]+5} ${foot[0]-12} ${foot[1]-8} Z`} fill={rear?'#211e26':P.ink} stroke={P.ink} strokeWidth="3"/>
 <path d={`M ${foot[0]-17} ${foot[1]+13} H ${foot[0]+26}`} stroke="#4a4041" strokeWidth="2"/>
 </g>;
};
const Sleeve:React.FC<{a:Pt;b:Pt;rear?:boolean}>=({a,b,rear=false})=>{
 const e=ik(a,b,rear?145:130,rear?145:80,rear?-1:1);
 const d=`M ${a.join(' ')} L ${e.join(' ')} L ${b.join(' ')}`;
 return <g>
 <path d={d} stroke={P.rim} strokeWidth="49" fill="none" strokeLinecap="round" strokeLinejoin="round" transform="translate(-3 -3)"/>
 <path d={d} stroke={P.ink} strokeWidth="45" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
 <path d={d} stroke={rear?'#ed9507':'#ffa70b'} strokeWidth="38" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
 <path d={`M ${e[0]-10} ${e[1]-10} L ${e[0]+11} ${e[1]-9}`} stroke="#c77b0e" strokeWidth="2.5" fill="none" opacity=".65"/>
 <circle cx={a[0]} cy={a[1]} r="23" fill={rear?'#ec9509':'#ffa70b'} stroke={P.ink} strokeWidth="3"/>
 </g>;
};
export const Face:React.FC<{gaze:Pt;surprise:number;relief:number;f:number;closed?:boolean}>=({gaze,surprise,relief,f,closed=false})=>{
 const blink=((f+51)%147)>139;const shut=closed||blink;const faceX=gaze[0]*2.2,faceY=gaze[1]*.8;
 return <g>
 <circle cx="-5" cy="-4" r="94" fill={P.rim}/>
 <path d="M-88-24Q-72-89-9-92Q48-97 80-46Q99-3 78 47Q45 92-5 92Q-72 93-90 38Q-100 5-88-24Z" fill={P.ink} stroke="#171219" strokeWidth="2"/>
 <g transform={`translate(${faceX} ${faceY})`} fill={P.white} stroke={P.white} strokeLinecap="round" strokeLinejoin="round">
 {shut?<><path d="M-31-8q10 8 20 0M12-8q10 8 20 0" fill="none" strokeWidth="4"/></>:<>
 <ellipse cx="-22" cy="-8" rx={6.5+surprise*2.7} ry={9.5+surprise*5} stroke="none"/>
 <ellipse cx="22" cy="-8" rx={6.5+surprise*2.7} ry={9.5+surprise*5} stroke="none"/>
 </>}
 <path d={`M -32 ${-35-surprise*12} L -15 ${-37-surprise*9} M 14 ${-37-surprise*9} L 31 ${-35-surprise*12}`} strokeWidth="5" fill="none"/>
 {surprise>.4?<ellipse cy="31" rx={4+surprise*3} ry={4+surprise*7} stroke="none"/>:<path d={`M -10 31 Q 0 ${32+relief*12} 12 29`} fill="none" strokeWidth="4"/>}
 </g>
 </g>;
};
export const Actor:React.FC<{x?:number;y?:number;scale?:number;f:number;pose?:Acting}>=({x=820,y=960,scale=.9,f,pose})=>{
 const a=pose??acting(f);const sway=Math.sin(f*.07)*.8;
 const body='M -67 -487 Q -23 -501 19 -495 Q 64 -490 74 -459 L 86 -208 Q 4 -196 -91 -211 L -79 -459 Q -84 -476 -67 -487 Z';
 return <g transform={`translate(${x} ${y}) scale(${scale})`}>
 <ellipse cx="5" cy="17" rx="104" ry="13" fill="#423e3d" opacity=".18" filter="url(#v2-shadow)"/>
 <Leg hip={[a.hip-36,-202+a.bob]} foot={a.backFoot} rear/>
 <Leg hip={[a.hip+37,-202+a.bob]} foot={a.frontFoot}/>
 <g transform={`translate(${a.hip} ${a.bob}) rotate(${a.lean} 0 -205)`}>
 <Sleeve a={[-70,-459]} b={a.backHand} rear/>
 <path d="M-60-472Q-67-521-10-526Q40-534 67-487L53-450Z" fill="#d98402" stroke={P.ink} strokeWidth="4"/>
 <path d={body} fill={P.rim} stroke={P.rim} strokeWidth="10" transform="translate(-3 -2)"/>
 <path d={body} fill="url(#v2-hood)" stroke={P.ink} strokeWidth="4"/>
 <path d="M-67-461L-69-223" stroke="#ffd47b" strokeWidth="5" fill="none" strokeLinecap="round"/>
 <path d="M-51-258H49L63-219H-65Z" fill="#e38c04"/>
 <path d="M-51-258L-61-235M49-258L59-235" stroke="#c97904" strokeWidth="3"/>
 <path d="M-84-210Q2-199 83-209" stroke="#b97109" strokeWidth="3" fill="none"/>
 <path d={`M -25 -474 Q ${-25+sway} -397 ${-28+sway*2} -326 M 24 -474 Q ${24-sway} -397 ${27-sway*2} -326`} stroke={P.white} strokeWidth="5" fill="none"/>
 <path d={`M ${-28+sway*2} -329 v12 M ${27-sway*2} -329 v12`} stroke="#fff3d7" strokeWidth="8" strokeLinecap="round"/>
 <path d="M-15-527H15V-479Q2-472-15-481Z" fill={P.ink}/>
 <Sleeve a={[66,-458]} b={a.frontHand}/>
 <g transform={`translate(${a.frontHand[0]+12} ${a.frontHand[1]-25}) rotate(${blend(-10,-3,a.clench)}) scale(.8)`}><Phone/></g>
 <g transform={`translate(${a.frontHand.join(' ')})`}>
 <ellipse cx="-4" cy="-4" rx="23" ry="24" fill={P.rim}/>
 <circle r="21" fill={P.ink}/><ellipse cx="14" cy="-7" rx="7" ry="12" fill="#18151d" transform="rotate(-22 14 -7)"/>
 </g>
 <g transform={`translate(${a.backHand.join(' ')})`}><circle cx="-4" cy="-4" r="23" fill={P.rim}/><circle r="21" fill={P.ink}/></g>
 <g transform={`translate(0 -600) rotate(${a.tilt})`}><Face gaze={a.gaze} surprise={a.surprise} relief={a.relief} f={f}/></g>
 </g>
 </g>;
};
/** Authored floor pose: separate silhouette, limbs and floor contacts, not a rotated idle rig. */
export const FallenActor:React.FC=()=> <g transform="translate(856 787) scale(.83)">
 <ellipse cx="270" cy="101" rx="360" ry="39" fill="#41434c" opacity=".26" filter="url(#v2-shadow)"/>
 <g fill="none" strokeLinecap="round" strokeLinejoin="round">
 <path d="M310 61L425 31L556 45" stroke={P.rim} strokeWidth="28" transform="translate(-2 -2)"/><path d="M310 61L425 31L556 45" stroke="#17151c" strokeWidth="23"/>
 <path d="M310 81L425 102L556 100" stroke={P.rim} strokeWidth="29" transform="translate(-2 -2)"/><path d="M310 81L425 102L556 100" stroke="#17151c" strokeWidth="24"/>
 <path d="M552 35L580 46L580 58L547 59Z" fill={P.ink} stroke={P.ink} strokeWidth="5"/><path d="M552 92L584 99L585 112H543Z" fill={P.ink} stroke={P.ink} strokeWidth="5"/>
 <path d="M94 18L144 115L198 102" stroke={P.rim} strokeWidth="42" transform="translate(-3 -2)"/><path d="M94 18L144 115L198 102" stroke={P.ink} strokeWidth="38"/><path d="M94 18L144 115L198 102" stroke="#ef9705" strokeWidth="31"/>
 </g>
 <path d="M63-4Q116-18 163-3L314 23L311 95L153 103L85 83Q66 55 63-4Z" fill="url(#v2-hood)" stroke={P.ink} strokeWidth="4"/>
 <path d="M64-5Q121-19 161-4" stroke={P.rim} strokeWidth="6" fill="none"/>
 <path d="M247 41L297 49L295 82L244 74Z" fill="#df8705"/>
 <path d="M90 11L153 23M91 28L152 43" stroke={P.white} strokeWidth="4"/><path d="M149 22l8 2M150 43l8 2" stroke={P.white} strokeWidth="7" strokeLinecap="round"/>
 <path d="M77 26L112 68L72 112" stroke={P.rim} strokeWidth="41" fill="none" strokeLinecap="round" strokeLinejoin="round" transform="translate(-3 -2)"/>
 <path d="M77 26L112 68L72 112" stroke={P.ink} strokeWidth="38" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
 <path d="M77 26L112 68L72 112" stroke="#ffa60b" strokeWidth="31" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
 <circle cx="72" cy="112" r="22" fill={P.ink}/><circle cx="201" cy="102" r="21" fill={P.ink}/>
 <path d="M21 22L86 25" stroke={P.ink} strokeWidth="24"/>
 <g transform="translate(-3 -3) rotate(-20) scale(.96)"><Face gaze={[-9,6]} surprise={0} relief={0} f={0} closed/></g>
 </g>;
