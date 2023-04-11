import{_ as e}from"./ContentWrap.vue_vue_type_script_setup_true_lang-e04d0b7e.js";import{_ as o}from"./Dialog.vue_vue_type_style_index_0_lang-eae2c59d.js";import{d as l,j as t,r as a,q as i,o as s,g as m,w as r,f as p,a as n,m as d,t as u,c,F as f,G as _,e as v}from"./index-61faf58b.js";import{E as j}from"./el-button-e6441f40.js";import{F as g}from"./Form-7bd7b6f3.js";import{u as b}from"./useValidator-03bda066.js";import{g as D}from"./index-66726be2.js";import"./el-card-839bb50e.js";import"./el-popper-e10402a6.js";import"./index-f844f20d.js";import"./el-overlay-37f85d5d.js";import"./scroll-a2507849.js";import"./vnode-ae8de639.js";import"./use-dialog-3079ebb1.js";import"./event-5568c9d8.js";import"./index-7630a328.js";import"./refs-31ecab84.js";import"./el-col-0b4bbd49.js";import"./el-input-dc0bf57b.js";import"./el-tag-450bf357.js";import"./tsxHelper-98042daf.js";import"./debounce-7bd0410d.js";import"./validator-9877d78c.js";import"./el-input-number-b68dff77.js";import"./el-switch-3796832a.js";import"./el-divider-30a44c9a.js";import"./InputPassword-6a9b1358.js";import"./_plugin-vue_export-helper-1b428a4d.js";import"./style.css_vue_type_style_index_0_src_true_lang-cd9eff14.js";import"./aria-ecee1d93.js";import"./index-4154bb8a.js";const y=l({__name:"Dialog",setup(l){const{required:y}=b(),{t:k}=t(),x=a(!1),P=a(!1),h=i([{field:"field1",label:k("formDemo.input"),component:"Input",formItemProps:{rules:[y()]}},{field:"field2",label:k("formDemo.select"),component:"Select",componentProps:{options:[{label:"option1",value:"1"},{label:"option2",value:"2"}]}},{field:"field3",label:k("formDemo.radio"),component:"Radio",componentProps:{options:[{label:"option-1",value:"1"},{label:"option-2",value:"2"}]}},{field:"field4",label:k("formDemo.checkbox"),component:"Checkbox",value:[],componentProps:{options:[{label:"option-1",value:"1"},{label:"option-2",value:"2"},{label:"option-3",value:"3"}]}},{field:"field5",component:"DatePicker",label:k("formDemo.datePicker"),componentProps:{type:"date"}},{field:"field6",component:"TimeSelect",label:k("formDemo.timeSelect")}]);(async()=>{const e=await D();e&&(h[1].componentProps.options=e.data)})();const C=a(),V=()=>{var e,o;null==(o=null==(e=n(C))?void 0:e.getElFormRef())||o.validate((e=>{e?console.log("submit success"):console.log("submit fail")}))};return(l,t)=>(s(),m(n(e),{title:n(k)("dialogDemo.dialog"),message:n(k)("dialogDemo.dialogDes")},{default:r((()=>[p(n(j),{type:"primary",onClick:t[0]||(t[0]=e=>x.value=!x.value)},{default:r((()=>[d(u(n(k)("dialogDemo.open")),1)])),_:1}),p(n(j),{type:"primary",onClick:t[1]||(t[1]=e=>P.value=!P.value)},{default:r((()=>[d(u(n(k)("dialogDemo.combineWithForm")),1)])),_:1}),p(n(o),{modelValue:x.value,"onUpdate:modelValue":t[3]||(t[3]=e=>x.value=e),title:n(k)("dialogDemo.dialog")},{footer:r((()=>[p(n(j),{onClick:t[2]||(t[2]=e=>x.value=!1)},{default:r((()=>[d(u(n(k)("dialogDemo.close")),1)])),_:1})])),default:r((()=>[(s(),c(f,null,_(1e4,(e=>v("div",{key:e},u(e),1))),64))])),_:1},8,["modelValue","title"]),p(n(o),{modelValue:P.value,"onUpdate:modelValue":t[5]||(t[5]=e=>P.value=e),title:n(k)("dialogDemo.dialog")},{footer:r((()=>[p(n(j),{type:"primary",onClick:V},{default:r((()=>[d(u(n(k)("dialogDemo.submit")),1)])),_:1}),p(n(j),{onClick:t[4]||(t[4]=e=>P.value=!1)},{default:r((()=>[d(u(n(k)("dialogDemo.close")),1)])),_:1})])),default:r((()=>[p(n(g),{ref_key:"formRef",ref:C,schema:h},null,8,["schema"])])),_:1},8,["modelValue","title"])])),_:1},8,["title","message"]))}});export{y as default};
