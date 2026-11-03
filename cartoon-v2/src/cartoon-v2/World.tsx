import React from 'react';
import {staticFile} from 'remotion';
import {Street} from './Street';
import {Actor,FallenActor} from './Actor';
import {Car,Phone,FilmDefs} from './Props';
import {tween,carX,pulse} from './math';
export type Camera={x:number;y:number;zoom:number};
export const wide:Camera={x:960,y:540,zoom:1};
const futureX=(f:number)=>f<130?tween(f,45,130,1690,1840):f<199?tween(f,130,199,1840,1880):tween(f,199,248,1880,1940);
export const CameraWorld:React.FC<{f:number;vision?:boolean;camera?:Camera;softBackground?:boolean;phoneFocus?:boolean}>=({f,vision=false,camera=wide,softBackground=false,phoneFocus=false})=>{
 const vehicle=vision?futureX(f):carX(f),visible=vision||(f>=389&&f<600);
 const angle=(vehicle+1100)/(52*1.3)*180/Math.PI;
 return <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style={{position:'absolute',fontFamily:'Manrope, sans-serif'}}>
 <style>{`@font-face{font-family:Manrope;src:url('${staticFile('fonts/Manrope.ttf')}') format('truetype');font-weight:200 800;}`}</style>
 <FilmDefs/>
 <g filter={vision?'url(#v2-future)':undefined}>
 <g transform={`translate(960 540) scale(${camera.zoom}) translate(${-camera.x} ${-camera.y})`}>
 <Street f={f} green={vision||f>=436} blur={softBackground}/>
 {vision&&<path d={`M 1450 850 H ${vehicle-215*1.3}`} stroke="#48464c" strokeWidth="5" opacity=".26" strokeLinecap="round"/>}
 {visible&&<Car x={vehicle} wheelAngle={angle} braking={vision}/>}
 {vision?<>
 <g filter={phoneFocus?'url(#v2-soft)':undefined}><FallenActor/></g>
 <g transform="translate(838 879) rotate(-13)">
 <ellipse cx="7" cy="8" rx="41" ry="18" fill="#353540" opacity=".21"/>
 <g transform="matrix(.9 .12 -.39 .42 0 0)"><Phone broken/></g>
 </g>
 </>:<Actor f={f}/>}
 </g>
 </g>
 <rect width="1920" height="1080" fill="url(#v2-paper)" pointerEvents="none"/>
 <rect width="1920" height="1080" fill="url(#v2-vignette)" pointerEvents="none"/>
 {f>=45&&f<51&&<rect width="1920" height="1080" fill="#f1e8e5" opacity={pulse(f,45,47,51)*.16}/>}
 </svg>;
};
