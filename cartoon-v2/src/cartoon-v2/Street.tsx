import React from 'react';
import {P,Pt,points,blend} from './math';
import {PedestrianLamp,VehicleLamp} from './Props';
const Window:React.FC<{x:number;y:number;w?:number;h?:number}>=({x,y,w=85,h=125})=><g transform={`translate(${x} ${y})`}>
 <path d={`M-5-5H${w+6}V${h+9}H-5Z`} fill="#d5c8b5"/>
 <rect width={w} height={h} fill="#b4cdd6"/>
 <path d={`M3 3V${h-2}H${w-2}`} stroke="#e6ddcb" strokeWidth="8" fill="none"/>
 <path d={`M${w/2} 2V${h-2}`} stroke="#e9dfcc" strokeWidth="5"/>
 <path d={`M-9 ${h+8}H${w+11}`} stroke="#afa491" strokeWidth="7"/>
 <path d={`M8 16L${w-15} 11V26L8 34Z`} fill="#d4e0dd" opacity=".35"/>
 </g>;
const Tree:React.FC<{x:number;y:number;s:number;f:number}>=({x,y,s,f})=><g transform={`translate(${x} ${y}) scale(${s})`}>
 <path d="M-11 0L-5-157L7-182L17 0Z" fill="#7b715b"/><path d="M-4-135L-49-183M5-99l46-83" stroke="#7b715b" strokeWidth="10" strokeLinecap="round"/>
 <g transform={`rotate(${Math.sin(f*.012)*.45} 0 -130)`}><path d="M-72-142Q-116-162-96-212Q-115-253-62-266Q-37-309 6-277Q60-304 76-262Q123-259 111-215Q133-167 78-153Q36-125-3-145Q-45-117-72-142Z" fill="#7fa17b"/><path d="M-78-218Q-55-259-17-247Q11-274 46-253" stroke="#91b38b" strokeWidth="14" fill="none" strokeLinecap="round" opacity=".65"/></g>
 </g>;
export const Street:React.FC<{f:number;green:boolean;blur?:boolean}>=({f,green,blur=false})=><g>
 <rect x="-2000" y="-1000" width="6000" height="3000" fill="url(#v2-sky)"/>
 <g filter={blur?'url(#v2-soft)':undefined}>
 <g opacity=".52"><path d="M-200 90H160V580H-200ZM270 50H700V580H270ZM810 115H1250V580H810ZM1400 45H2070V580H1400Z" fill="#d0c9bb"/>
 {Array.from({length:18},(_,i)=><rect key={i} x={-100+i*133} y={155+(i%3)*21} width="68" height="111" fill="#bfd2d4"/>)}</g>
 <path d="M-120 240H454V620H-120Z" fill="#ddcfb9"/><path d="M454 240L517 270V620H454Z" fill="#bbaa94"/>
 <path d="M-130 245H468V271H-130Z" fill="#c9b89e"/>
 <Window x={-20} y={304}/><Window x={150} y={304}/><Window x={320} y={304}/>
 <rect x="-20" y="474" width="375" height="147" fill="#b1cbd4"/>
 <path d="M-30 478H370L393 440H-35Z" fill="#cba353"/><path d="M-30 478H370L368 491H-30Z" fill="#b28c49"/>
 <path d="M112 487V620M271 487V620" stroke="#e9e0d0" strokeWidth="12"/>
 <path d="M540 165H1108V620H540Z" fill="#e5d8c4"/><path d="M1108 165L1180 211V620H1108Z" fill="#cabca5"/>
 <path d="M524 165H1122V194H524Z" fill="#d2c2a9"/>
 <Window x={585} y={230} w={105} h={120}/><Window x={780} y={230} w={105} h={120}/><Window x={970} y={230} w={93} h={120}/>
 <rect x="582" y="409" width="493" height="212" fill="#b9d4dc"/><path d="M596 430L738 414V575L596 592Z" fill="#c7dde0" opacity=".7"/>
 <path d="M580 620V410H1078V620M744 416V620M914 416V620" stroke="#ede4d3" strokeWidth="13" fill="none"/>
 <path d="M555 408H1102L1080 362H570Z" fill="#b57461"/><path d="M555 408H1102V426H555Z" fill="#985e50"/>
 <g transform="translate(771 371)"><rect x="-33" y="-63" width="130" height="38" rx="4" fill="#b9a286"/><text x="32" y="-36" textAnchor="middle" fill="#f5e6c9" fontSize="21" fontWeight="700" letterSpacing="5">CAFÉ</text></g>
 <path d="M1450 665L1515 300H1630L1811 665Z" fill="#a3a4a0"/><path d="M1620 360L1637 405M1648 441L1668 494M1681 530L1705 594" stroke="#d4cdba" strokeWidth="5" fill="none"/><path d="M1180 225H1450V621H1180Z" fill="#dbceb9"/><path d="M1450 225L1500 252V621H1450Z" fill="#c3b39a"/>
 <Window x={1210} y={285} w={83} h={107}/><Window x={1340} y={285} w={83} h={107}/>
 <path d="M1208 456H1430V620H1208Z" fill="#b4cfd3"/><path d="M1190 448H1456L1437 412H1208Z" fill="#6d9290"/><path d="M1190 448H1456V462H1190Z" fill="#527775"/>
 <path d="M1320 463V620" stroke="#e9dfce" strokeWidth="11"/>
 <path d="M1811 282H2150V620H1811Z" fill="#e8dac5"/>
 <Tree x={1870} y={629} s={1.14} f={f}/>
 </g>
 <path d="M-200 622H2200V656H-200Z" fill="#c5c1b5"/>
 <path d="M-200 653H2200V665H-200Z" fill="#dcd7c7"/>
 <path d="M-200 665H2200V940H-200Z" fill="url(#v2-road)"/>
 <path d="M-200 753H2200" stroke="#d8d0bd" strokeWidth="5" strokeDasharray="80 61" opacity=".7"/>
 <path d="M556 675L530 922" stroke="#e4dfd0" strokeWidth="11"/>
 <g fill="#e9e4d4">{Array.from({length:8},(_,i)=>{const t=(i+.05)/8,u=t+.070;const strip=(v:number):Pt[]=>{const y=blend(937,668,v),x=blend(970,1150,v),w=blend(260,179,v);return [[x-w/2,y],[x+w/2,y]]};const a=strip(t),b=strip(u);return <polygon key={i} points={points([a[0],a[1],b[1],b[0]])}/>})}</g>
 <path d="M-200 943H2200V1600H-200Z" fill="#c0b9aa"/>
 <path d="M-200 943H2200" stroke="#e5ddca" strokeWidth="13"/>
 <path d="M-200 954H2200" stroke="#8f8b82" strokeWidth="7"/>
 <g stroke="#a29e92" strokeWidth="1.5" fill="none" opacity=".7"><path d="M-200 1038H2200M-200 1139H2200M-200 1260H2200"/>{Array.from({length:10},(_,i)=><path key={i} d={`M${i*240-70} 951L${i*270-180} 1310`}/>)}</g>
 <VehicleLamp x={537} y={647}/>
 <PedestrianLamp x={1270} y={651} scale={.94} green={green}/>
 </g>;
