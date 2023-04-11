import{_ as e}from"./ContentWrap.vue_vue_type_script_setup_true_lang-e04d0b7e.js";import{J as a,K as t,L as s,M as n,N as i,d as o,O as l,P as u,Q as r,R as c,S as d,r as m,U as f,V as p,H as v,W as g,X as b,s as k,o as w,g as h,f as _,w as x,e as y,n as I,a as C,Y as z,Z as O,A as j,_ as T,$ as N,c as L,F as A,a0 as R,a1 as V,a2 as E,a3 as X,a4 as Y,a5 as B,a6 as D,G as M,y as $,z as F,a7 as W,h as S,a8 as P,a9 as G,aa as H,ab as Z,ac as J,ad as K,ae as Q,af as U,ag as q,ah as ee,j as ae,m as te,t as se}from"./index-61faf58b.js";import{u as ne}from"./index-7630a328.js";import{d as ie}from"./debounce-7bd0410d.js";import{E as oe}from"./el-button-e6441f40.js";import"./el-card-839bb50e.js";import"./el-popper-e10402a6.js";import"./index-f844f20d.js";function le(e,t,s){var n=!0,i=!0;if("function"!=typeof e)throw new TypeError("Expected a function");return a(s)&&(n="leading"in s?!!s.leading:n,i="trailing"in s?!!s.trailing:i),ie(e,t,{leading:n,maxWait:t,trailing:i})}const ue=t({urlList:{type:s(Array),default:()=>n([])},zIndex:{type:Number},initialIndex:{type:Number,default:0},infinite:{type:Boolean,default:!0},hideOnClickModal:{type:Boolean,default:!1},teleported:{type:Boolean,default:!1},closeOnPressEscape:{type:Boolean,default:!0},zoomRate:{type:Number,default:1.2}}),re={close:()=>!0,switch:e=>i(e)},ce=["src"],de=o({name:"ElImageViewer"});const me=K(G(o({...de,props:ue,emits:re,setup(e,{expose:a,emit:t}){const s=e,n={CONTAIN:{name:"contain",icon:l(u)},ORIGINAL:{name:"original",icon:l(r)}},{t:o}=ne(),G=c("image-viewer"),{nextZIndex:K}=d(),Q=m(),U=m([]),q=f(),ee=m(!0),ae=m(s.initialIndex),te=p(n.CONTAIN),se=m({scale:1,deg:0,offsetX:0,offsetY:0,enableTransition:!1}),ie=v((()=>{const{urlList:e}=s;return e.length<=1})),oe=v((()=>0===ae.value)),ue=v((()=>ae.value===s.urlList.length-1)),re=v((()=>s.urlList[ae.value])),de=v((()=>{const{scale:e,deg:a,offsetX:t,offsetY:s,enableTransition:i}=se.value;let o=t/e,l=s/e;switch(a%360){case 90:case-270:[o,l]=[l,-o];break;case 180:case-180:[o,l]=[-o,-l];break;case 270:case-90:[o,l]=[-l,o]}const u={transform:`scale(${e}) rotate(${a}deg) translate(${o}px, ${l}px)`,transition:i?"transform .3s":""};return te.value.name===n.CONTAIN.name&&(u.maxWidth=u.maxHeight="100%"),u})),me=v((()=>i(s.zIndex)?s.zIndex:K()));function fe(){q.stop(),t("close")}function pe(){ee.value=!1}function ve(e){ee.value=!1,e.target.alt=o("el.image.error")}function ge(e){if(ee.value||0!==e.button||!Q.value)return;se.value.enableTransition=!1;const{offsetX:a,offsetY:t}=se.value,s=e.pageX,n=e.pageY,i=le((e=>{se.value={...se.value,offsetX:a+e.pageX-s,offsetY:t+e.pageY-n}})),o=H(document,"mousemove",i);H(document,"mouseup",(()=>{o()})),e.preventDefault()}function be(){se.value={scale:1,deg:0,offsetX:0,offsetY:0,enableTransition:!1}}function ke(){if(ee.value)return;const e=J(n),a=Object.values(n),t=te.value.name,s=(a.findIndex((e=>e.name===t))+1)%e.length;te.value=n[e[s]],be()}function we(e){const a=s.urlList.length;ae.value=(e+a)%a}function he(){oe.value&&!s.infinite||we(ae.value-1)}function _e(){ue.value&&!s.infinite||we(ae.value+1)}function xe(e,a={}){if(ee.value)return;const{zoomRate:t,rotateDeg:n,enableTransition:i}={zoomRate:s.zoomRate,rotateDeg:90,enableTransition:!0,...a};switch(e){case"zoomOut":se.value.scale>.2&&(se.value.scale=Number.parseFloat((se.value.scale/t).toFixed(3)));break;case"zoomIn":se.value.scale<7&&(se.value.scale=Number.parseFloat((se.value.scale*t).toFixed(3)));break;case"clockwise":se.value.deg+=n;break;case"anticlockwise":se.value.deg-=n}se.value.enableTransition=i}return g(re,(()=>{b((()=>{const e=U.value[0];(null==e?void 0:e.complete)||(ee.value=!0)}))})),g(ae,(e=>{be(),t("switch",e)})),k((()=>{var e,a;!function(){const e=le((e=>{switch(e.code){case Z.esc:s.closeOnPressEscape&&fe();break;case Z.space:ke();break;case Z.left:he();break;case Z.up:xe("zoomIn");break;case Z.right:_e();break;case Z.down:xe("zoomOut")}})),a=le((e=>{xe((e.deltaY||e.deltaX)<0?"zoomIn":"zoomOut",{zoomRate:s.zoomRate,enableTransition:!1})}));q.run((()=>{H(document,"keydown",e),H(document,"wheel",a)}))}(),null==(a=null==(e=Q.value)?void 0:e.focus)||a.call(e)})),a({setActiveItem:we}),(e,a)=>(w(),h(P,{to:"body",disabled:!e.teleported},[_(S,{name:"viewer-fade",appear:""},{default:x((()=>[y("div",{ref_key:"wrapper",ref:Q,tabindex:-1,class:I(C(G).e("wrapper")),style:z({zIndex:C(me)})},[y("div",{class:I(C(G).e("mask")),onClick:a[0]||(a[0]=O((a=>e.hideOnClickModal&&fe()),["self"]))},null,2),j(" CLOSE "),y("span",{class:I([C(G).e("btn"),C(G).e("close")]),onClick:fe},[_(C(T),null,{default:x((()=>[_(C(N))])),_:1})],2),j(" ARROW "),C(ie)?j("v-if",!0):(w(),L(A,{key:0},[y("span",{class:I([C(G).e("btn"),C(G).e("prev"),C(G).is("disabled",!e.infinite&&C(oe))]),onClick:he},[_(C(T),null,{default:x((()=>[_(C(R))])),_:1})],2),y("span",{class:I([C(G).e("btn"),C(G).e("next"),C(G).is("disabled",!e.infinite&&C(ue))]),onClick:_e},[_(C(T),null,{default:x((()=>[_(C(V))])),_:1})],2)],64)),j(" ACTIONS "),y("div",{class:I([C(G).e("btn"),C(G).e("actions")])},[y("div",{class:I(C(G).e("actions__inner"))},[_(C(T),{onClick:a[1]||(a[1]=e=>xe("zoomOut"))},{default:x((()=>[_(C(E))])),_:1}),_(C(T),{onClick:a[2]||(a[2]=e=>xe("zoomIn"))},{default:x((()=>[_(C(X))])),_:1}),y("i",{class:I(C(G).e("actions__divider"))},null,2),_(C(T),{onClick:ke},{default:x((()=>[(w(),h(Y(C(te).icon)))])),_:1}),y("i",{class:I(C(G).e("actions__divider"))},null,2),_(C(T),{onClick:a[3]||(a[3]=e=>xe("anticlockwise"))},{default:x((()=>[_(C(B))])),_:1}),_(C(T),{onClick:a[4]||(a[4]=e=>xe("clockwise"))},{default:x((()=>[_(C(D))])),_:1})],2)],2),j(" CANVAS "),y("div",{class:I(C(G).e("canvas"))},[(w(!0),L(A,null,M(e.urlList,((e,a)=>$((w(),L("img",{ref_for:!0,ref:e=>U.value[a]=e,key:e,src:e,style:z(C(de)),class:I(C(G).e("img")),onLoad:pe,onError:ve,onMousedown:ge},null,46,ce)),[[F,a===ae.value]]))),128))],2),W(e.$slots,"default")],6)])),_:3})],8,["disabled"]))}}),[["__file","/home/runner/work/element-plus/element-plus/packages/components/image-viewer/src/image-viewer.vue"]])),fe=o({__name:"ImageViewer",props:{urlList:{type:Array,default:()=>[]},zIndex:Q.number.def(200),initialIndex:Q.number.def(0),infinite:Q.bool.def(!0),hideOnClickModal:Q.bool.def(!1),appendToBody:Q.bool.def(!1),show:Q.bool.def(!1)},setup(e){const a=e,t=v((()=>{const e={...a};return delete e.show,e})),s=m(a.show),n=()=>{s.value=!1};return(e,a)=>s.value?(w(),h(C(me),U({key:0},C(t),{onClose:n}),null,16)):j("",!0)}});let pe=null;const ve=o({__name:"ImageViewer",setup(a){const{t:t}=ae(),s=()=>{!function(e){if(!q)return;const{urlList:a,initialIndex:t=0,infinite:s=!0,hideOnClickModal:n=!1,appendToBody:i=!1,zIndex:o=2e3,show:l=!0}=e,u={},r=document.createElement("div");u.urlList=a,u.initialIndex=t,u.infinite=s,u.hideOnClickModal=n,u.appendToBody=i,u.zIndex=o,u.show=l,document.body.appendChild(r),pe=_(fe,u),ee(pe,r)}({urlList:["https://img1.baidu.com/it/u=657828739,1486746195&fm=26&fmt=auto&gp=0.jpg","https://img0.baidu.com/it/u=3114228356,677481409&fm=26&fmt=auto&gp=0.jpg","https://img1.baidu.com/it/u=508846955,3814747122&fm=26&fmt=auto&gp=0.jpg","https://img1.baidu.com/it/u=3536647690,3616605490&fm=26&fmt=auto&gp=0.jpg","https://img1.baidu.com/it/u=4087287201,1148061266&fm=26&fmt=auto&gp=0.jpg","https://img2.baidu.com/it/u=3429163260,2974496379&fm=26&fmt=auto&gp=0.jpg"]})};return(a,n)=>(w(),h(C(e),{title:C(t)("imageViewerDemo.imageViewer"),message:C(t)("imageViewerDemo.imageViewerDes")},{default:x((()=>[_(C(oe),{type:"primary",onClick:s},{default:x((()=>[te(se(C(t)("imageViewerDemo.open")),1)])),_:1})])),_:1},8,["title","message"]))}});export{ve as default};