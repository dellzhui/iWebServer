import{d as a,ae as t,q as l,av as e,s as r,H as n,W as s,a as i,o,c as u,t as c,n as p,i as m,co as d}from"./index-61faf58b.js";const V=a({__name:"CountTo",props:{startVal:t.number.def(0),endVal:t.number.def(2021),duration:t.number.def(3e3),autoplay:t.bool.def(!0),decimals:t.number.validate((a=>a>=0)).def(0),decimal:t.string.def("."),separator:t.string.def(","),prefix:t.string.def(""),suffix:t.string.def(""),useEasing:t.bool.def(!0),easingFn:{type:Function,default:(a,t,l,e)=>l*(1-Math.pow(2,-10*a/e))*1024/1023+t}},emits:["mounted","callback"],setup(a,{expose:t,emit:V}){const f=a,{getPrefixCls:F}=m(),g=F("count-to"),S=a=>{const{decimals:t,decimal:l,separator:e,suffix:r,prefix:n}=f;a=Number(a).toFixed(t);const s=(a+="").split(".");let i=s[0];const o=s.length>1?l+s[1]:"",u=/(\d+)(\d{3})/;if(e&&!d(e))for(;u.test(i);)i=i.replace(u,"$1"+e+"$2");return n+i+o+r},A=l({localStartVal:f.startVal,displayValue:S(f.startVal),printVal:null,paused:!1,localDuration:f.duration,startTime:null,timestamp:null,remaining:null,rAF:null}),b=e(A,"displayValue");r((()=>{f.autoplay&&D(),V("mounted")}));const x=n((()=>f.startVal>f.endVal));s([()=>f.startVal,()=>f.endVal],(()=>{f.autoplay&&D()}));const D=()=>{const{startVal:a,duration:t}=f;A.localStartVal=a,A.startTime=null,A.localDuration=t,A.paused=!1,A.rAF=requestAnimationFrame(q)},y=()=>{cancelAnimationFrame(A.rAF)},T=()=>{A.startTime=null,A.localDuration=+A.remaining,A.localStartVal=+A.printVal,requestAnimationFrame(q)},q=a=>{const{useEasing:t,easingFn:l,endVal:e}=f;A.startTime||(A.startTime=a),A.timestamp=a;const r=a-A.startTime;A.remaining=A.localDuration-r,t?i(x)?A.printVal=A.localStartVal-l(r,0,A.localStartVal-e,A.localDuration):A.printVal=l(r,A.localStartVal,e-A.localStartVal,A.localDuration):i(x)?A.printVal=A.localStartVal-(A.localStartVal-e)*(r/A.localDuration):A.printVal=A.localStartVal+(e-A.localStartVal)*(r/A.localDuration),i(x)?A.printVal=A.printVal<e?e:A.printVal:A.printVal=A.printVal>e?e:A.printVal,A.displayValue=S(A.printVal),r<A.localDuration?A.rAF=requestAnimationFrame(q):V("callback")};return t({pauseResume:()=>{A.paused?(T(),A.paused=!1):(y(),A.paused=!0)},reset:()=>{A.startTime=null,cancelAnimationFrame(A.rAF),A.displayValue=S(f.startVal)},start:D,pause:y}),(a,t)=>(o(),u("span",{class:p(i(g))},c(i(b)),3))}});export{V as _};
