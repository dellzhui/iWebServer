import{K as s,bs as a,d as e,aC as l,R as o,H as n,o as t,c,e as i,a7 as r,n as u,a as p,g as d,w as f,f as k,$ as g,Z as m,_ as y,A as b,Y as v,h as C,a9 as h,ad as _}from"./index-61faf58b.js";const B=s({closable:Boolean,type:{type:String,values:["success","info","warning","danger",""],default:""},hit:Boolean,disableTransitions:Boolean,color:{type:String,default:""},size:{type:String,values:a,default:""},effect:{type:String,values:["dark","light","plain"],default:"light"},round:Boolean}),E={close:s=>s instanceof MouseEvent,click:s=>s instanceof MouseEvent},S=e({name:"ElTag"});const $=_(h(e({...S,props:B,emits:E,setup(s,{emit:a}){const e=s,h=l(),_=o("tag"),B=n((()=>{const{type:s,hit:a,effect:l,closable:o,round:n}=e;return[_.b(),_.is("closable",o),_.m(s),_.m(h.value),_.m(l),_.is("hit",a),_.is("round",n)]})),E=s=>{a("close",s)},S=s=>{a("click",s)};return(s,a)=>s.disableTransitions?(t(),c("span",{key:0,class:u(p(B)),style:v({backgroundColor:s.color}),onClick:S},[i("span",{class:u(p(_).e("content"))},[r(s.$slots,"default")],2),s.closable?(t(),d(p(y),{key:0,class:u(p(_).e("close")),onClick:m(E,["stop"])},{default:f((()=>[k(p(g))])),_:1},8,["class","onClick"])):b("v-if",!0)],6)):(t(),d(C,{key:1,name:`${p(_).namespace.value}-zoom-in-center`,appear:""},{default:f((()=>[i("span",{class:u(p(B)),style:v({backgroundColor:s.color}),onClick:S},[i("span",{class:u(p(_).e("content"))},[r(s.$slots,"default")],2),s.closable?(t(),d(p(y),{key:0,class:u(p(_).e("close")),onClick:m(E,["stop"])},{default:f((()=>[k(p(g))])),_:1},8,["class","onClick"])):b("v-if",!0)],6)])),_:3},8,["name"]))}}),[["__file","/home/runner/work/element-plus/element-plus/packages/components/tag/src/tag.vue"]]));export{$ as E,B as t};