webpackJsonp([4],{"UTF+":function(t,a){},jgdz:function(t,a,e){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var s=e("OoUZ"),i={template:"#tpl",data:function(){return{title:"",date:"",html:"",tags:[],blogimg:""}},created:function(){var t=this,a=this.$route.params.id;Object(s.f)(a).then(function(a){if(0===a.data.code){var e=a.data.data;t.blogimg=e.image,t.tags=e.tags,t.title=e.title,t.date=e.created_at,Object(s.h)(e.path).then(function(a){t.html=a.data,document.body.className="fixme"})}})}},n={render:function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"blog-main"},[e("div",{staticClass:"html",attrs:{id:"html"},domProps:{innerHTML:t._s(t.html)}}),t._v(" "),e("div",{staticClass:"blog-main-footer"},[t._l(t.tags,function(a){return e("el-tag",{key:a,staticClass:"tag",attrs:{type:"success"}},[t._v(t._s(a))])}),t._v(" "),e("h4",{staticClass:"date"},[t._v(t._s(t.date))])],2)])},staticRenderFns:[]};var l=e("VU/8")(i,n,!1,function(t){e("UTF+")},null,null);a.default=l.exports}});
//# sourceMappingURL=4.fd561ad54b9a36399268.js.map