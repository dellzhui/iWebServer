import{_ as e}from"./ContentWrap.vue_vue_type_script_setup_true_lang-e04d0b7e.js";import{d as a,j as t,x as l,r as o,o as i,g as s,w as r,f as m,a as p,m as n,t as d}from"./index-61faf58b.js";import{_ as b}from"./Table.vue_vue_type_script_lang-b82724f5.js";import{g as c}from"./index-055e179d.js";import{E as u}from"./el-tag-450bf357.js";import{E as f}from"./el-button-e6441f40.js";import"./el-card-839bb50e.js";import"./el-popper-e10402a6.js";import"./index-f844f20d.js";import"./tsxHelper-98042daf.js";import"./event-5568c9d8.js";import"./el-input-dc0bf57b.js";import"./index-7630a328.js";import"./scroll-a2507849.js";import"./debounce-7bd0410d.js";import"./validator-9877d78c.js";import"./index-4154bb8a.js";const j=a({__name:"DefaultTable",setup(a){const{t:j}=t(),_=[{field:"index",label:j("tableDemo.index"),type:"index"},{field:"title",label:j("tableDemo.title")},{field:"author",label:j("tableDemo.author")},{field:"display_time",label:j("tableDemo.displayTime"),sortable:!0},{field:"importance",label:j("tableDemo.importance"),formatter:(e,a,t)=>l(u,{type:1===t?"success":2===t?"warning":"danger"},(()=>j(1===t?"tableDemo.important":2===t?"tableDemo.good":"tableDemo.commonly")))},{field:"pageviews",label:j("tableDemo.pageviews")},{field:"action",label:j("tableDemo.action")}],g=o(!0);let D=o([]);(async e=>{const a=await c(e||{pageIndex:1,pageSize:10}).catch((()=>{})).finally((()=>{g.value=!1}));a&&(D.value=a.data.list)})();return(a,t)=>(i(),s(p(e),{title:p(j)("tableDemo.table"),message:p(j)("tableDemo.tableDes")},{default:r((()=>[m(p(b),{columns:_,data:p(D),loading:g.value,defaultSort:{prop:"display_time",order:"descending"}},{action:r((e=>[m(p(f),{type:"primary",onClick:a=>(e=>{console.log(e)})(e)},{default:r((()=>[n(d(p(j)("tableDemo.action")),1)])),_:2},1032,["onClick"])])),_:1},8,["data","loading"])])),_:1},8,["title","message"]))}});export{j as default};