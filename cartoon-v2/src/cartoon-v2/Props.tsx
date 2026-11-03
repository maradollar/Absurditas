import React from 'react';
import {P} from './math';
export const FilmDefs=()=> <defs>
 <linearGradient id="v2-sky" x2="0" y2="1"><stop stopColor="#d8e4e9"/><stop offset="1" stopColor="#f4e9d1"/></linearGradient>
 <linearGradient id="v2-road" x2=".15" y2="1"><stop stopColor="#969b9c"/><stop offset="1" stopColor="#7d8589"/></linearGradient>
 <linearGradient id="v2-hood" x2="1" y2=".25"><stop stopColor="#eb8d00"/><stop offset=".4" stopColor="#ffa600"/><stop offset="1" stopColor="#ffb21b"/></linearGradient>
 <linearGradient id="v2-car" x2=".2" y2="1"><stop stopColor="#cf8771"/><stop offset=".5" stopColor="#ba6152"/><stop offset="1" stopColor="#8d4947"/></linearGradient>
 <linearGradient id="v2-glass" x2=".5" y2="1"><stop stopColor="#b7d6e0"/><stop offset="1" stopColor="#7798ad"/></linearGradient>
 <radialGradient id="v2-vignette"><stop offset=".5" stopColor="#2a1f23" stopOpacity="0"/><stop offset="1" stopColor="#2a1f23" stopOpacity=".2"/></radialGradient>
 <filter id="v2-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.5"/></filter>
 <filter id="v2-shadow" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>
 <filter id="v2-future"><feColorMatrix type="matrix" values="0.92 0.01 0.01 0 0 0.01 0.95 0.01 0 0 0.01 0.02 1 0 0.01 0 0 0 1 0"/></filter>
 <pattern id="v2-paper" width="91" height="89" patternUnits="userSpaceOnUse"><circle cx="3" cy="6" r=".6" fill="#3c2f23" opacity=".045"/><circle cx="61" cy="48" r=".6" fill="#fff" opacity=".08"/></pattern>
 </defs>;
export const Phone:React.FC<{broken?:boolean}>=({broken=false})=><g>
 <rect x="-25" y="-48" width="51" height="96" rx="8" fill="#292a30" stroke={P.ink} strokeWidth="3"/>
 <path d="M-23-39V35Q-23 44-15 45H18" stroke="#eed8b4" strokeWidth="3" fill="none"/>
 <rect x="-19" y="-39" width="39" height="74" rx="4" fill="url(#v2-glass)"/>
 <path d="M-5-44H7" stroke="#8b8b86" strokeWidth="3" strokeLinecap="round"/>
 <path d="M-15-32L12-7M-16-21L1-4" stroke="#e6eff0" strokeWidth="4" opacity=".4"/>
 {broken&&<g fill="none" stroke="#f6f4e8" strokeWidth="1.8" strokeLinejoin="round"><path d="M-3-5L-16-25L-12-39M-3-5L16-29M-3-5L20 4M-3-5L-10 15L-19 29M-10 15L9 35M-3-5L-19 0M-10 15L13 17L20 4"/><path d="M-15-23L0-22L16-29M-19 0L-11 6L-10 15" opacity=".7"/></g>}
 <circle cy="41" r="2" fill="#96918a"/>
 </g>;
export const PedestrianLamp:React.FC<{x:number;y:number;green:boolean;scale?:number}>=({x,y,green,scale=1})=><g transform={`translate(${x} ${y}) scale(${scale})`}>
 <ellipse cy="5" rx="41" ry="7" fill="#615b54" opacity=".2"/>
 <path d="M0 0V-270" stroke="#51565b" strokeWidth="13"/>
 <path d="M-3-8V-268" stroke="#a5a8a1" strokeWidth="3" opacity=".6"/>
 <rect x="-33" y="-318" width="66" height="132" rx="13" fill="#353b42" stroke="#22262d" strokeWidth="3"/>
 <rect x="-25" y="-310" width="50" height="54" rx="6" fill={green?'#2b3136':'#773e3b'}/>
 <rect x="-25" y="-248" width="50" height="54" rx="6" fill={green?'#3e8065':'#2b3136'}/>
 <g fill={green?'#4c4542':'#ff7967'} transform="translate(0 -286)"><circle cy="-12" r="5"/><path d="M-7-3H7V9H3V24H-2V9H-7Z"/></g>
 <g fill={green?'#abedaf':'#42524b'} transform="translate(0 -225)"><circle cy="-15" r="5"/><path d="M-1-7L7-2L16 3L13 8L3 3L-1 11L9 23L4 27L-6 14L-13 26L-18 22L-9 4L-15 9L-19 4Z"/></g>
 </g>;
