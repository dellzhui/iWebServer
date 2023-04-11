import{F as e}from"./Form-7bd7b6f3.js";import{_ as s}from"./ContentWrap.vue_vue_type_script_setup_true_lang-e04d0b7e.js";import{d as r,u as o,r as t,q as a,s as l,o as i,g as n,w as p,f as m,a as d,m as u,t as c,j as f,E as j}from"./index-61faf58b.js";import{u as _}from"./useValidator-03bda066.js";import{E as v}from"./el-button-e6441f40.js";import{u as w}from"./useForm-e3b0495d.js";import{b as y,c as g,d as h}from"./index-34f08ef1.js";import{_ as P}from"./_plugin-vue_export-helper-1b428a4d.js";import"./el-col-0b4bbd49.js";import"./el-popper-e10402a6.js";import"./index-f844f20d.js";import"./el-input-dc0bf57b.js";import"./event-5568c9d8.js";import"./el-tag-450bf357.js";import"./tsxHelper-98042daf.js";import"./index-7630a328.js";import"./scroll-a2507849.js";import"./debounce-7bd0410d.js";import"./validator-9877d78c.js";import"./el-input-number-b68dff77.js";import"./el-switch-3796832a.js";import"./el-divider-30a44c9a.js";import"./InputPassword-6a9b1358.js";import"./style.css_vue_type_style_index_0_src_true_lang-cd9eff14.js";import"./aria-ecee1d93.js";import"./el-card-839bb50e.js";import"./index-4154bb8a.js";const b=P(r({__name:"UserAdd",setup(r){const{required:P,isEmail:b,isEqual:I}=_(),{t:x}=f(),{push:F,currentRoute:C}=o(),k=t(!1),R=C.value.query,E=a([{field:"email",label:x("邮箱"),component:"Input",formItemProps:{rules:[P(),{validator:b,trigger:"blur"}]},colProps:{span:13},componentProps:{style:{width:"100%"},placeholder:x("请输入邮箱")}},{field:"username",label:x("用户名"),component:"Input",formItemProps:{rules:[P()]},colProps:{span:13},componentProps:{style:{width:"100%"},placeholder:x("用户名")}},{field:"password",label:x("密码"),component:"InputPassword",value:"",formItemProps:{rules:[P()]},colProps:{span:13},componentProps:{style:{width:"100%"},placeholder:x("请输入初始化密码")}},{field:"confrimPassword",label:x("确认密码"),component:"InputPassword",value:"",formItemProps:{rules:[P(),{validator:async(e,s,r)=>{const{getFormData:o}=O,t=await o();I(null==t?void 0:t.password,s,r,"两次密码不一致")},trigger:"blur"}]},colProps:{span:13},componentProps:{style:{width:"100%"},placeholder:x("请确认初始化密码")}}]),{register:q,elFormRef:D,methods:O}=w(),V=async()=>{const e=d(D);await(null==e?void 0:e.validate((async e=>{if(e){k.value=!0;const{getFormData:e}=O,s=await e();if(Object.keys(R).length){const e={password:null==s?void 0:s.password,confrimPassword:null==s?void 0:s.confrimPassword};A(e)}else $(s)}})))},$=async e=>{const s=await y(e).catch((e=>{-1107===e.response.data.errorCode?j.error("添加用户的邮箱已存在"):-1108===e.response.data.errorCode&&j.error("用户名已存在")})).finally((()=>{k.value=!1}));s&&s.success&&F("/user/list")},A=async e=>{const s=await g(e,{userId:R.userId}).catch((e=>{-1107===e.response.data.errorCode?j.error("添加用户的邮箱已存在"):-1108===e.response.data.errorCode&&j.error("用户名已存在")})).finally((()=>{k.value=!1}));s&&s.success&&F("/user/list")},H=t(),U=(e,s)=>{var r,o;const t=null==(r=d(H))?void 0:r.getElFormRef();e?null==t||t.resetFields():null==(o=d(H))||o.setValues(s)};return l((()=>{Object.keys(R).length&&(async e=>{const s=await h({username:e.username});s.success&&U(!1,s.data[0])})(R)})),(r,o)=>(i(),n(d(s),{title:`${d(x)(Object.keys(d(R)).length?"编辑用户":"新增用户")}`},{default:p((()=>[m(d(e),{isCustom:!1,schema:E,ref_key:"formRef",ref:H,onRegister:d(q)},null,8,["schema","onRegister"]),m(d(v),{loading:k.value,type:"primary",class:"w-[10%]",onClick:V},{default:p((()=>[u(c(d(x)("提交")),1)])),_:1},8,["loading"])])),_:1},8,["title"]))}}),[["__scopeId","data-v-60cc7a44"]]);export{b as default};
