/* Deterministic SVG character rig and GSAP acting for the HyperFrames film. */
(function(){
 'use strict';
 const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
 const mix=(a,b,t)=>a+(b-a)*t;
 const smooth=x=>{const t=clamp(x);return t*t*(3-2*t)};
 const pulse=(t,a,b,c)=>smooth((t-a)/(b-a))*(1-smooth((t-b)/(c-b)));
 const pt=a=>a.map(v=>v.toFixed(3)).join(' ');
 function ik(a,b,l1=116,l2=116,sign=-1){const dx=b[0]-a[0],dy=b[1]-a[1],n=Math.max(.001,Math.hypot(dx,dy)),d=Math.min(n,l1+l2-.01),q=(l1*l1-l2*l2+d*d)/(2*d),h=Math.sqrt(Math.max(0,l1*l1-q*q));return [a[0]+q*dx/n-sign*h*dy/n,a[1]+q*dy/n+sign*h*dx/n]}
 function actor(el){
  const part={};el.querySelectorAll('[data-part]').forEach(n=>part[n.dataset.part]=n);
  const seat=+el.dataset.seat;
  return {el,part,initialX:+el.dataset.x,s:{x:+el.dataset.x,y:+el.dataset.y,scale:+el.dataset.scale,seat,walk:0,depthWalk:0,age:0,lean:0,head:0,gaze:12,gy:0,surprise:0,smile:.15,handRX:seat?180:160,handRY:seat?-205:-315,handLX:seat?-90:-102,handLY:seat?-170:-183,lift:0,face:1,stain:0,talk:0},hand:[0,0]};
 }
 function drawActor(a){
  const s=a.s,p=a.part,t=s.age,delta=s.seat*55;
  const breath=Math.sin(t*2.15+a.initialX*.003)*1.2;
  const phase=(s.x-a.initialX)/(s.scale*s.face*140)+(s.depthWalk||0);
  const frac=x=>x-Math.floor(x);
  const stride=side=>{const ph=frac(phase+side*.5),u=clamp((ph-.62)/.38);let x,y;if(ph<.62){x=70-140*ph;y=0}else{x=mix(-16.8,70,smooth(u));y=-Math.sin(Math.PI*u)*43}return [x*s.walk,y*s.walk]};
  const hips=[[-36,-202+delta+breath],[37,-202+delta+breath]];
  const aa=stride(0),bb=stride(1),dir=a.initialX>1000?-1:1;
  const feet=[[mix(-46,32*dir,s.seat)+aa[0],aa[1]],[mix(53,84*dir,s.seat)+bb[0]+s.lift*37,bb[1]-s.lift*47]];
  ['back','front'].forEach((side,i)=>{const k=ik(hips[i],feet[i],102.5,102.5);const knee=[mix(k[0],(i?85:38)*dir,s.seat),mix(k[1],-132,s.seat)];const d=`M${pt(hips[i])}L${pt(knee)}L${pt(feet[i])}`;p[side+'-leg'].setAttribute('d',d);p[side+'-leg-rim'].setAttribute('d',d);p[side+'-shoe'].setAttribute('transform',`translate(${pt(feet[i])})`)});
  const walkArm=Math.sin(phase*Math.PI*2)*31*s.walk;
  const hands=[[s.handLX-walkArm,s.handLY-delta],[s.handRX+walkArm*.6,s.handRY-delta]];
  const shoulders=[[-70,-459],[66,-458]];
  ['back','front'].forEach((side,i)=>{const k=ik(shoulders[i],hands[i],145,130,i===0?-1:1),d=`M${pt(shoulders[i])}L${pt(k)}L${pt(hands[i])}`;['-arm','-arm-rim','-arm-outline'].forEach(n=>p[side+n].setAttribute('d',d));p[side+'-hand'].setAttribute('transform',`translate(${pt(hands[i])})`)});
  p.body.setAttribute('transform',`translate(0 ${delta+breath}) rotate(${s.lean} 0 -202)`);
  p.head.setAttribute('transform',`translate(0 -600) rotate(${s.head})`);
  p.gaze.setAttribute('transform',`translate(${s.gaze*1.65} ${s.gy*.8})`);
  const bl=1-pulse((t+a.initialX*.013)%6.2,5.70,5.79,5.97);
  [p['eye-left'],p['eye-right']].forEach(n=>{n.setAttribute('ry',Math.max(.65,(10+s.surprise*6)*bl));n.setAttribute('rx',7.5+s.surprise*2)});
  p.brows.setAttribute('d',`M-33 ${-35-s.surprise*13}L-15 ${-37-s.surprise*9}M14 ${-37-s.surprise*9}L32 ${-35-s.surprise*13}`);
  const mouthY=29,open=s.surprise*.85+s.talk*(.5+.5*Math.sin(t*14));
  p.mouth.setAttribute('d',open>.43?`M-6 ${mouthY}C-6 ${mouthY-11*open} 7 ${mouthY-11*open} 7 ${mouthY}C7 ${mouthY+17*open} -6 ${mouthY+17*open} -6 ${mouthY}`:`M-11 29Q0 ${31+s.smile*15} 13 28`);
  p.mouth.setAttribute('fill',open>.43?'#fff4dc':'none');
  a.el.setAttribute('transform',`translate(${s.x} ${s.y}) scale(${s.scale*s.face} ${s.scale})`);
  const ang=s.lean*Math.PI/180,h=hands[1],rot=[h[0]*Math.cos(ang)-(h[1]+202)*Math.sin(ang),-202+h[0]*Math.sin(ang)+(h[1]+202)*Math.cos(ang)];
  a.hand=[s.x+s.scale*s.face*rot[0],s.y+s.scale*(rot[1]+delta+breath)];
  p.stain.setAttribute('cx',-12);p.stain.setAttribute('cy',-230+delta);p.stain.setAttribute('rx',44);p.stain.setAttribute('ry',23);p.stain.style.opacity=s.stain;
 }
 window.CartoonRig={create:actor,draw:drawActor};
})();