export const VehicleLamp:React.FC<{x:number;y:number}>=({x,y})=><g transform={`translate(${x} ${y})`}>
 <path d="M0 0V-310" stroke="#56575b" strokeWidth="12"/><path d="M-3-8V-300" stroke="#b9b8ac" strokeWidth="3"/>
 <rect x="-34" y="-371" width="68" height="158" rx="16" fill="#34383e" stroke="#24292d" strokeWidth="3"/>
 <circle cy="-341" r="19" fill="#de6c57"/><circle cy="-292" r="18" fill="#49453f"/><circle cy="-243" r="18" fill="#384b44"/>
 <circle cx="-5" cy="-346" r="7" fill="#f7a28a" opacity=".65"/>
 </g>;
export const Car:React.FC<{x:number;y?:number;s?:number;wheelAngle:number;braking?:boolean}>=({x,y=782,s=1.3,wheelAngle,braking=false})=><g transform={`translate(${x} ${y}) scale(${s})`}>
 <ellipse cy="46" rx="331" ry="22" fill="#303139" opacity=".21" filter="url(#v2-shadow)"/>
 <path d="M-322 0L-330-73Q-328-95-292-107L-211-129L-129-235Q-115-252-78-253H72Q99-251 122-226L206-129L287-111Q325-104 334-68L338-7L316 17H-299Z" fill="url(#v2-car)" stroke="#4b3535" strokeWidth="4" strokeLinejoin="round"/>
 <path d="M-186-133L-116-224Q-109-234-85-234H-30V-135ZM-13-234H66Q80-233 99-211L163-135H-13Z" fill="#5e737e" stroke="#4a4c54" strokeWidth="4"/>
 <path d="M-168-143L-105-219H-78M4-220H60L110-164" stroke="#b6c5c4" strokeWidth="8" strokeLinecap="round" opacity=".5" fill="none"/>
 <path d="M-312-84Q-69-107 315-78" stroke="#e3a58d" strokeWidth="6" opacity=".6" fill="none"/>
 <path d="M-22-131V-7M-177-129L-196-10M181-127L210-10" stroke="#8e4c47" strokeWidth="3" fill="none"/>
 <path d="M-115-112h31M58-112h31" stroke="#e2b4a0" strokeWidth="5" strokeLinecap="round"/>
 <path d="M-16-153l-12 19h-19" stroke="#8e4f48" strokeWidth="12" strokeLinecap="round" fill="none"/>
 <path d="M307-92l13 8v25h-33Z" fill="#f8dfaa"/><path d="M-323-85h17v30h-19Z" fill={braking?'#ff5d45':'#a7433f'}/>
 <path d="M282-25h39M-313-21h29" stroke="#c0bcb0" strokeWidth="7" strokeLinecap="round"/>
 {[-215,207].map((wx,i)=><g key={i} transform={`translate(${wx} 0)`}>
 <path d="M-64 11Q-62-67 0-68Q62-66 65 10" fill="#4a3335"/>
 <circle r="52" fill="#24252a" stroke="#181b21" strokeWidth="4"/>
 <circle r="34" fill="#929b9e" stroke="#4d5b63" strokeWidth="4"/>
 <g transform={`rotate(${wheelAngle})`} stroke="#59656e" strokeWidth="9" strokeLinecap="round"><path d="M-24 0H24M0-24V24M-17-17L17 17M17-17L-17 17"/></g>
 <circle r="11" fill="#c7c5b8"/>
 <path d="M-42-16A45 45 0 0 1 30-34" stroke="#74777b" strokeWidth="3" fill="none" opacity=".7"/>
 </g>)}
 </g>;
