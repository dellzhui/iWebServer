import{d as e,j as t,r as s,q as a,I as l,o as i,g as n,w as o,f as d,a as r,e as c,n as x,t as u,i as _}from"./index-61faf58b.js";import{a as m,E as p}from"./el-col-0b4bbd49.js";import{E as f}from"./el-card-839bb50e.js";import{E as g}from"./el-skeleton-item-e40507b6.js";import{_ as v}from"./CountTo.vue_vue_type_script_setup_true_lang-2f8d0770.js";import{r as y}from"./index-4154bb8a.js";import{_ as h}from"./_plugin-vue_export-helper-1b428a4d.js";const b=()=>y.get({url:"/analysis/userAccessSource"}),j=()=>y.get({url:"/analysis/weeklyUserActivity"}),w=()=>y.get({url:"/analysis/monthlySales"}),$={class:"flex flex-col justify-between"},k={class:"flex flex-col justify-between"},z={class:"flex flex-col justify-between"},S={class:"flex flex-col justify-between"},E=h(e({__name:"PanelGroup",setup(e){const{t:h}=t(),{getPrefixCls:b}=_(),j=b("panel"),w=s(!0);let E=a({users:0,messages:0,moneys:0,shoppings:0});return(async()=>{const e=await y.get({url:"/analysis/total"}).catch((()=>{})).finally((()=>{w.value=!1}));E=Object.assign(E,(null==e?void 0:e.data)||{})})(),(e,t)=>{const s=l("Icon");return i(),n(r(p),{gutter:20,justify:"space-between",class:x(r(j))},{default:o((()=>[d(r(m),{xl:6,lg:6,md:12,sm:12,xs:24},{default:o((()=>[d(r(f),{shadow:"hover",class:"mb-20px"},{default:o((()=>[d(r(g),{loading:w.value,animated:"",rows:2},{default:o((()=>[c("div",{class:x(`${r(j)}__item flex justify-between`)},[c("div",null,[c("div",{class:x(`${r(j)}__item--icon ${r(j)}__item--peoples p-16px inline-block rounded-6px`)},[d(s,{icon:"svg-icon:peoples",size:40})],2)]),c("div",$,[c("div",{class:x(`${r(j)}__item--text text-16px text-gray-500 text-right`)},u(r(h)("analysis.newUser")),3),d(r(v),{class:"text-20px font-700 text-right","start-val":0,"end-val":102400,duration:2600})])],2)])),_:1},8,["loading"])])),_:1})])),_:1}),d(r(m),{xl:6,lg:6,md:12,sm:12,xs:24},{default:o((()=>[d(r(f),{shadow:"hover",class:"mb-20px"},{default:o((()=>[d(r(g),{loading:w.value,animated:"",rows:2},{default:o((()=>[c("div",{class:x(`${r(j)}__item flex justify-between`)},[c("div",null,[c("div",{class:x(`${r(j)}__item--icon ${r(j)}__item--message p-16px inline-block rounded-6px`)},[d(s,{icon:"svg-icon:message",size:40})],2)]),c("div",k,[c("div",{class:x(`${r(j)}__item--text text-16px text-gray-500 text-right`)},u(r(h)("analysis.unreadInformation")),3),d(r(v),{class:"text-20px font-700 text-right","start-val":0,"end-val":81212,duration:2600})])],2)])),_:1},8,["loading"])])),_:1})])),_:1}),d(r(m),{xl:6,lg:6,md:12,sm:12,xs:24},{default:o((()=>[d(r(f),{shadow:"hover",class:"mb-20px"},{default:o((()=>[d(r(g),{loading:w.value,animated:"",rows:2},{default:o((()=>[c("div",{class:x(`${r(j)}__item flex justify-between`)},[c("div",null,[c("div",{class:x(`${r(j)}__item--icon ${r(j)}__item--money p-16px inline-block rounded-6px`)},[d(s,{icon:"svg-icon:money",size:40})],2)]),c("div",z,[c("div",{class:x(`${r(j)}__item--text text-16px text-gray-500 text-right`)},u(r(h)("analysis.transactionAmount")),3),d(r(v),{class:"text-20px font-700 text-right","start-val":0,"end-val":9280,duration:2600})])],2)])),_:1},8,["loading"])])),_:1})])),_:1}),d(r(m),{xl:6,lg:6,md:12,sm:12,xs:24},{default:o((()=>[d(r(f),{shadow:"hover",class:"mb-20px"},{default:o((()=>[d(r(g),{loading:w.value,animated:"",rows:2},{default:o((()=>[c("div",{class:x(`${r(j)}__item flex justify-between`)},[c("div",null,[c("div",{class:x(`${r(j)}__item--icon ${r(j)}__item--shopping p-16px inline-block rounded-6px`)},[d(s,{icon:"svg-icon:shopping",size:40})],2)]),c("div",S,[c("div",{class:x(`${r(j)}__item--text text-16px text-gray-500 text-right`)},u(r(h)("analysis.totalShopping")),3),d(r(v),{class:"text-20px font-700 text-right","start-val":0,"end-val":13600,duration:2600})])],2)])),_:1},8,["loading"])])),_:1})])),_:1})])),_:1},8,["class"])}}}),[["__scopeId","data-v-843cc555"]]),I=Object.freeze(Object.defineProperty({__proto__:null,default:E},Symbol.toStringTag,{value:"Module"}));export{E as P,j as a,w as b,I as c,b as g};
