import{W as e,bd as n,X as o,ab as t,d as a,_ as s,cJ as l,R as r,r as i,S as c,q as u,H as d,cK as p,aC as f,s as m,at as v,be as g,a9 as b,I as h,o as y,g as C,w as E,y as x,f as w,e as B,n as k,Y as M,Z as I,c as T,a4 as S,A as R,t as _,b2 as A,a7 as z,m as j,z as L,h as P,aW as V,aY as $,bJ as O,ah as H,bm as K,aZ as q,bb as D,bg as U,bW as W}from"./index-61faf58b.js";import{E as F}from"./el-button-e6441f40.js";import{E as Z}from"./el-input-dc0bf57b.js";import{E as J,u as Y,a as X,b as G}from"./el-overlay-37f85d5d.js";import{o as N}from"./aria-ecee1d93.js";import{e as Q}from"./el-popper-e10402a6.js";import{i as ee}from"./validator-9877d78c.js";import{u as ne}from"./index-7630a328.js";import{u as oe}from"./index-f844f20d.js";const te="_trap-focus-children",ae=[],se=e=>{if(0===ae.length)return;const n=ae[ae.length-1][te];if(n.length>0&&e.code===t.tab){if(1===n.length)return e.preventDefault(),void(document.activeElement!==n[0]&&n[0].focus());const o=e.shiftKey,t=e.target===n[0],a=e.target===n[n.length-1];t&&o&&(e.preventDefault(),n[n.length-1].focus()),a&&!o&&(e.preventDefault(),n[0].focus())}},le=a({name:"ElMessageBox",directives:{TrapFocus:{beforeMount(e){e[te]=N(e),ae.push(e),ae.length<=1&&document.addEventListener("keydown",se)},updated(e){o((()=>{e[te]=N(e)}))},unmounted(){ae.shift(),0===ae.length&&document.removeEventListener("keydown",se)}}},components:{ElButton:F,ElFocusTrap:Q,ElInput:Z,ElOverlay:J,ElIcon:s,...l},inheritAttrs:!1,props:{buttonSize:{type:String,validator:ee},modal:{type:Boolean,default:!0},lockScroll:{type:Boolean,default:!0},showClose:{type:Boolean,default:!0},closeOnClickModal:{type:Boolean,default:!0},closeOnPressEscape:{type:Boolean,default:!0},closeOnHashChange:{type:Boolean,default:!0},center:Boolean,draggable:Boolean,roundButton:{default:!1,type:Boolean},container:{type:String,default:"body"},boxType:{type:String,default:""}},emits:["vanish","action"],setup(t,{emit:a}){const{t:s}=ne(),l=r("message-box"),b=i(!1),{nextZIndex:h}=c(),y=u({autofocus:!0,beforeClose:null,callback:null,cancelButtonText:"",cancelButtonClass:"",confirmButtonText:"",confirmButtonClass:"",customClass:"",customStyle:{},dangerouslyUseHTMLString:!1,distinguishCancelAndClose:!1,icon:"",inputPattern:null,inputPlaceholder:"",inputType:"text",inputValue:null,inputValidator:null,inputErrorMessage:"",message:null,modalFade:!0,modalClass:"",showCancelButton:!1,showConfirmButton:!0,type:"",title:void 0,showInput:!1,action:"",confirmButtonLoading:!1,cancelButtonLoading:!1,confirmButtonDisabled:!1,editorErrorMessage:"",validateError:!1,zIndex:h()}),C=d((()=>{const e=y.type;return{[l.bm("icon",e)]:e&&p[e]}})),E=oe(),x=oe(),w=f(d((()=>t.buttonSize)),{prop:!0,form:!0,formItem:!0}),B=d((()=>y.icon||p[y.type]||"")),k=d((()=>!!y.message)),M=i(),I=i(),T=i(),S=i(),R=i(),_=d((()=>y.confirmButtonClass));e((()=>y.inputValue),(async e=>{await o(),"prompt"===t.boxType&&null!==e&&V()}),{immediate:!0}),e((()=>b.value),(e=>{var n,a;e&&("prompt"!==t.boxType&&(y.autofocus?T.value=null!=(a=null==(n=R.value)?void 0:n.$el)?a:M.value:T.value=M.value),y.zIndex=h()),"prompt"===t.boxType&&(e?o().then((()=>{var e;S.value&&S.value.$el&&(y.autofocus?T.value=null!=(e=$())?e:M.value:T.value=M.value)})):(y.editorErrorMessage="",y.validateError=!1))}));const A=d((()=>t.draggable));function z(){b.value&&(b.value=!1,o((()=>{y.action&&a("action",y.action)})))}Y(M,I,A),m((async()=>{await o(),t.closeOnHashChange&&window.addEventListener("hashchange",z)})),v((()=>{t.closeOnHashChange&&window.removeEventListener("hashchange",z)}));const j=()=>{t.closeOnClickModal&&P(y.distinguishCancelAndClose?"close":"cancel")},L=G(j),P=e=>{var n;("prompt"!==t.boxType||"confirm"!==e||V())&&(y.action=e,y.beforeClose?null==(n=y.beforeClose)||n.call(y,e,y,z):z())},V=()=>{if("prompt"===t.boxType){const e=y.inputPattern;if(e&&!e.test(y.inputValue||""))return y.editorErrorMessage=y.inputErrorMessage||s("el.messagebox.error"),y.validateError=!0,!1;const n=y.inputValidator;if("function"==typeof n){const e=n(y.inputValue);if(!1===e)return y.editorErrorMessage=y.inputErrorMessage||s("el.messagebox.error"),y.validateError=!0,!1;if("string"==typeof e)return y.editorErrorMessage=e,y.validateError=!0,!1}}return y.editorErrorMessage="",y.validateError=!1,!0},$=()=>{const e=S.value.$refs;return e.input||e.textarea},O=()=>{P("close")};return t.lockScroll&&X(b),((o,t)=>{let a;e((()=>o.value),(e=>{var o,s;e?(a=document.activeElement,n(t)&&(null==(s=(o=t.value).focus)||s.call(o))):a.focus()}))})(b),{...g(y),ns:l,overlayEvent:L,visible:b,hasMessage:k,typeClass:C,contentId:E,inputId:x,btnSize:w,iconComponent:B,confirmButtonClasses:_,rootRef:M,focusStartRef:T,headerRef:I,inputRef:S,confirmRef:R,doClose:z,handleClose:O,onCloseRequested:()=>{t.closeOnPressEscape&&O()},handleWrapperClick:j,handleInputEnter:e=>{if("textarea"!==y.inputType)return e.preventDefault(),P("confirm")},handleAction:P,t:s}}}),re=["aria-label","aria-describedby"],ie=["aria-label"],ce=["id"];var ue=b(le,[["render",function(e,n,o,t,a,s){const l=h("el-icon"),r=h("close"),i=h("el-input"),c=h("el-button"),u=h("el-focus-trap"),d=h("el-overlay");return y(),C(P,{name:"fade-in-linear",onAfterLeave:n[11]||(n[11]=n=>e.$emit("vanish")),persisted:""},{default:E((()=>[x(w(d,{"z-index":e.zIndex,"overlay-class":[e.ns.is("message-box"),e.modalClass],mask:e.modal},{default:E((()=>[B("div",{role:"dialog","aria-label":e.title,"aria-modal":"true","aria-describedby":e.showInput?void 0:e.contentId,class:k(`${e.ns.namespace.value}-overlay-message-box`),onClick:n[8]||(n[8]=(...n)=>e.overlayEvent.onClick&&e.overlayEvent.onClick(...n)),onMousedown:n[9]||(n[9]=(...n)=>e.overlayEvent.onMousedown&&e.overlayEvent.onMousedown(...n)),onMouseup:n[10]||(n[10]=(...n)=>e.overlayEvent.onMouseup&&e.overlayEvent.onMouseup(...n))},[w(u,{loop:"",trapped:e.visible,"focus-trap-el":e.rootRef,"focus-start-el":e.focusStartRef,onReleaseRequested:e.onCloseRequested},{default:E((()=>[B("div",{ref:"rootRef",class:k([e.ns.b(),e.customClass,e.ns.is("draggable",e.draggable),{[e.ns.m("center")]:e.center}]),style:M(e.customStyle),tabindex:"-1",onClick:n[7]||(n[7]=I((()=>{}),["stop"]))},[null!==e.title&&void 0!==e.title?(y(),T("div",{key:0,ref:"headerRef",class:k(e.ns.e("header"))},[B("div",{class:k(e.ns.e("title"))},[e.iconComponent&&e.center?(y(),C(l,{key:0,class:k([e.ns.e("status"),e.typeClass])},{default:E((()=>[(y(),C(S(e.iconComponent)))])),_:1},8,["class"])):R("v-if",!0),B("span",null,_(e.title),1)],2),e.showClose?(y(),T("button",{key:0,type:"button",class:k(e.ns.e("headerbtn")),"aria-label":e.t("el.messagebox.close"),onClick:n[0]||(n[0]=n=>e.handleAction(e.distinguishCancelAndClose?"close":"cancel")),onKeydown:n[1]||(n[1]=A(I((n=>e.handleAction(e.distinguishCancelAndClose?"close":"cancel")),["prevent"]),["enter"]))},[w(l,{class:k(e.ns.e("close"))},{default:E((()=>[w(r)])),_:1},8,["class"])],42,ie)):R("v-if",!0)],2)):R("v-if",!0),B("div",{id:e.contentId,class:k(e.ns.e("content"))},[B("div",{class:k(e.ns.e("container"))},[e.iconComponent&&!e.center&&e.hasMessage?(y(),C(l,{key:0,class:k([e.ns.e("status"),e.typeClass])},{default:E((()=>[(y(),C(S(e.iconComponent)))])),_:1},8,["class"])):R("v-if",!0),e.hasMessage?(y(),T("div",{key:1,class:k(e.ns.e("message"))},[z(e.$slots,"default",{},(()=>[e.dangerouslyUseHTMLString?(y(),C(S(e.showInput?"label":"p"),{key:1,for:e.showInput?e.inputId:void 0,innerHTML:e.message},null,8,["for","innerHTML"])):(y(),C(S(e.showInput?"label":"p"),{key:0,for:e.showInput?e.inputId:void 0},{default:E((()=>[j(_(e.dangerouslyUseHTMLString?"":e.message),1)])),_:1},8,["for"]))]))],2)):R("v-if",!0)],2),x(B("div",{class:k(e.ns.e("input"))},[w(i,{id:e.inputId,ref:"inputRef",modelValue:e.inputValue,"onUpdate:modelValue":n[2]||(n[2]=n=>e.inputValue=n),type:e.inputType,placeholder:e.inputPlaceholder,"aria-invalid":e.validateError,class:k({invalid:e.validateError}),onKeydown:A(e.handleInputEnter,["enter"])},null,8,["id","modelValue","type","placeholder","aria-invalid","class","onKeydown"]),B("div",{class:k(e.ns.e("errormsg")),style:M({visibility:e.editorErrorMessage?"visible":"hidden"})},_(e.editorErrorMessage),7)],2),[[L,e.showInput]])],10,ce),B("div",{class:k(e.ns.e("btns"))},[e.showCancelButton?(y(),C(c,{key:0,loading:e.cancelButtonLoading,class:k([e.cancelButtonClass]),round:e.roundButton,size:e.btnSize,onClick:n[3]||(n[3]=n=>e.handleAction("cancel")),onKeydown:n[4]||(n[4]=A(I((n=>e.handleAction("cancel")),["prevent"]),["enter"]))},{default:E((()=>[j(_(e.cancelButtonText||e.t("el.messagebox.cancel")),1)])),_:1},8,["loading","class","round","size"])):R("v-if",!0),x(w(c,{ref:"confirmRef",type:"primary",loading:e.confirmButtonLoading,class:k([e.confirmButtonClasses]),round:e.roundButton,disabled:e.confirmButtonDisabled,size:e.btnSize,onClick:n[5]||(n[5]=n=>e.handleAction("confirm")),onKeydown:n[6]||(n[6]=A(I((n=>e.handleAction("confirm")),["prevent"]),["enter"]))},{default:E((()=>[j(_(e.confirmButtonText||e.t("el.messagebox.confirm")),1)])),_:1},8,["loading","class","round","disabled","size"]),[[L,e.showConfirmButton]])],2)],6)])),_:3},8,["trapped","focus-trap-el","focus-start-el","onReleaseRequested"])],42,re)])),_:3},8,["z-index","overlay-class","mask"]),[[L,e.visible]])])),_:3})}],["__file","/home/runner/work/element-plus/element-plus/packages/components/message-box/src/index.vue"]]);const de=new Map,pe=(e,n,o=null)=>{const t=w(ue,e,U(e.message)||O(e.message)?{default:U(e.message)?e.message:()=>e.message}:null);return t.appContext=o,H(t,n),(e=>{let n=document.body;return e.appendTo&&($(e.appendTo)&&(n=document.querySelector(e.appendTo)),W(e.appendTo)&&(n=e.appendTo),W(n)||(n=document.body)),n})(e).appendChild(n.firstElementChild),t.component},fe=(e,n)=>{const o=document.createElement("div");e.onVanish=()=>{H(null,o),de.delete(a)},e.onAction=n=>{const o=de.get(a);let s;s=e.showInput?{value:a.inputValue,action:n}:n,e.callback?e.callback(s,t.proxy):"cancel"===n||"close"===n?e.distinguishCancelAndClose&&"cancel"!==n?o.reject("close"):o.reject("cancel"):o.resolve(s)};const t=pe(e,o,n),a=t.proxy;for(const s in e)K(e,s)&&!K(a.$props,s)&&(a[s]=e[s]);return a.visible=!0,a};function me(e,n=null){if(!V)return Promise.reject();let o;return $(e)||O(e)?e={message:e}:o=e.callback,new Promise(((t,a)=>{const s=fe(e,null!=n?n:me._context);de.set(s,{options:e,callback:o,resolve:t,reject:a})}))}const ve={alert:{closeOnPressEscape:!1,closeOnClickModal:!1},confirm:{showCancelButton:!0},prompt:{showCancelButton:!0,showInput:!0}};["alert","confirm","prompt"].forEach((e=>{me[e]=function(e){return(n,o,t,a)=>{let s="";return q(o)?(t=o,s=""):s=D(o)?"":o,me(Object.assign({title:s,message:n,type:"",...ve[e]},t,{boxType:e}),a)}}(e)})),me.close=()=>{de.forEach(((e,n)=>{n.doClose()})),de.clear()},me._context=null;const ge=me;ge.install=e=>{ge._context=e._context,e.config.globalProperties.$msgbox=ge,e.config.globalProperties.$messageBox=ge,e.config.globalProperties.$alert=ge.alert,e.config.globalProperties.$confirm=ge.confirm,e.config.globalProperties.$prompt=ge.prompt};const be=ge;export{be as E};
