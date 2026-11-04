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
  return {el,part,initialX:+el.dataset.x,s:{x:+el.dataset.x,y:+el.dataset.y,scale:+el.dataset.scale,seat,walk:0,age:0,lean:0,head:0,gaze:12,gy:0,surprise:0,smile:.15,handRX:seat?180:160,handRY:seat?-205:-315,handLX:seat?-90:-102,handLY:seat?-170:-183,lift:0,face:1,stain:0,talk:0},hand:[0,0]};
 }
 function drawActor(a){
  const s=a.s,p=a.part,t=s.age,delta=s.seat*55;
  const breath=Math.sin(t*2.15+a.initialX*.003)*1.2;
  const phase=(s.x-a.initialX)/(s.scale*s.face*140);
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
 function scene(root,cfg){
  const tl=gsap.timeline({paused:true});
  const parts={};root.querySelectorAll('[data-part]').forEach(n=>{if(!n.closest('[data-actor]'))parts[n.dataset.part]=n});
  const props={};root.querySelectorAll('[data-prop]').forEach(n=>props[n.dataset.prop]=n);
  const actors={};root.querySelectorAll('[data-actor]').forEach(n=>actors[n.dataset.actor]=actor(n));
  const camera={x:960,y:540,z:1};
  const s={age:0,vision:0,green:0,carX:2600,carY:805,carScale:1.1,carOn:0,danger:0,leaf:0,
   phoneOn:0,phoneX:856,phoneY:690,phoneScale:.6,phoneRot:0,phoneFlat:0,phoneFloor:0,cracks:0,ui:0,held:0,
   cupX:970,cupY:747,cupRot:0,saucerX:830,saucerRot:0,spill:0,trayOn:0,
   rain:0,puddle:0,ticket:0,question:0,apology:0,friendCupX:1245,friendCupY:755,friendCupRot:0};
  const setOpacity=(node,v)=>{if(node)node.style.opacity=String(v)};
  const draw=()=>{
   Object.values(actors).forEach(drawActor);
   parts.camera?.setAttribute('transform',`translate(960 540) scale(${camera.z}) translate(${-camera.x} ${-camera.y})`);
   setOpacity(parts['future-wash'],s.vision*.135);if(parts['vision-tag'])parts['vision-tag'].style.opacity=s.vision;
   setOpacity(parts['lamp-green'],s.green);setOpacity(parts['lamp-red'],1-s.green);
   if(parts['lamp-green-bg'])parts['lamp-green-bg'].setAttribute('fill',s.green>.5?'#3e8065':'#304b42');
   if(parts['lamp-red-bg'])parts['lamp-red-bg'].setAttribute('fill',s.green>.5?'#303b40':'#6d403b');
   if(props.car){props.car.setAttribute('transform',`translate(${s.carX} ${s.carY}) scale(${s.carScale})`);setOpacity(props.car,s.carOn);props.car.querySelectorAll('[data-part="wheel"]').forEach(n=>n.setAttribute('transform',`translate(${n.dataset.wheelX} 34) rotate(${s.carX/58*180/Math.PI})`))}
   if(props.phone){
    let x=s.phoneX,y=s.phoneY;if(s.held&&actors.hero){x=actors.hero.hand[0]+9;y=actors.hero.hand[1]-43}
    const scaleY=s.phoneScale*(1-s.phoneFlat*.82);
    props.phone.setAttribute('transform',`translate(${x} ${y}) rotate(${s.phoneRot}) scale(${s.phoneScale} ${scaleY})`);setOpacity(props.phone,s.phoneOn);
    setOpacity(parts['phone-cracks'],s.cracks);
    props.phone.querySelectorAll('[data-ui]').forEach(n=>n.style.opacity=+n.dataset.ui===Math.round(s.ui)?1:0);
   }
   if(props.cup)props.cup.setAttribute('transform',`translate(${s.cupX} ${s.cupY}) rotate(${s.cupRot})`);
   if(props['friend-cup'])props['friend-cup'].setAttribute('transform',`translate(${s.friendCupX} ${s.friendCupY}) rotate(${s.friendCupRot})`);
   if(props.saucer)props.saucer.setAttribute('transform',`translate(${s.saucerX-830} 0) rotate(${s.saucerRot} 830 790)`);
   if(props.tray){setOpacity(props.tray,s.trayOn);props.tray.setAttribute('transform',`translate(${(actors.waiter?.s.x??-500)+135} 785)`)}
   if(props.spill){setOpacity(props.spill,s.spill);props.spill.setAttribute('transform','translate(741 757)')}
   setOpacity(props.danger,s.danger);setOpacity(props.rain,s.rain);setOpacity(props.puddle,s.puddle);setOpacity(props.ticket,s.ticket);setOpacity(props['question-bubble'],s.question);setOpacity(props['apology-bubble'],s.apology);
   if(props.rain)props.rain.setAttribute('transform',`translate(${-((s.age*265)%235)} ${(s.age*670)%173})`);
   if(props.leaf)props.leaf.setAttribute('transform',`translate(${1730-s.leaf*220} ${380+s.leaf*560}) rotate(${s.leaf*290})`);
   if(parts['tree-crown'])parts['tree-crown'].setAttribute('transform',`rotate(${Math.sin(s.age*1.1)*.35} 0 -150)`);
  };
  const to=(obj,t,v,d=.7,ease='power2.inOut')=>tl.to(obj,{...v,duration:d,ease,onUpdate:draw},Math.max(0,t));
  const step=(obj,t,v)=>tl.set(obj,{...v,onUpdate:draw},Math.max(0,t));
  const hero=actors.hero?.s,friend=actors.friend?.s;
  const pose=(name,t,v,d=.7,ease='power2.inOut')=>{if(actors[name])to(actors[name].s,t,v,d,ease)};
  const cam=(t,x,y,z,d=1.4)=>to(camera,t,{x,y,z},d,'sine.inOut');
  const vision=(t,on,d=.22)=>to(s,t,{vision:on},d,'sine.inOut');
  const n=cfg.kind,du=cfg.duration;
  // Static CSS/attributes are the layout end state. These authored poses establish
  // the meaningful hero frame before the entrance and action curves are added.
  if(['vision','phone','wheel'].includes(n)){
   Object.assign(s,{vision:1,green:1,carOn:1,carX:1840,phoneOn:1,phoneX:838,phoneY:879,phoneScale:.80,phoneFlat:.66,phoneRot:-13,cracks:1,ui:5});
   if(n==='phone'){Object.assign(camera,{x:838,y:879,z:4.5});to(s,0,{carX:1900},du);cam(.2,838,883,4.85,du-.3)}
   else if(n==='wheel'){Object.assign(camera,{x:1640,y:768,z:2.45});Object.assign(s,{carX:1900});to(s,0,{carX:1940},du);cam(0,1660,768,2.5,du)}
   else{to(s,0,{carX:1870},du);cam(.1,980,561,1.045,du-.2)}
  }
  if(n==='street'){Object.assign(s,{held:1,phoneOn:1});cam(.1,960,540,1.02,du-.1);pose('hero',.25,{gaze:18,gy:-10},.65)}
  if(n==='safe'){
   Object.assign(s,{held:1,phoneOn:1});Object.assign(hero,{surprise:.75,head:-5,gaze:-15});
   pose('hero',1.4,{surprise:.12,head:2,gaze:17},2.4);cam(.1,900,563,1.10,4.5);
  }
  if(n==='crossing'){
   Object.assign(s,{held:1,phoneOn:1,carOn:1,carX:-1050});
   to(s,1.35,{green:1},.12);to(s,0,{carX:-360},3.3,'none');to(s,3.3,{carX:-80},1.4,'none');to(s,4.7,{carX:80},.7,'power1.in');to(s,5.4,{carX:1350},1.6,'power1.in');to(s,7.0,{carX:2700},1.5,'none');
   pose('hero',1.6,{lean:4,lift:.85,gaze:19,head:3},1.1);pose('hero',3.1,{gaze:-18,head:-5,surprise:.35,lift:1},.55);pose('hero',4.0,{lift:0,lean:0,surprise:.75},.5);pose('hero',5.6,{gaze:-5},.6);pose('hero',6.2,{gaze:20,head:3},.9);pose('hero',8.6,{smile:.7,surprise:0,head:0},1);
   to(s,8.2,{danger:1},.4);to(s,10.4,{danger:0},.35);
  }
  if(n==='reflection'){
   Object.assign(s,{green:1,held:1,phoneOn:1});Object.assign(hero,{smile:.6,gaze:18});
   cam(0,858,551,1.38,du-1);pose('hero',2,{handRX:150,handRY:-354,gaze:15,gy:13,head:7},1.1);pose('hero',5,{gaze:1,gy:0,head:-2,smile:.9},1.3);pose('hero',8,{handLX:-178,handLY:-300,head:3},1.2);
  }
  if(n==='rules'){
   Object.assign(s,{green:1,held:1,phoneOn:1});Object.assign(hero,{smile:.5});Object.assign(friend,{gaze:-17,handLX:-130,handLY:-285});
   pose('hero',1,{handLX:-180,handLY:-358,gaze:0},1);pose('friend',2,{handRX:145,handRY:-350,head:-4},1.1);pose('hero',6,{gaze:19,handLX:-110,handLY:-215},1.2);vision(8.6,1,.25);to(s,8.6,{leaf:1},3);vision(12.6,0,.3);cam(.4,1030,556,1.04,du-1);
  }
  if(n==='limits'){
   Object.assign(s,{green:1,held:1,phoneOn:1});Object.assign(hero,{gaze:17,head:4});Object.assign(friend,{gaze:-18,smile:.6});
   pose('friend',1,{handLX:-175,handLY:-363,talk:.3},.8);pose('hero',3,{head:-8,gaze:-17,handLX:-140,handLY:-300},.8);pose('hero',6,{gaze:20,head:3},1.2);pose('friend',6.4,{handLX:-92,handLY:-183,talk:0},1.2);pose('hero',9,{head:0,gaze:2,surprise:.3},.7);vision(10.1,1,.18);vision(10.9,0,.25);vision(12.7,1,.18);vision(13.4,0,.25);pose('hero',14,{surprise:0,smile:.5},1.2);cam(0,1080,557,1.05,du-.2);
  }
  if(n==='decision'){
   Object.assign(s,{green:1,held:1,phoneOn:1});Object.assign(hero,{head:3,gaze:-12,smile:.45});
   pose('hero',1.0,{handLX:-160,handLY:-390,head:-3},1.1);pose('hero',5.3,{handLX:-115,handLY:-280,gaze:18,smile:.9},1.0);pose('hero',9.4,{gaze:1,head:0,handLX:-130,handLY:-183},1.5);cam(.3,880,558,1.18,du-.6);
  }
  if(n==='cafe'){
   Object.assign(s,{cupX:830,cupY:755});
   Object.assign(hero,{handRX:170,handRY:-205,gaze:16,smile:.55});Object.assign(friend,{gaze:-15,smile:.55,handLX:-100,handLY:-205});
   Object.assign(actors.waiter.s,{handRX:125,handRY:-236,handLX:-90,handLY:-190});
   cam(.2,980,594,1.08,3);vision(4.15,1,.22);to(s,4.5,{cupX:740,cupY:782,cupRot:-62,spill:1},1.0,'power1.in');pose('hero',4.6,{surprise:.7,stain:1,handRX:132,handRY:-180,head:-5},.7);vision(6.5,0,.25);step(s,6.62,{cupX:830,cupY:755,cupRot:0,spill:0});step(hero,6.62,{stain:0});pose('hero',6.65,{surprise:.1,handRX:170,handRY:-205,head:3},.4);
   pose('hero',7.0,{handRX:154,handRY:-226,gaze:18,gy:10},.6);to(s,7.6,{cupX:915,cupY:725},1.25);pose('hero',7.6,{handRX:243,handRY:-258},1.25);pose('hero',9.05,{handRX:145,handRY:-180,gaze:0,gy:0},.8);
   to(s,10.6,{trayOn:1},.2);pose('waiter',10.6,{walk:1},.25);pose('waiter',10.6,{x:680},4.0,'none');pose('waiter',14.6,{x:2130},5.9,'none');pose('waiter',20.2,{walk:0},.25);to(s,15.08,{saucerX:845,saucerRot:3},.12);to(s,15.20,{saucerRot:-2},.16);to(s,15.36,{saucerRot:0},.26);pose('hero',14.8,{gaze:18,head:5},.6);pose('hero',17.4,{gaze:0,gy:0,smile:1,handRX:170,handRY:-205},1.2);cam(9.0,1038,682,1.18,4.2);cam(18,1000,588,1.08,3.8);
  }
  if(n==='rain'){
   Object.assign(hero,{gaze:16,smile:.55,handRX:120,handRY:-240});Object.assign(actors.passer.s,{face:-1,handRX:90,handRY:-370});
   pose('hero',.8,{x:830,walk:.7,gaze:20},2.2,'none');pose('hero',2.9,{walk:0,surprise:.35,head:-5},.5);vision(3.1,1,.2);to(s,3.15,{rain:1,puddle:.8},.8);vision(8.9,0,.3);to(s,8.9,{rain:0,puddle:0},.2);pose('hero',9.3,{x:710,walk:.6},1.6,'none');pose('hero',10.9,{walk:0,gaze:17,head:0,smile:.9,surprise:0},.4);to(s,11.8,{rain:1,puddle:1},1.3);pose('passer',11.8,{handRX:70,handRY:-580,handLX:-65,handLY:-575,head:-6,lean:-4},.8);pose('passer',12,{x:1390,walk:1},6.0,'none');pose('passer',18,{walk:0},.5);cam(.2,1050,557,1.035,du-.4);
  }
  if(n==='money'||n==='horizon'){
   Object.assign(hero,{handRX:197,handRY:-220,handLX:-84,handLY:-190,gaze:19,gy:10,smile:.6});
   if(n==='money'){pose('hero',2,{head:-7,handLX:-162,handLY:-390,smile:.9},1);pose('hero',5,{head:2,handLX:-85,handLY:-190},1);cam(.3,1045,600,1.10,du-1);vision(9.2,1,.25);vision(12.0,0,.3)}
   else{Object.assign(s,{ticket:1});pose('hero',1,{head:-5,gaze:20,gy:15,smile:.1},.8);pose('hero',5,{handLX:-175,handLY:-335,head:5},1.2);vision(10.5,1,.22);vision(11.4,0,.3);vision(13.1,1,.22);vision(14.0,0,.3);pose('hero',15.5,{handLX:-94,handLY:-190,head:0,smile:.5},1.1);cam(0,1000,590,1.13,du-.3)}
  }
  if(n==='messages'){
   Object.assign(hero,{handRX:188,handRY:-240,gaze:20,gy:16,head:6,smile:.25});Object.assign(s,{phoneOn:1});
   cam(.2,856,690,3.8,5.0);vision(6.6,1,.22);step(s,6.75,{ui:1});pose('hero',7,{surprise:.25,smile:0},.5);vision(12.8,0,.25);step(s,12.95,{ui:2});pose('hero',13,{handRX:188,handRY:-240,smile:.3},.5);vision(17.3,1,.22);step(s,17.45,{ui:3});vision(19.8,0,.25);step(s,19.95,{ui:2});pose('hero',20.4,{handRX:200,handRY:-250},.18);step(s,21.08,{ui:4});pose('hero',21.3,{handRX:188,handRY:-240,smile:.9},.4);
  }
  if(n==='repeat'){
   Object.assign(s,{phoneOn:1,ui:4});Object.assign(hero,{gaze:18,gy:14,head:6,smile:.45,handRX:188,handRY:-240});Object.assign(friend,{gaze:-17,smile:.5,handLX:-145,handLY:-245});
   for(const t of [1.4,4.8,8.0]){vision(t,1,.2);vision(t+.6,0,.25);pose('hero',t,{head:-4,gaze:0},.25);pose('hero',t+.8,{head:6,gaze:18},.4)}
   pose('friend',3,{handLX:-180,handLY:-325,talk:.35},.8);pose('friend',6,{handLX:-120,handLY:-240,head:-5,smile:.1},1.2);cam(0,1050,580,1.08,du-.2);
  }
  if(n==='conversation'){
   Object.assign(s,{phoneOn:1,ui:4});Object.assign(hero,{handRX:188,handRY:-240,gaze:19,gy:14,head:7,smile:.3});Object.assign(friend,{gaze:-16,handLX:-160,handLY:-280,talk:.4,smile:.35});
   pose('friend',1.5,{handLX:-190,handLY:-340,head:-3},1.1);pose('friend',4.0,{handLX:-115,handLY:-215,head:3},1.4);pose('hero',5.4,{gaze:0,gy:0,surprise:.1},.4);vision(6.0,1,.18);vision(6.65,0,.2);pose('hero',7.0,{gaze:18,gy:13},.35);pose('friend',8.0,{handLX:-180,handLY:-350,smile:0,head:-7},1.0);pose('friend',11.8,{talk:.55,head:2},.5);to(s,15.35,{question:1},.25);pose('hero',14.0,{gaze:20,gy:-5,head:0,surprise:.35},.6);to(s,17,{question:0},.3);pose('friend',17.3,{talk:0,handLX:-110,handLY:-210,head:-5},.8);cam(.1,1030,575,1.13,du-.3);
  }
  if(n==='departure'){
   Object.assign(s,{phoneOn:1,ui:4,vision:1});Object.assign(hero,{gaze:18,gy:12,head:6,handRX:188,handRY:-240});Object.assign(friend,{gaze:-13,smile:0,head:-6});
   pose('friend',3.0,{lean:7,handLX:-80,handLY:-155},.4);pose('friend',3.4,{seat:0,lean:2,handLX:-105,handLY:-183,handRX:115,handRY:-183},1.0);pose('friend',8.3,{gaze:15,head:1,walk:1},.35);pose('friend',8.65,{x:2030},4.55,'none');pose('friend',13.2,{walk:0},.2);pose('hero',5,{gaze:20,gy:0,head:0,surprise:.4},1);cam(.3,1070,574,1.06,du-.5);
  }
  if(n==='restore'){
   Object.assign(s,{phoneOn:1,ui:4});Object.assign(hero,{handRX:188,handRY:-240,gaze:18,gy:12,head:6,smile:.1});Object.assign(friend,{gaze:-17,head:-5,smile:.1});
   to(s,2.2,{phoneX:844,phoneY:770,phoneFlat:1,phoneRot:-12},1.2);pose('hero',2.2,{handRX:168,handRY:-194,head:0,gy:0},1.2);pose('hero',3.55,{handRX:197,handRY:-265,gaze:20,head:2,smile:.65},1);pose('hero',6.0,{talk:.45,handRX:215,handRY:-295},.6);to(s,6.5,{apology:1},.3);pose('friend',7,{head:3,smile:.7},.8);pose('hero',9.0,{talk:0,handRX:170,handRY:-205,smile:1},1.1);to(s,10.4,{apology:0},.4);pose('friend',10.5,{head:-2,smile:1,handLX:-140,handLY:-270,talk:.3},1.2);cam(.2,990,574,1.075,du-.4);
  }
  if(n==='choice'){
   Object.assign(s,{phoneOn:1,phoneX:844,phoneY:770,phoneFlat:1,phoneRot:-12,ui:4});Object.assign(hero,{gaze:17,smile:1,handRX:175,handRY:-205});Object.assign(friend,{gaze:-16,smile:1,handLX:-100,handLY:-205});
   pose('friend',1.0,{talk:.25,handLX:-180,handLY:-295},1);pose('friend',3.3,{talk:0,handLX:-100,handLY:-205},.8);pose('hero',4.3,{head:-4,handRX:205,handRY:-270},.8);pose('hero',5.3,{head:1,handRX:175,handRY:-205},1.1);pose('friend',6.7,{handLX:-54,handLY:-226},.3);to(s,7.0,{friendCupX:1355,friendCupY:505,friendCupRot:-12},1.8);pose('friend',7,{handLX:61,handLY:-499,head:3,gaze:-4},1.8);to(s,10.0,{friendCupX:1245,friendCupY:755,friendCupRot:0},1.7);pose('friend',10,{handLX:-54,handLY:-226,gaze:-16,head:0},1.7);cam(0,995,570,1.10,du-.2);
  }
  if(n==='reprise'){
   Object.assign(s,{held:1,phoneOn:1,carOn:1,carX:-350,green:0});Object.assign(hero,{gaze:19,head:2,smile:.5});
   to(s,0,{carX:-160},3.0,'power2.out');pose('hero',.8,{surprise:.2,head:-4},.5);vision(1.4,1,.2);vision(2.3,0,.25);pose('hero',3.2,{surprise:0,gaze:0,head:0,handLX:-165,handLY:-335},1);pose('hero',6.4,{handLX:-108,handLY:-205,gaze:16,smile:.8},1);cam(.2,875,548,1.17,du-.4);
  }
  if(n==='finish'){
   Object.assign(s,{phoneOn:1,phoneX:844,phoneY:770,phoneFlat:1,phoneRot:-12,ui:4});Object.assign(hero,{gaze:17,smile:.9,handRX:170,handRY:-205});Object.assign(friend,{gaze:-17,smile:.8});
   pose('hero',1.0,{gaze:0,head:-2,handLX:-155,handLY:-310},1.3);pose('friend',3.0,{gaze:0,head:3},1.1);pose('hero',5.6,{handLX:-90,handLY:-190,head:2},1.2);pose('hero',9.0,{handRX:230,handRY:-300,gaze:0},1.1);pose('hero',12.7,{handRX:170,handRY:-205},1.2);pose('friend',16,{handRX:175,handRY:-370,head:-2},1.2);pose('hero',18.5,{handLX:-180,handLY:-350,head:-4},.8);pose('hero',19.3,{head:2,handLX:-165,handLY:-380},.6);pose('friend',19.5,{handRX:158,handRY:-402,head:2},.7);cam(.1,970,556,1.12,du-.3);
  }
  // Meaningful continuous rig motion: breath, blink, gaze and walk contacts are
  // pure functions of this finite local timeline, never real time or randomness.
  to(s,0,{age:du},du,'none');Object.values(actors).forEach(a=>to(a.s,0,{age:du},du,'none'));
  const fade=['vision','phone','wheel'].includes(n)?.18:.34;
  tl.from(root.querySelector('[data-part="background"]'),{opacity:n==='street'?.98:.25,duration:fade,ease:'sine.inOut'},0);
  root.querySelectorAll('[data-actor]').forEach((el,i)=>tl.from(el,{opacity:n==='street'?.98:.12,duration:fade+.05,ease:i%2?'power2.out':'power1.out'},0));
  tl.from(root.querySelector('.scene-content'),{opacity:n==='street'?.98:.15,duration:fade,ease:'power3.out'},0);
  draw();return tl;
 }
 window.WhatIfFilm={scene};
})();
