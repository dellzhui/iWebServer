import{d as t,ae as e,H as r,x as s,a as l}from"./index-61faf58b.js";const o=t({name:"Highlight",props:{tag:e.string.def("span"),keys:{type:Array,default:()=>[]},color:e.string.def("var(--el-color-primary)")},emits:["click"],setup(t,{emit:e,slots:o}){const a=r((()=>t.keys.map((r=>s("span",{onClick:()=>{e("click",r)},style:{color:t.color,cursor:"pointer"}},r))))),n=()=>{if(!(null==o?void 0:o.default))return null;const e=null==o?void 0:o.default()[0].children;if(!e)return null==o?void 0:o.default()[0];const r=(n=e,t.keys.forEach(((t,e)=>{const r=new RegExp(t,"g");n=n.replace(r,`{{${e}}}`)})),n.split(/{{|}}/));var n;const i=/^[0-9]*$/,c=r.map((t=>i.test(t)&&l(a)[t]||t));return s(t.tag,c)};return()=>n()}});export{o as _};