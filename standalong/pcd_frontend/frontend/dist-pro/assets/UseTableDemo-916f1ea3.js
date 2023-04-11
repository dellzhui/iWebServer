import{_ as e}from"./ContentWrap.vue_vue_type_script_setup_true_lang-e04d0b7e.js";import{d as t,j as a,q as l,x as o,r as i,o as n,c as s,f as r,w as m,a as p,m as d,t as c,e as u,F as b}from"./index-61faf58b.js";import{_ as g}from"./Table.vue_vue_type_script_lang-b82724f5.js";import{g as D}from"./index-055e179d.js";import{E as f}from"./el-tag-450bf357.js";import{E as _}from"./el-button-e6441f40.js";import{u as v}from"./useTable-c44ab387.js";import"./el-card-839bb50e.js";import"./el-popper-e10402a6.js";import"./index-f844f20d.js";import"./tsxHelper-98042daf.js";import"./event-5568c9d8.js";import"./el-input-dc0bf57b.js";import"./index-7630a328.js";import"./scroll-a2507849.js";import"./debounce-7bd0410d.js";import"./validator-9877d78c.js";import"./index-4154bb8a.js";import"./el-message-box-f87b857a.js";import"./el-overlay-37f85d5d.js";import"./vnode-ae8de639.js";import"./aria-ecee1d93.js";const j={class:"ml-30px"},x={class:"ml-30px"},h=t({__name:"UseTableDemo",setup(t){const{register:h,tableObject:y,methods:C,elTableRef:w}=v({getListApi:D,response:{list:"list",total:"total"}}),{getList:k}=C;k();const{register:P,tableObject:S,methods:T}=v({getListApi:D,response:{list:"list",total:"total"}}),{getList:z}=T;z();const{t:U}=a(),L=l([{field:"index",label:U("tableDemo.index"),type:"index"},{field:"content",label:U("tableDemo.header"),children:[{field:"title",label:U("tableDemo.title")},{field:"author",label:U("tableDemo.author")},{field:"display_time",label:U("tableDemo.displayTime")},{field:"importance",label:U("tableDemo.importance"),formatter:(e,t,a)=>o(f,{type:1===a?"success":2===a?"warning":"danger"},(()=>U(1===a?"tableDemo.important":2===a?"tableDemo.good":"tableDemo.commonly")))},{field:"pageviews",label:U("tableDemo.pageviews")}]},{field:"action",label:U("tableDemo.action")}]),R=e=>{console.log(e)},$=i(),A=e=>{$.value=e?{total:y.total}:void 0},E=e=>{const{setProps:t}=C;t({reserveIndex:e})},I=e=>{const{setProps:t}=C;t({selection:e})},q=i(1),O=()=>{const{setColumn:e}=C;e([{field:"title",path:"label",value:`${U("tableDemo.title")}${p(q)}`}]),q.value++},F=e=>{const{setProps:t}=C;t({expand:e})},H=()=>{var e;null==(e=p(w))||e.toggleAllSelection()};return(t,a)=>(n(),s(b,null,[r(p(e),{title:`UseTable ${p(U)("tableDemo.operate")}`},{default:m((()=>[r(p(_),{onClick:a[0]||(a[0]=e=>A(!0))},{default:m((()=>[d(c(p(U)("tableDemo.show"))+" "+c(p(U)("tableDemo.pagination")),1)])),_:1}),r(p(_),{onClick:a[1]||(a[1]=e=>A(!1))},{default:m((()=>[d(c(p(U)("tableDemo.hidden"))+" "+c(p(U)("tableDemo.pagination")),1)])),_:1}),r(p(_),{onClick:a[2]||(a[2]=e=>E(!0))},{default:m((()=>[d(c(p(U)("tableDemo.reserveIndex")),1)])),_:1}),r(p(_),{onClick:a[3]||(a[3]=e=>E(!1))},{default:m((()=>[d(c(p(U)("tableDemo.restoreIndex")),1)])),_:1}),r(p(_),{onClick:a[4]||(a[4]=e=>I(!0))},{default:m((()=>[d(c(p(U)("tableDemo.showSelections")),1)])),_:1}),r(p(_),{onClick:a[5]||(a[5]=e=>I(!1))},{default:m((()=>[d(c(p(U)("tableDemo.hiddenSelections")),1)])),_:1}),r(p(_),{onClick:O},{default:m((()=>[d(c(p(U)("tableDemo.changeTitle")),1)])),_:1}),r(p(_),{onClick:a[6]||(a[6]=e=>F(!0))},{default:m((()=>[d(c(p(U)("tableDemo.showExpandedRows")),1)])),_:1}),r(p(_),{onClick:a[7]||(a[7]=e=>F(!1))},{default:m((()=>[d(c(p(U)("tableDemo.hiddenExpandedRows")),1)])),_:1}),r(p(_),{onClick:H},{default:m((()=>[d(c(p(U)("tableDemo.selectAllNone")),1)])),_:1})])),_:1},8,["title"]),r(p(e),{title:`UseTable ${p(U)("tableDemo.example")}`},{default:m((()=>[r(p(g),{pageSize:p(y).pageSize,"onUpdate:pageSize":a[8]||(a[8]=e=>p(y).pageSize=e),currentPage:p(y).currentPage,"onUpdate:currentPage":a[9]||(a[9]=e=>p(y).currentPage=e),columns:L,data:p(y).tableList,loading:p(y).loading,pagination:$.value,onRegister:p(h)},{action:m((e=>[r(p(_),{type:"primary",onClick:t=>R(e)},{default:m((()=>[d(c(p(U)("tableDemo.action")),1)])),_:2},1032,["onClick"])])),expand:m((e=>[u("div",j,[u("div",null,c(p(U)("tableDemo.title"))+"："+c(e.row.title),1),u("div",null,c(p(U)("tableDemo.author"))+"："+c(e.row.author),1),u("div",null,c(p(U)("tableDemo.displayTime"))+"："+c(e.row.display_time),1)])])),_:1},8,["pageSize","currentPage","columns","data","loading","pagination","onRegister"])])),_:1},8,["title"]),r(p(e),{title:`UseTable 2 ${p(U)("tableDemo.example")}`},{default:m((()=>[r(p(g),{pageSize:p(S).pageSize,"onUpdate:pageSize":a[10]||(a[10]=e=>p(S).pageSize=e),currentPage:p(S).currentPage,"onUpdate:currentPage":a[11]||(a[11]=e=>p(S).currentPage=e),columns:L,data:p(S).tableList,loading:p(S).loading,pagination:$.value,onRegister:p(P)},{action:m((e=>[r(p(_),{type:"primary",onClick:t=>R(e)},{default:m((()=>[d(c(p(U)("tableDemo.action")),1)])),_:2},1032,["onClick"])])),expand:m((e=>[u("div",x,[u("div",null,c(p(U)("tableDemo.title"))+"："+c(e.row.title),1),u("div",null,c(p(U)("tableDemo.author"))+"："+c(e.row.author),1),u("div",null,c(p(U)("tableDemo.displayTime"))+"："+c(e.row.display_time),1)])])),_:1},8,["pageSize","currentPage","columns","data","loading","pagination","onRegister"])])),_:1},8,["title"])],64))}});export{h as default};
