import{aW as e,H as a,aB as t,bN as o,r as n,N as l,K as s,b6 as i,L as r,ay as u,M as p,aY as d,d as c,a_ as v,bp as f,aC as m,a$ as y,R as x,V as b,bE as g,bO as h,bP as w,bk as S,W as k,X as z,b7 as C,s as I,av as E,y as $,z as F,o as P,c as M,A as V,F as _,n as j,a as B,a7 as N,e as A,g as R,w as O,a4 as H,_ as W,af as K,f as T,b5 as L,Z,aX as X,t as Y,Y as D,a9 as U,aZ as q,ad as G}from"./index-61faf58b.js";import{U as J}from"./event-5568c9d8.js";import{u as Q,a as ee}from"./el-button-e6441f40.js";import{i as ae}from"./el-popper-e10402a6.js";const te=()=>e&&/firefox/i.test(window.navigator.userAgent),oe=e=>/([(\uAC00-\uD7AF)|(\u3130-\u318F)])+/gi.test(e),ne=["class","style"],le=/^on[A-Z]/,se=(e={})=>{const{excludeListeners:n=!1,excludeKeys:l}=e,s=a((()=>((null==l?void 0:l.value)||[]).concat(ne))),i=t();return a(i?()=>{var e;return o(Object.entries(null==(e=i.proxy)?void 0:e.$attrs).filter((([e])=>!(s.value.includes(e)||n&&le.test(e)))))}:()=>({}))};let ie;const re=`\n  height:0 !important;\n  visibility:hidden !important;\n  ${te()?"":"overflow:hidden !important;"}\n  position:absolute !important;\n  z-index:-1000 !important;\n  top:0 !important;\n  right:0 !important;\n`,ue=["letter-spacing","line-height","padding-top","padding-bottom","font-family","font-weight","font-size","text-rendering","text-transform","width","text-indent","padding-left","padding-right","border-width","box-sizing"];function pe(e,a=1,t){var o;ie||(ie=document.createElement("textarea"),document.body.appendChild(ie));const{paddingSize:n,borderSize:s,boxSizing:i,contextStyle:r}=function(e){const a=window.getComputedStyle(e),t=a.getPropertyValue("box-sizing"),o=Number.parseFloat(a.getPropertyValue("padding-bottom"))+Number.parseFloat(a.getPropertyValue("padding-top")),n=Number.parseFloat(a.getPropertyValue("border-bottom-width"))+Number.parseFloat(a.getPropertyValue("border-top-width"));return{contextStyle:ue.map((e=>`${e}:${a.getPropertyValue(e)}`)).join(";"),paddingSize:o,borderSize:n,boxSizing:t}}(e);ie.setAttribute("style",`${r};${re}`),ie.value=e.value||e.placeholder||"";let u=ie.scrollHeight;const p={};"border-box"===i?u+=s:"content-box"===i&&(u-=n),ie.value="";const d=ie.scrollHeight-n;if(l(a)){let e=d*a;"border-box"===i&&(e=e+n+s),u=Math.max(e,u),p.minHeight=`${e}px`}if(l(t)){let e=d*t;"border-box"===i&&(e=e+n+s),u=Math.min(e,u)}return p.height=`${u}px`,null==(o=ie.parentNode)||o.removeChild(ie),ie=void 0,p}const de=s({id:{type:String,default:void 0},size:i,disabled:Boolean,modelValue:{type:r([String,Number,Object]),default:""},type:{type:String,default:"text"},resize:{type:String,values:["none","both","horizontal","vertical"]},autosize:{type:r([Boolean,Object]),default:!1},autocomplete:{type:String,default:"off"},formatter:{type:Function},parser:{type:Function},placeholder:{type:String},form:{type:String},readonly:{type:Boolean,default:!1},clearable:{type:Boolean,default:!1},showPassword:{type:Boolean,default:!1},showWordLimit:{type:Boolean,default:!1},suffixIcon:{type:u},prefixIcon:{type:u},containerRole:{type:String,default:void 0},label:{type:String,default:void 0},tabindex:{type:[String,Number],default:0},validateEvent:{type:Boolean,default:!0},inputStyle:{type:r([Object,Array,String]),default:()=>p({})}}),ce={[J]:e=>d(e),input:e=>d(e),change:e=>d(e),focus:e=>e instanceof FocusEvent,blur:e=>e instanceof FocusEvent,clear:()=>!0,mouseleave:e=>e instanceof MouseEvent,mouseenter:e=>e instanceof MouseEvent,keydown:e=>e instanceof Event,compositionstart:e=>e instanceof CompositionEvent,compositionupdate:e=>e instanceof CompositionEvent,compositionend:e=>e instanceof CompositionEvent},ve=["role"],fe=["id","type","disabled","formatter","parser","readonly","autocomplete","tabindex","aria-label","placeholder","form"],me=["id","tabindex","disabled","readonly","autocomplete","aria-label","placeholder","form"],ye=c({name:"ElInput",inheritAttrs:!1});const xe=G(U(c({...ye,props:de,emits:ce,setup(t,{expose:o,emit:l}){const s=t,i=v(),r=f(),u=a((()=>{const e={};return"combobox"===s.containerRole&&(e["aria-haspopup"]=i["aria-haspopup"],e["aria-owns"]=i["aria-owns"],e["aria-expanded"]=i["aria-expanded"]),e})),p=a((()=>["textarea"===s.type?re.b():ie.b(),ie.m(ne.value),ie.is("disabled",le.value),ie.is("exceed",_e.value),{[ie.b("group")]:r.prepend||r.append,[ie.bm("group","append")]:r.append,[ie.bm("group","prepend")]:r.prepend,[ie.m("prefix")]:r.prefix||s.prefixIcon,[ie.m("suffix")]:r.suffix||s.suffixIcon||s.clearable||s.showPassword,[ie.bm("suffix","password-clear")]:Fe.value&&Pe.value},i.class])),d=a((()=>[ie.e("wrapper"),ie.is("focus",ce.value)])),c=se({excludeKeys:a((()=>Object.keys(u.value)))}),{form:U,formItem:G}=Q(),{inputId:te}=ee(s,{formItemContext:G}),ne=m(),le=y(),ie=x("input"),re=x("textarea"),ue=b(),de=b(),ce=n(!1),ye=n(!1),xe=n(!1),be=n(!1),ge=n(),he=b(s.inputStyle),we=a((()=>ue.value||de.value)),Se=a((()=>{var e;return null!=(e=null==U?void 0:U.statusIcon)&&e})),ke=a((()=>(null==G?void 0:G.validateState)||"")),ze=a((()=>ke.value&&g[ke.value])),Ce=a((()=>be.value?h:w)),Ie=a((()=>[i.style,s.inputStyle])),Ee=a((()=>[s.inputStyle,he.value,{resize:s.resize}])),$e=a((()=>ae(s.modelValue)?"":String(s.modelValue))),Fe=a((()=>s.clearable&&!le.value&&!s.readonly&&!!$e.value&&(ce.value||ye.value))),Pe=a((()=>s.showPassword&&!le.value&&!s.readonly&&!!$e.value&&(!!$e.value||ce.value))),Me=a((()=>s.showWordLimit&&!!c.value.maxlength&&("text"===s.type||"textarea"===s.type)&&!le.value&&!s.readonly&&!s.showPassword)),Ve=a((()=>Array.from($e.value).length)),_e=a((()=>!!Me.value&&Ve.value>Number(c.value.maxlength))),je=a((()=>!!r.suffix||!!s.suffixIcon||Fe.value||s.showPassword||Me.value||!!ke.value&&Se.value)),[Be,Ne]=function(e){const a=n();return[function(){if(null==e.value)return;const{selectionStart:t,selectionEnd:o,value:n}=e.value;if(null==t||null==o)return;const l=n.slice(0,Math.max(0,t)),s=n.slice(Math.max(0,o));a.value={selectionStart:t,selectionEnd:o,value:n,beforeTxt:l,afterTxt:s}},function(){if(null==e.value||null==a.value)return;const{value:t}=e.value,{beforeTxt:o,afterTxt:n,selectionStart:l}=a.value;if(null==o||null==n||null==l)return;let s=t.length;if(t.endsWith(n))s=t.length-n.length;else if(t.startsWith(o))s=o.length;else{const e=o[l-1],a=t.indexOf(e,l-1);-1!==a&&(s=a+1)}e.value.setSelectionRange(s,s)}]}(ue);S(de,(e=>{if(!Me.value||"both"!==s.resize)return;const a=e[0],{width:t}=a.contentRect;ge.value={right:`calc(100% - ${t+15+6}px)`}}));const Ae=()=>{const{type:a,autosize:t}=s;if(e&&"textarea"===a&&de.value)if(t){const e=q(t)?t.minRows:void 0,a=q(t)?t.maxRows:void 0;he.value={...pe(de.value,e,a)}}else he.value={minHeight:pe(de.value).minHeight}},Re=()=>{const e=we.value;e&&e.value!==$e.value&&(e.value=$e.value)},Oe=async e=>{Be();let{value:a}=e.target;s.formatter&&(a=s.parser?s.parser(a):a,a=s.formatter(a)),xe.value||(a!==$e.value?(l(J,a),l("input",a),await z(),Re(),Ne()):Re())},He=e=>{l("change",e.target.value)},We=e=>{l("compositionstart",e),xe.value=!0},Ke=e=>{var a;l("compositionupdate",e);const t=null==(a=e.target)?void 0:a.value,o=t[t.length-1]||"";xe.value=!oe(o)},Te=e=>{l("compositionend",e),xe.value&&(xe.value=!1,Oe(e))},Le=()=>{be.value=!be.value,Ze()},Ze=async()=>{var e;await z(),null==(e=we.value)||e.focus()},Xe=e=>{ce.value=!0,l("focus",e)},Ye=e=>{var a;ce.value=!1,l("blur",e),s.validateEvent&&(null==(a=null==G?void 0:G.validate)||a.call(G,"blur").catch((e=>C())))},De=e=>{ye.value=!1,l("mouseleave",e)},Ue=e=>{ye.value=!0,l("mouseenter",e)},qe=e=>{l("keydown",e)},Ge=()=>{l(J,""),l("change",""),l("clear"),l("input","")};return k((()=>s.modelValue),(()=>{var e;z((()=>Ae())),s.validateEvent&&(null==(e=null==G?void 0:G.validate)||e.call(G,"change").catch((e=>C())))})),k($e,(()=>Re())),k((()=>s.type),(async()=>{await z(),Re(),Ae()})),I((()=>{!s.formatter&&s.parser,Re(),z(Ae)})),o({input:ue,textarea:de,ref:we,textareaStyle:Ee,autosize:E(s,"autosize"),focus:Ze,blur:()=>{var e;return null==(e=we.value)?void 0:e.blur()},select:()=>{var e;null==(e=we.value)||e.select()},clear:Ge,resizeTextarea:Ae}),(e,a)=>$((P(),M("div",K(B(u),{class:B(p),style:B(Ie),role:e.containerRole,onMouseenter:Ue,onMouseleave:De}),[V(" input "),"textarea"!==e.type?(P(),M(_,{key:0},[V(" prepend slot "),e.$slots.prepend?(P(),M("div",{key:0,class:j(B(ie).be("group","prepend"))},[N(e.$slots,"prepend")],2)):V("v-if",!0),A("div",{class:j(B(d))},[V(" prefix slot "),e.$slots.prefix||e.prefixIcon?(P(),M("span",{key:0,class:j(B(ie).e("prefix"))},[A("span",{class:j(B(ie).e("prefix-inner")),onClick:Ze},[N(e.$slots,"prefix"),e.prefixIcon?(P(),R(B(W),{key:0,class:j(B(ie).e("icon"))},{default:O((()=>[(P(),R(H(e.prefixIcon)))])),_:1},8,["class"])):V("v-if",!0)],2)],2)):V("v-if",!0),A("input",K({id:B(te),ref_key:"input",ref:ue,class:B(ie).e("inner")},B(c),{type:e.showPassword?be.value?"text":"password":e.type,disabled:B(le),formatter:e.formatter,parser:e.parser,readonly:e.readonly,autocomplete:e.autocomplete,tabindex:e.tabindex,"aria-label":e.label,placeholder:e.placeholder,style:e.inputStyle,form:s.form,onCompositionstart:We,onCompositionupdate:Ke,onCompositionend:Te,onInput:Oe,onFocus:Xe,onBlur:Ye,onChange:He,onKeydown:qe}),null,16,fe),V(" suffix slot "),B(je)?(P(),M("span",{key:1,class:j(B(ie).e("suffix"))},[A("span",{class:j(B(ie).e("suffix-inner")),onClick:Ze},[B(Fe)&&B(Pe)&&B(Me)?V("v-if",!0):(P(),M(_,{key:0},[N(e.$slots,"suffix"),e.suffixIcon?(P(),R(B(W),{key:0,class:j(B(ie).e("icon"))},{default:O((()=>[(P(),R(H(e.suffixIcon)))])),_:1},8,["class"])):V("v-if",!0)],64)),B(Fe)?(P(),R(B(W),{key:1,class:j([B(ie).e("icon"),B(ie).e("clear")]),onMousedown:Z(B(X),["prevent"]),onClick:Ge},{default:O((()=>[T(B(L))])),_:1},8,["class","onMousedown"])):V("v-if",!0),B(Pe)?(P(),R(B(W),{key:2,class:j([B(ie).e("icon"),B(ie).e("password")]),onClick:Le},{default:O((()=>[(P(),R(H(B(Ce))))])),_:1},8,["class"])):V("v-if",!0),B(Me)?(P(),M("span",{key:3,class:j(B(ie).e("count"))},[A("span",{class:j(B(ie).e("count-inner"))},Y(B(Ve))+" / "+Y(B(c).maxlength),3)],2)):V("v-if",!0),B(ke)&&B(ze)&&B(Se)?(P(),R(B(W),{key:4,class:j([B(ie).e("icon"),B(ie).e("validateIcon"),B(ie).is("loading","validating"===B(ke))])},{default:O((()=>[(P(),R(H(B(ze))))])),_:1},8,["class"])):V("v-if",!0)],2)],2)):V("v-if",!0)],2),V(" append slot "),e.$slots.append?(P(),M("div",{key:1,class:j(B(ie).be("group","append"))},[N(e.$slots,"append")],2)):V("v-if",!0)],64)):(P(),M(_,{key:1},[V(" textarea "),A("textarea",K({id:B(te),ref_key:"textarea",ref:de,class:B(re).e("inner")},B(c),{tabindex:e.tabindex,disabled:B(le),readonly:e.readonly,autocomplete:e.autocomplete,style:B(Ee),"aria-label":e.label,placeholder:e.placeholder,form:s.form,onCompositionstart:We,onCompositionupdate:Ke,onCompositionend:Te,onInput:Oe,onFocus:Xe,onBlur:Ye,onChange:He,onKeydown:qe}),null,16,me),B(Me)?(P(),M("span",{key:0,style:D(ge.value),class:j(B(ie).e("count"))},Y(B(Ve))+" / "+Y(B(c).maxlength),7)):V("v-if",!0)],64))],16,ve)),[[F,"hidden"!==e.type]])}}),[["__file","/home/runner/work/element-plus/element-plus/packages/components/input/src/input.vue"]]));export{xe as E,te as a,oe as i,se as u};
