import React from 'react';
import {Composition,Folder} from 'remotion';
import {CartoonFilm} from './cartoon-v2/CartoonFilm';
import {OpeningShot,VisionShot,PhoneShot,WheelShot,ReturnShot,GreenShot,DecisionShot,RealisationShot} from './cartoon-v2/Shots';
export const Root: React.FC = () => <>
 <Composition id="WhatIfCartoonV2" component={CartoonFilm} width={1920} height={1080} fps={30} durationInFrames={900}/>
 <Folder name="Cartoon-V2-Shots">
 <Composition id="V2-Opening" component={OpeningShot} width={1920} height={1080} fps={30} durationInFrames={45}/>
 <Composition id="V2-Vision" component={VisionShot} width={1920} height={1080} fps={30} durationInFrames={85}/>
 <Composition id="V2-Phone" component={PhoneShot} width={1920} height={1080} fps={30} durationInFrames={69}/>
 <Composition id="V2-Wheel" component={WheelShot} width={1920} height={1080} fps={30} durationInFrames={61}/>
 <Composition id="V2-Return" component={ReturnShot} width={1920} height={1080} fps={30} durationInFrames={129}/>
 <Composition id="V2-Green" component={GreenShot} width={1920} height={1080} fps={30} durationInFrames={65}/>
 <Composition id="V2-Decision" component={DecisionShot} width={1920} height={1080} fps={30} durationInFrames={200}/>
 <Composition id="V2-Realisation" component={RealisationShot} width={1920} height={1080} fps={30} durationInFrames={246}/>
 </Folder>
 </>;
