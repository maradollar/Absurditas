import React from 'react';
import {AbsoluteFill, staticFile, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {CartoonFilm} from '../cartoon-v2/CartoonFilm';
import {EmphasisLayer} from './Emphasis';

export const CartoonFilmV3:React.FC=()=>{const {fps}=useVideoConfig();return <AbsoluteFill>
 <CartoonFilm/>
 <EmphasisLayer/>
 <Audio name="V3 · Text-, Fokus- und Grafikakzente" src={staticFile('cartoon-v2/accent-v3.wav')} premountFor={fps}/>
 </AbsoluteFill>};
