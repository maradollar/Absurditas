/* All acting and object motion is seekable, deterministic GSAP state. */
window.DynamicScene=function(root,cfg){
 'use strict';
 const tl=gsap.timeline({paused:true}),du=cfg.duration,a=cfg.action,w=cfg.world;
 const one=n=>root.querySelector('[data-anim="'+n+'"]'),prop=n=>root.querySelector('[data-prop="'+n+'"]');
 const rig={};root.querySelectorAll('[data-actor]').forEach(el=>rig[el.dataset.actor]=CartoonRig.create(el));
 const h=rig.hero?.s,f=rig.friend?.s,c=rig.colleague?.s;
 const cam={x:cfg.camera[0],y:cfg.camera[1],z:cfg.camera[2]};
 const v={t:0,vanX:-1500,trainX:0,door:0,cupX:830,cupY:755,cupR:0,spill:0,ball:0,var:0,score:0,phone:0,connected:0,tilt:0,cyclist:0,phoneHeld:1};
 const C=one('camera'),tr=one('train'),dl=one('door-left'),dr=one('door-right'),car=one('van'),cp=prop('cup');
 let ownArm;
 if(cfg.future&&rig.hero){
  rig.hero.el.style.opacity=0;
  ownArm=document.createElementNS('http://www.w3.org/2000/svg','g');
  ownArm.innerHTML='<path fill="none" stroke="#fff4dc" stroke-width="63" stroke-linejoin="round"/><path fill="none" stroke="#17151d" stroke-width="58" stroke-linejoin="round"/><path fill="none" stroke="#ffa308" stroke-width="49" stroke-linejoin="round"/><circle r="23" fill="#17151d"/>';
  C.appendChild(ownArm);
 }
 const draw=()=>{
  if(rig['hero-inside'])Object.assign(rig['hero-inside'].s,rig.hero.s);
  Object.values(rig).forEach(q=>{q.s.age=v.t+cfg.start;CartoonRig.draw(q)});
  if(rig['hero-inside']){
   rig.hero.el.style.opacity=v.t<du*.38?1:0;rig['hero-inside'].el.style.opacity=v.t<du*.38?0:1;
  }
  if(ownArm){const z=rig.hero.hand;ownArm.querySelectorAll('path').forEach(n=>n.setAttribute('d',`M760 1250L730 900L${z[0]} ${z[1]}`));ownArm.querySelector('circle').setAttribute('cx',z[0]);ownArm.querySelector('circle').setAttribute('cy',z[1]);}
  if(C)C.setAttribute('transform',`translate(960 540) scale(${cam.z}) translate(${-cam.x} ${-cam.y})`);
  if(car){car.setAttribute('transform',`translate(${v.vanX} 805)`);car.querySelectorAll('[data-anim="wheel"]').forEach(n=>n.setAttribute('transform',`translate(${n.dataset.wheelX} 29) rotate(${v.vanX/57*180/Math.PI})`))}
  if(tr)tr.setAttribute('transform',`translate(${v.trainX} 0)`);
  if(dl)dl.setAttribute('transform',`translate(${1027-v.door*144} 402)`);
  if(dr)dr.setAttribute('transform',`translate(${1172+v.door*144} 402)`);
  if(cp)cp.setAttribute('transform',`translate(${v.cupX} ${v.cupY}) rotate(${v.cupR})`);
  if(one('coffee-spill'))one('coffee-spill').style.opacity=v.spill;
  if(one('ball')){
   const x=1100+v.ball*333,y=536-v.ball*28-Math.sin(v.ball*Math.PI)*58;
   one('ball').setAttribute('transform',`translate(${x} ${y}) rotate(${v.ball*600})`);
  }
  if(one('var'))one('var').style.opacity=v.var;
  if(one('score'))one('score').textContent=v.score>.5?'1 : 0':'0 : 0';
  if(one('connected'))one('connected').style.opacity=v.connected;
  if(one('wall-time')&&w==='dinner')one('wall-time').textContent=(cfg.future||cfg.start+v.t>=341)?'19:43':'19:42';
  if(one('table-phone'))one('table-phone').setAttribute('transform',`translate(${870+Math.sin(v.t*37)*v.phone*2.7} 770) rotate(-10) scale(1 .32)`);
  if(one('cyclist'))one('cyclist').setAttribute('transform',`translate(${1560+v.cyclist*30} ${485+v.cyclist*215}) scale(${.7+v.cyclist*.3})`);
  if(prop('phone')&&rig.hero){const z=rig.hero.hand;prop('phone').style.opacity=v.phoneHeld;prop('phone').setAttribute('transform',`translate(${z[0]+9} ${z[1]-32}) scale(.55)`);prop('phone').querySelectorAll('[data-ui]').forEach(n=>n.style.opacity=n.dataset.ui==='5'?1:0)}
 };
 const to=(o,t,vars,d=.6,e='power2.inOut')=>tl.to(o,{...vars,duration:Math.max(.06,d),ease:e,onUpdate:draw},Math.max(0,t));
 const pose=(who,t,vars,d=.6,e='power2.inOut')=>rig[who]&&to(rig[who].s,t,vars,d,e);
 const pct=(p,vars,d=.5)=>to(v,du*p,vars,Math.min(d,du*(1-p)));
 const green=['ground','broken','brake','green','pass','driver','relief','question','moment','perspective','watchfuture','path','choose','empty','single'].includes(a);
 root.querySelectorAll('[data-part="lamp-green"]').forEach(n=>n.style.opacity=green?1:0);
 root.querySelectorAll('[data-part="lamp-red"]').forEach(n=>n.style.opacity=green?0:1);
 root.querySelectorAll('[data-part="lamp-green-bg"]').forEach(n=>n.setAttribute('fill',green?'#3e8065':'#304b42'));
 root.querySelectorAll('[data-part="lamp-red-bg"]').forEach(n=>n.setAttribute('fill',green?'#303b40':'#6d403b'));
 if(h)Object.assign(h,{gaze:5,smile:.25,handRX:120,handRY:-185,handLX:-99,handLY:-183});
 if(f)Object.assign(f,{gaze:-9,smile:.2,handRX:106,handRY:-190,handLX:-96,handLY:-185});
 if(c)Object.assign(c,{gaze:-12,handRX:123,handRY:-280});
 if(a==='ground'){to(cam,.1,{x:cam.x+22,y:cam.y-7},du-.1,'sine.inOut')}
 if(a==='broken'){to(cam,.1,{z:cam.z+.18},du-.1,'sine.inOut')}
 if(a==='brake'){v.vanX=1650;to(v,.1,{vanX:1720},du-.2,'power3.out')}
 if(['return','realize'].includes(a)){Object.assign(h,{surprise:.9,smile:-.1,gaze:-12,head:-5});pose('hero',.35,{surprise:.35,head:1,gaze:17},du*.65)}
 if(['watch','watchfuture'].includes(a)){to(cam,.15,{x:cam.x+12,z:cam.z+.06},du-.2,'sine.inOut')}
 if(a==='green'){Object.assign(h,{gaze:17,head:4,surprise:.2});pose('hero',.5,{lift:.35,lean:3},.5);pose('hero',1.4,{lift:0,lean:-2,gaze:-14},.5)}
 if(a==='pass'){v.vanX=-300;to(v,0,{vanX:900},du,'none');pose('hero',.2,{surprise:.7,gaze:-14},.5);pose('hero',du*.45,{gaze:18,head:5},du*.5)}
 if(a==='driver'){v.vanX=900;to(v,0,{vanX:2010},du,'none');to(cam,0,{x:2160},du,'none')}
 if(['relief','question','saved'].includes(a)){Object.assign(h,{smile:.65,surprise:.18});pose('hero',.35,{handRX:135,handRY:-327,head:5},.8);pose('hero',du*.6,{handRX:100,handRY:-210,head:0},.8)}
 if(a==='confident'){Object.assign(h,{smile:.8,gaze:10});pose('hero',.4,{handRX:174,handRY:-320,head:-3},.9);pose('hero',du*.58,{handRX:90,handRY:-260},1)}
 if(['rule','noreset'].includes(a)){pose('hero',.3,{handRX:150,handRY:-360,head:-5},.65);pose('hero',du*.6,{head:3,handRX:180,handRY:-280},.7)}
 if(a==='path'){pose('hero',.25,{lift:.7,gaze:18,lean:3},.8)}
 if(a==='choose'){Object.assign(h,{lift:.3});pose('hero',.3,{lift:0,x:783,lean:-4},.65);pose('hero',1.4,{lean:0,smile:.5},.8)}
 if(a==='establish'){Object.assign(h,{gaze:13,handRX:160,handRY:-227});pose('hero',.4,{head:4,gy:12},.8)}
 if(a==='spill'){
  Object.assign(h,{handRX:160,handRY:-227});pose('hero',du*.13,{handRX:210,handRY:-211,head:6},du*.3);
  to(v,du*.20,{cupR:52,cupX:857,cupY:757},du*.32,'power2.in');pct(.43,{spill:1},.35);
 }
 if(a==='sleeve'){Object.assign(h,{handRX:154,handRY:-227,gaze:19,gy:13});pose('hero',.4,{handRX:173,handRY:-227},du*.65)}
 if(a==='move'){
  Object.assign(h,{handRX:154,handRY:-227,gaze:17,gy:12});
  to(v,.36,{cupX:740},Math.min(1.25,du-.5),'power2.inOut');pose('hero',.36,{handRX:60,handRY:-227},Math.min(1.25,du-.5));
 }
 if(a==='brush'){
  v.cupX=740;Object.assign(h,{handRX:60,handRY:-227,gaze:19,gy:15});pose('hero',.4,{handRX:200,handRY:-220},.85);pose('hero',1.65,{handRX:155,handRY:-235},.6);
 }
 if(a==='dry'){v.cupX=740;Object.assign(h,{smile:.8});pose('hero',.4,{handRX:195,handRY:-227},.65)}
 if(a==='missed'){to(v,du*.45,{trainX:-160},du*.5,'power1.in')}
 if(a==='run'){v.door=1;Object.assign(h,{x:420,walk:1,lean:7,handRX:105,handRY:-270});pose('hero',0,{x:960},du-.1,'none')}
 if(a==='board'){
  [rig.hero,rig['hero-inside']].forEach(q=>{q.part.gaze.style.opacity=0;q.el.querySelectorAll('[data-part="drawstrings"]').forEach(n=>n.style.opacity=0)});
  v.door=1;Object.assign(h,{x:960,walk:.75,lean:5,handRX:120,handRY:-270});
  pose('hero',.08,{x:1170},du*.28,'none');pose('hero',du*.39,{y:811,scale:.55,lean:0,depthWalk:1.3},du*.42);pose('hero',du*.84,{walk:0,handRX:70,handRY:-220},du*.14);
 }
 if(a==='depart'){v.door=0;to(v,.5,{trainX:-2700},du-.6,'power1.in')}
 if(a==='boss'){pose('colleague',.25,{handRX:150,handRY:-340,talk:.9},.6);pose('hero',.2,{gaze:20,head:5},.6)}
 if(a==='search'){Object.assign(h,{surprise:.4,gaze:20});if(one('answer'))one('answer').style.opacity=0}
 if(a==='answer'){pose('hero',.18,{handRX:260,handRY:-221,gaze:15},.55)}
 if(['joke','jokereprise'].includes(a)){pose('colleague',.3,{talk:.8,handRX:170,handRY:-360,head:5},.7);pose('hero',.8,{smile:.9,head:-5,talk:.4},.6)}
 if(a==='laugh'){Object.assign(h,{smile:.9,talk:.4,gaze:20});pose('hero',du*.45,{smile:.1,talk:0,head:-3},.6)}
 if(['money','chart','rise','buy','profit','repeat','fees','net','lotto','horizon','overconfident','information'].includes(a)){
  Object.assign(h,{gaze:17,handRX:251,handRY:-225,smile:a==='fees'?.05:.45});
  if(a==='money')pose('hero',.35,{handRX:155,handRY:-350,head:3},.75);
  if(a==='repeat')pose('hero',.15,{handRX:220,handRY:-230,head:-4},.55);
  if(['fees','net','information'].includes(a))pose('hero',.3,{surprise:.35,smile:-.2,head:6},.7);
  if(a==='overconfident')pose('hero',.3,{smile:.95,head:-5,handRX:160,handRY:-340},.8);
  const graph=one('graph');if(graph&&['chart','rise'].includes(a)){
   const n=graph.getTotalLength();graph.style.strokeDasharray=n;tl.fromTo(graph,{strokeDashoffset:n},{strokeDashoffset:0,duration:Math.min(2,du-.2),ease:'power1.inOut'},.15);
  }
  if(a==='fees')root.querySelectorAll('[data-anim="cost-row"]').forEach((n,i)=>tl.from(n,{opacity:0,x:14,duration:.3,ease:'power2.out'},.25+i*.45));
 }
 if(['goalvision','goal'].includes(a)){to(v,.35,{ball:1},Math.min(1.1,du*.45),'power2.in');pct(.63,{score:1},.08)}
 if(a==='football'){pose('hero',.3,{smile:.6,gaze:18,handRX:150,handRY:-350},.6)}
 if(w==='living'&&['football','limited'].includes(a)&&rig.hero)rig.hero.part.gaze.style.opacity=0;
 if(a==='var'){v.score=1;v.ball=1;pct(.05,{var:1},.24)}
 if(a==='offside'){v.ball=1;v.score=0;v.var=0;root.querySelectorAll('[data-anim="player"]').forEach((n,i)=>tl.to(n,{x:i%2?'+=16':'-=9',duration:du*.8,ease:'sine.inOut'},.15))}
 if(a==='reaction'){Object.assign(h,{surprise:.8,smile:-.4,gaze:18});pose('hero',.3,{handRX:150,handRY:-420,head:-6},.6)}
 if(a==='limited'){Object.assign(h,{smile:-.2,surprise:.3});v.ball=1}
 if(a==='stop'){Object.assign(h,{lift:.75,lean:5});pose('hero',.2,{lift:0,lean:-4,head:-5},.6)}
 if(a==='side'){to(v,.3,{cyclist:1},Math.min(2,du-.35),'sine.inOut')}
 if(a==='pocket'){Object.assign(h,{handRX:135,handRY:-335});pose('hero',.2,{handRX:30,handRY:-190,head:4},.8);to(v,.8,{phoneHeld:0},.18);pose('hero',1.12,{handRX:110,handRY:-185},.6)}
 if(a==='look'){Object.assign(h,{gaze:-15,head:-5});pose('hero',du*.4,{gaze:17,head:5},.8);pose('hero',du*.75,{gaze:0,head:0},.5)}
 if(['arrival','friend','job','thinking','hurt','tryagain','distracted','talk','away','question','shock','distance','gift','reactions','friendcall'].includes(a)&&w==='cafe'){
  Object.assign(h||{},{gaze:15,handRX:150,handRY:-225});if(f)Object.assign(f,{gaze:-11,smile:.04});
  if(['job','hurt'].includes(a)){Object.assign(f,{head:7,smile:-.35,gy:10});pose('friend',.3,{talk:.55,handLX:-135,handLY:-300},.8)}
  if(a==='thinking'){Object.assign(h,{head:-5,gaze:0,handRX:104,handRY:-505,smile:.05});pose('hero',.3,{head:5,surprise:.25},du*.7)}
  if(a==='tryagain'){Object.assign(f,{head:-5,smile:-.25});pose('friend',.3,{head:5,handRX:135,handRY:-300,talk:.4},du*.6)}
  if(['distracted','talk','away','question'].includes(a)){
   if(h)Object.assign(h,{gaze:19,head:5,smile:.1});if(f)Object.assign(f,{talk:.7,handLX:-125,handLY:-280});
   if(a==='distracted')pose('hero',.3,{head:-4},du*.35);
   if(a==='away')pose('hero',.3,{gaze:-16,head:-7,gy:-7},.7);
   if(a==='question'){Object.assign(f,{surprise:.25,head:-7,handLX:-160,handLY:-300});pose('friend',.2,{talk:.9,head:2},.8)}
  }
  if(a==='shock')Object.assign(h,{surprise:.9,smile:-.2,gaze:16});
  if(a==='distance'){pose('hero',.3,{gaze:-9,head:6},.8);pose('friend',.4,{gaze:8,head:7},.9)}
  if(a==='gift'){pose('hero',.3,{handRX:190,handRY:-240},.75)}
  if(a==='friendcall'){Object.assign(f,{handRX:85,handRY:-550,gaze:-5,head:-5,smile:.25});pose('friend',.5,{talk:0,head:0},1)}
 }
 if(w==='dinner'){
  Object.assign(h||{},{gaze:13,handRX:200,handRY:-230,smile:.1});
  if(a==='message'){one('phone-large')?.querySelector('[data-anim="connected"]')?.remove();}
  if(['compulsion','hesitate','temptation','wait'].includes(a)){
   pose('hero',.3,{handRX:125,handRY:-240,gaze:18,head:5},.9);to(v,.4,{phone:.5},.15);to(v,1.2,{phone:0},.4);
   if(a==='wait')pose('hero',du*.5,{handRX:80,handRY:-210,head:0},.8);
  }
  if(['uncertainty','decide'].includes(a))pose('hero',.4,{handRX:85,handRY:-210,gaze:0,head:0,smile:.45},.9);
  if(a==='call'){v.connected=0;pct(.50,{connected:1},.15)}
  if(a==='speaker'){pose('hero',.25,{handRX:204,handRY:-210,gaze:15},.5)}
  if(a==='apology'){Object.assign(h,{gaze:15,talk:.55,smile:.15});pose('hero',.4,{head:-5,handRX:145,handRY:-290},.7)}
  if(a==='listen'){Object.assign(h,{gaze:8,head:0,smile:.6});pose('hero',.5,{head:4},1.6)}
  if(['life','choice','release','comment','subscribe'].includes(a)){
   pose('hero',.3,{smile:.6,gaze:0,handRX:152,handRY:-345},.9);pose('hero',du*.7,{head:4,handRX:115,handRY:-285},.65);
  }
 }
 // Every shot has an entrance; the incoming composition supplies its transition.
 if(cfg.start>0)tl.from(root,{opacity:0,duration:.22,ease:cfg.future?'power4.out':'sine.inOut'},0);
 const accent=root.querySelector('.accent');
 if(accent){tl.from(accent,{y:105,rotation:-1,opacity:0,duration:.34,ease:'power3.out'},.12);tl.from(root.querySelector('.accent-line'),{scaleX:0,duration:.42,ease:'expo.out'},.27)}
 if(root.querySelector('.future-label'))tl.from(root.querySelector('.future-label'),{y:-17,opacity:0,duration:.25,ease:'power2.out'},.14);
 if(one('finder'))tl.from(one('finder'),{opacity:0,scale:.98,svgOrigin:'960 540',duration:.35,ease:'circ.out'},.14);
 // This is the living rig clock, not an empty duration tween.
 to(v,0,{t:du},du,'none');draw();
 return tl;
};
