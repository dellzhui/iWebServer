import{D as a}from"./Descriptions-9e91dd7b.js";import{d as e,j as t,o,g as r,w as n,f as s,a as m,m as c,t as i,e as p}from"./index-61faf58b.js";import{E as l}from"./el-tag-450bf357.js";const d=["innerHTML"],u=e({__name:"Detail",props:{currentRow:{type:Object,default:()=>null},detailSchema:{type:Array,default:()=>[]}},setup(e){const{t:u}=t();return(t,f)=>(o(),r(m(a),{schema:e.detailSchema,data:e.currentRow||{}},{importance:n((({row:a})=>[s(m(l),{type:1===a.importance?"success":2===a.importance?"warning":"danger"},{default:n((()=>[c(i(1===a.importance?m(u)("tableDemo.important"):2===a.importance?m(u)("tableDemo.good"):m(u)("tableDemo.commonly")),1)])),_:2},1032,["type"])])),content:n((({row:a})=>[p("div",{innerHTML:a.content},null,8,d)])),_:1},8,["schema","data"]))}});export{u as _};
