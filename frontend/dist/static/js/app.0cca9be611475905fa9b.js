webpackJsonp([6],{NHnr:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=n("7+uW"),i={name:"App",components:{gFooter:function(){return n.e(4).then(n.bind(null,"mzkE"))}},methods:{toblogs:function(){this.$router.push({name:"index"})},toboe:function(){this.$router.push({name:"betonether",params:{id:0}})},togithub:function(){window.location.href="https://github.com/guoxingx"}}},a={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{attrs:{id:"app"}},[n("el-menu",{staticClass:"el-menu-demo",attrs:{mode:"horizontal"},on:{select:e.handleSelect}},[n("el-menu-item",{attrs:{index:"1"},on:{click:function(t){e.toblogs()}}},[e._v("blogs")]),e._v(" "),n("el-menu-item",{attrs:{index:"2"},on:{click:function(t){e.toboe()}}},[e._v("betonether")]),e._v(" "),n("el-menu-item",{attrs:{index:"3"},on:{click:function(t){e.togithub()}}},[e._v("my github")])],1),e._v(" "),n("div",{staticClass:"main"},[n("router-view")],1)],1)},staticRenderFns:[]};var l=n("VU/8")(i,a,!1,function(e){n("gwwX")},null,null).exports,u=n("/ocq");o.default.use(u.a);var r=new u.a({routes:[{path:"/",name:"index",redirect:"/blogs"},{path:"/blogs",name:"blogs",component:function(e){Promise.all([n.e(0),n.e(1)]).then(function(){var t=[n("oMF7")];e.apply(null,t)}.bind(this)).catch(n.oe)},meta:{title:"gxblog"}},{path:"/blogs/:id",name:"blog",component:function(e){Promise.all([n.e(0),n.e(3)]).then(function(){var t=[n("jgdz")];e.apply(null,t)}.bind(this)).catch(n.oe)},meta:{title:"gxblog"}},{path:"/betonether/:id",name:"betonether",component:function(e){Promise.all([n.e(0),n.e(2)]).then(function(){var t=[n("GvzG")];e.apply(null,t)}.bind(this)).catch(n.oe)},meta:{title:"gxblog-betonether"}}]}),c=n("zL8q"),s=n.n(c),m=(n("tvR6"),n("WiKS")),p=n.n(m);o.default.config.productionTip=!1,o.default.use(s.a),o.default.component("vue-headful",p.a),new o.default({el:"#app",router:r,components:{App:l},template:"<App/>",render:function(e){return e(l)}})},gwwX:function(e,t){},tvR6:function(e,t){}},["NHnr"]);
//# sourceMappingURL=app.0cca9be611475905fa9b.js.map