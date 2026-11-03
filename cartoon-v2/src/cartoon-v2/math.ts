export type Pt=[number,number];
export const clamp=(x:number)=>Math.max(0,Math.min(1,x));
export const ease=(x:number)=>{const t=clamp(x);return t*t*(3-2*t)};
export const tween=(f:number,a:number,b:number,x:number,y:number)=>x+(y-x)*ease((f-a)/(b-a));
export const blend=(a:number,b:number,t:number)=>a+(b-a)*t;
export const pulse=(f:number,a:number,b:number,c:number)=>ease((f-a)/(b-a))*(1-ease((f-b)/(c-b)));
export const points=(p:Pt[])=>p.map(x=>x.join(',')).join(' ');
export const ik=(a:Pt,b:Pt,l1:number,l2:number,sign=1):Pt=>{const dx=b[0]-a[0],dy=b[1]-a[1],n=Math.max(.001,Math.hypot(dx,dy)),d=Math.max(.01,Math.min(n,l1+l2-.01)),q=(l1*l1-l2*l2+d*d)/(2*d),h=Math.sqrt(Math.max(0,l1*l1-q*q));return [a[0]+q*dx/n-sign*h*dy/n,a[1]+q*dy/n+sign*h*dx/n]};
/** C1 vehicle position: a visible approach, then acceleration through the crossing. */
const driveKeys=[[389,-1100,18],[436,-400,10],[476,-70,10],[505,260,19],[540,1270,34],[577,2590,34]];
export const carX=(f:number)=>{if(f<389)return -1100;if(f>=577)return 2590+(f-577)*34;let i=0;while(f>driveKeys[i+1][0])i++;const [a,x,m]=driveKeys[i],[b,y,n]=driveKeys[i+1],h=b-a,t=(f-a)/h;return (2*t*t*t-3*t*t+1)*x+(t*t*t-2*t*t+t)*h*m+(-2*t*t*t+3*t*t)*y+(t*t*t-t*t)*h*n};
export const P={ink:'#111016',hood:'#ffa308',hoodShade:'#de8703',hoodLight:'#ffc255',rim:'#ffe0af',white:'#fff4dc',wall:'#d8c8af',blue:'#b6d4e2',road:'#8c9294',teal:'#507e7c',red:'#b9584d'};
