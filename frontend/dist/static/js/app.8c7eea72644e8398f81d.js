webpackJsonp([6],{NHnr:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var o=n("7+uW"),i={name:"App",components:{gFooter:function(){return n.e(3).then(n.bind(null,"mzkE"))}},methods:{toblogs:function(){this.$router.push({name:"index"})},toboe:function(){this.$router.push({name:"betonether",params:{id:0}})},togithub:function(){window.location.href="https://github.com/guoxingx"}}},a={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"app"}},[n("el-menu",{staticStyle:{position:"fixed",top:"0",width:"100%","margin-top":"10px","margin-right":"10px","z-index":"1234",opacity:"0.95"},attrs:{mode:"horizontal"},on:{select:t.handleSelect}},[n("el-menu-item",{attrs:{index:"1"},on:{click:function(e){t.toblogs()}}},[t._v("blogs")]),t._v(" "),n("el-menu-item",{attrs:{index:"2"},on:{click:function(e){t.toboe()}}},[t._v("betonether")]),t._v(" "),n("el-menu-item",{attrs:{index:"3"},on:{click:function(e){t.togithub()}}},[t._v("my github")])],1),t._v(" "),n("div",{staticClass:"main",staticStyle:{"margin-top":"60px","border-radius":"10px","min-height":"620px"}},[n("router-view")],1)],1)},staticRenderFns:[]};var r=n("VU/8")(i,a,!1,function(t){n("jYV/")},null,null).exports,u=n("/ocq");o.default.use(u.a);var c=new u.a({routes:[{path:"/",name:"index",redirect:"/blogs"},{path:"/blogs",name:"blogs",component:function(t){Promise.all([n.e(0),n.e(4)]).then(function(){var e=[n("oMF7")];t.apply(null,e)}.bind(this)).catch(n.oe)}},{path:"/blogs/:id",name:"blog",component:function(t){Promise.all([n.e(0),n.e(1)]).then(function(){var e=[n("jgdz")];t.apply(null,e)}.bind(this)).catch(n.oe)}},{path:"/betonether/:id",name:"betonether",component:function(t){Promise.all([n.e(0),n.e(2)]).then(function(){var e=[n("GvzG")];t.apply(null,e)}.bind(this)).catch(n.oe)}}]}),l=n("zL8q"),s=n.n(l);n("tvR6");o.default.config.productionTip=!1,o.default.use(s.a),new o.default({el:"#app",router:c,components:{App:r},template:"<App/>",render:function(t){return t(r)}})},"jYV/":function(t,e){},tvR6:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.8c7eea72644e8398f81d.js.map