webpackJsonp([6],{NHnr:function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var o=t("7+uW"),i={name:"App",components:{gFooter:function(){return t.e(4).then(t.bind(null,"mzkE"))}},methods:{toblogs:function(){this.$router.push({name:"index"})},toboe:function(){this.$router.push({name:"betonether",params:{id:0}})},togithub:function(){window.location.href="https://github.com/guoxingx"}}},a={render:function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{attrs:{id:"app"}},[t("el-menu",{staticClass:"el-menu-demo",attrs:{mode:"horizontal"},on:{select:e.handleSelect}},[t("el-menu-item",{attrs:{index:"1"},on:{click:function(n){e.toblogs()}}},[e._v("blogs")]),e._v(" "),t("el-menu-item",{attrs:{index:"2"},on:{click:function(n){e.toboe()}}},[e._v("betonether")]),e._v(" "),t("el-menu-item",{attrs:{index:"3"},on:{click:function(n){e.togithub()}}},[e._v("my github")])],1),e._v(" "),t("div",{staticClass:"main"},[t("router-view")],1)],1)},staticRenderFns:[]};var u=t("VU/8")(i,a,!1,function(e){t("gwwX")},null,null).exports,l=t("/ocq");o.default.use(l.a);var c=new l.a({routes:[{path:"/",name:"index",redirect:"/blogs"},{path:"/blogs",name:"blogs",component:function(e){Promise.all([t.e(0),t.e(1)]).then(function(){var n=[t("oMF7")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/blogs/:id",name:"blog",component:function(e){Promise.all([t.e(0),t.e(3)]).then(function(){var n=[t("jgdz")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/betonether/:id",name:"betonether",component:function(e){Promise.all([t.e(0),t.e(2)]).then(function(){var n=[t("GvzG")];e.apply(null,n)}.bind(this)).catch(t.oe)}}]}),r=t("zL8q"),s=t.n(r),p=(t("tvR6"),t("WiKS")),d=t.n(p);o.default.config.productionTip=!1,o.default.use(s.a),o.default.component("vue-headful",d.a),new o.default({el:"#app",router:c,components:{App:u},template:"<App/>",render:function(e){return e(u)}})},gwwX:function(e,n){},tvR6:function(e,n){}},["NHnr"]);
//# sourceMappingURL=app.3c77594e9e7ef7c1e394.js.map