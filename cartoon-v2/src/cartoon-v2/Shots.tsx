import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {CameraWorld,Camera,wide} from './World';
import {tween} from './math';
const Frame:React.FC<{f:number;vision?:boolean;camera?:Camera;soft?:boolean;phone?:boolean}>=({f,vision=false,camera=wide,soft=false,phone=false})=><AbsoluteFill style={{background:'#d8c8af'}}><CameraWorld f={f} vision={vision} camera={camera} softBackground={soft} phoneFocus={phone}/></AbsoluteFill>;
/** Every shot uses the same street coordinates; only cameras and story state differ. */
export const OpeningShot:React.FC=()=>{const f=useCurrentFrame();return <Frame f={f} camera={{x:960,y:540,zoom:tween(f,0,44,1,1.025)}}/>};
export const VisionShot:React.FC=()=>{const f=45+useCurrentFrame();return <Frame f={f} vision camera={{x:960,y:540,zoom:1.025}}/>};
export const PhoneShot:React.FC=()=>{const f=130+useCurrentFrame();return <Frame f={f} vision camera={{x:838,y:tween(f,130,198,879,883),zoom:tween(f,130,198,4.8,5.2)}} soft phone/>};
export const WheelShot:React.FC=()=>{const f=199+useCurrentFrame();return <Frame f={f} vision camera={{x:tween(f,199,248,1601,1661),y:768,zoom:2.5}} soft/>};
export const ReturnShot:React.FC=()=>{const f=260+useCurrentFrame();return <Frame f={f} camera={{x:tween(f,278,330,960,935),y:tween(f,278,330,540,570),zoom:tween(f,278,330,1.025,1.09)}}/>};
export const GreenShot:React.FC=()=>{const f=389+useCurrentFrame();return <Frame f={f} camera={{x:tween(f,389,421,935,960),y:tween(f,389,421,570,540),zoom:tween(f,389,421,1.09,1)}}/>};
export const DecisionShot:React.FC=()=>{const f=454+useCurrentFrame();return <Frame f={f}/>};
export const RealisationShot:React.FC=()=>{const f=654+useCurrentFrame();return <Frame f={f} camera={{x:tween(f,654,870,960,842),y:tween(f,654,870,540,565),zoom:tween(f,654,870,1,1.65)}} soft/>};
