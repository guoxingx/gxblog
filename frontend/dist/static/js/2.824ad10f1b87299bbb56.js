webpackJsonp([2],{GvzG:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=s("OoUZ"),n=s("fIeu"),o={name:"blog_list",components:{"boe-list-cell":function(){return s.e(8).then(s.bind(null,"+spj"))},account:function(){return s.e(10).then(s.bind(null,"2get"))},"boe-bets":function(){return s.e(9).then(s.bind(null,"CQ7M"))}},beforeRouteUpdate:function(e,t,s){if(e.params.id!==this.boe.id)for(var a in this.boe_list)this.boe_list[a].id===e.params.id&&(this.boe=this.boe_list[a],this.getBetList());s()},data:function(){return{boes_count:0,boe_list:[],boe:{},betList:[],visible0:!1,visible1:!1,visible2:!1,balance:0,account:Object(n.a)(),nodeStatus:-1,nodeStatusString:"unknown",peerCount:0}},created:function(){this.refresh()},methods:{bet:function(e){var t=this;if(0===this.nodeStatus){if(this.betCheck())return;Object(a.a)(this.boe.id,e,this.amount,Object(n.a)(),this.password).then(function(s){200===s.status?t.betResponse(s.data.code):t.$message({message:"下注失败:(",type:"warning"}),0===e&&(t.visible0=!1),1===e&&(t.visible1=!1),2===e&&(t.visible2=!1)})}else this.$message({message:"节点暂不可用，请等待 / 点击刷新",type:"warning"})},betCheck:function(){if(this.boe.ended)return this.$message({message:"该轮游戏已结束",type:"warning"}),1;var e=Object(n.a)();return this.boe.id?this.amount?e?this.password?0:(this.$message({message:"密码未填写",type:"warning"}),1):(this.$message({message:"账号未找到",type:"warning"}),1):(this.$message({message:"金额未填写",type:"warning"}),1):(this.$message({message:"id未找到",type:"warning"}),1)},betResponse:function(e){0===e?this.$message({message:"下注成功！请等待数据写入区块...",type:"success"}):30001===e?this.$message({message:"操作过于频繁，15秒后重试",type:"warning"}):1===e?this.$message({message:"密码错误",type:"warning"}):this.$message({message:"下注过大，庄家保证金不足！",type:"warning"})},getBetList:function(){var e=this;Object(n.a)()&&Object(a.d)(this.boe.id,Object(n.a)()).then(function(t){if(200===t.status){var s=[],a=t.data.data;for(var n in a){var o=a[n];s.push({beton:o[0],amount:Math.round(o[1]/1e15),odds:o[2]/1e3,profit:Math.round(o[3]/1e15),withdrawed:o[4]})}e.betList=s}})},refreshNodeStatus:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]&&arguments[0];Object(a.i)().then(function(s){if(200===s.status){var a=s.data.data;e.nodeStatus=a.status,e.nodeStatusString=a.message,e.peerCount=a.peer_count,t&&e.$message({message:"状态刷新成功",type:"success"})}})},refresh:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]&&arguments[0],s=this.$route.params.id;this.refreshNodeStatus(),Object(a.e)().then(function(a){if(200===a.status&&0===a.data.code){var n=a.data.data;for(var o in n)n[o].id===Number(s)&&(e.boe=n[o]);e.boe.id||(e.boe=n[0]),e.boes_count=n.length,e.boe_list=n,e.getBetList(),t&&e.$message({message:"刷新成功",type:"success"})}}),this.account=Object(n.a)(),this.account&&Object(a.c)(this.account).then(function(t){200===t.status&&(e.balance=Math.round(t.data.data/1e15))})}}},i={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("el-row",[s("el-col",{staticClass:"right",staticStyle:{float:"right"},attrs:{xs:24,sm:24,md:24,lg:5,xl:8}},[s("div",{staticClass:"status"},[s("el-button",{attrs:{type:0===e.nodeStatus?"success":"danger",round:""},on:{click:function(t){e.refreshNodeStatus(!0)}}},[e._v("\n        当前状态: "+e._s(e.nodeStatusString)+"\n      ")])],1),e._v(" "),s("div",{staticClass:"status"},[s("el-button",{attrs:{type:0===e.nodeStatus?"success":"danger",round:""},on:{click:function(t){e.refreshNodeStatus(!0)}}},[e._v("\n        连接节点数: "+e._s(e.peerCount)+"\n      ")])],1)]),e._v(" "),s("el-col",{attrs:{xs:24,sm:6,md:6,lg:5,xl:4}},[s("div",{staticClass:"left"},[s("h1",[e._v("BetOnEther")]),e._v(" "),s("h2",[e._v("基于以太坊测试链")]),e._v(" "),s("account",{attrs:{balance:e.balance,account:e.account,nodeStatus:e.nodeStatus}}),e._v(" "),s("div",{staticClass:"list"},e._l(e.boe_list,function(e){return s("boe-list-cell",{key:e,attrs:{boe:e}})}))],1)]),e._v(" "),e.boe.id?e._e():s("el-col",{staticClass:"board",attrs:{xs:24,sm:18,md:16,lg:14,xl:12}},[s("h2",[e._v("未选择比赛")])]),e._v(" "),e.boe.id?s("el-col",{staticClass:"board",attrs:{xs:24,sm:18,md:16,lg:14,xl:12}},[s("h2",[e._v(e._s(e.boe.league)+" round "+e._s(e.boe.round))]),e._v(" "),s("h4",{style:e.boe.ended?"color: #E6A23C;":"color: #409EFF;"},[e._v("\n      "+e._s(e.boe.ended?"已结束":"进行中")+"\n    ")]),e._v(" "),s("el-button",{attrs:{type:"primary",round:""},on:{click:function(t){e.refresh(!0)}}},[e._v("点我刷新")]),e._v(" "),s("el-row",[s("el-col",{attrs:{span:11}},[s("div",{staticClass:"team"},[s("img",{attrs:{src:e.boe.home_image}}),s("h4",[e._v(e._s(e.boe.home))])])]),e._v(" "),s("el-col",{staticClass:"vs",attrs:{span:2}},[s("h3",[e._v("vs")])]),e._v(" "),s("el-col",{attrs:{span:11}},[s("div",{staticClass:"team",attrs:{xs:12}},[s("img",{attrs:{src:e.boe.visiting_image}}),s("h4",[e._v(e._s(e.boe.visiting))])])])],1),e._v(" "),s("el-row",{attrs:{gutter:12}},[s("el-col",{attrs:{span:6,offset:3}},[s("h5",[e._v("主胜")]),e._v(" "),s("el-card",{class:{result:0===e.boe.result},attrs:{shadow:"hover"}},[s("el-button",{directives:[{name:"popover",rawName:"v-popover:beton0",arg:"beton0"}],attrs:{type:"text"}},[e._v("\n            "+e._s(e.boe.win_odds/1e3||0)+"\n          ")])],1)],1),e._v(" "),s("el-col",{attrs:{span:6,offset:0}},[s("h5",[e._v("平局")]),e._v(" "),s("el-card",{class:{result:1===e.boe.result},attrs:{shadow:"hover"}},[s("el-button",{directives:[{name:"popover",rawName:"v-popover:beton1",arg:"beton1"}],attrs:{type:"text"}},[e._v("\n            "+e._s(e.boe.draw_odds/1e3||0)+"\n          ")])],1)],1),e._v(" "),s("el-col",{attrs:{span:6,offset:0}},[s("h5",[e._v("客胜")]),e._v(" "),s("el-card",{class:{result:2===e.boe.result},attrs:{shadow:"hover"}},[s("el-button",{directives:[{name:"popover",rawName:"v-popover:beton2",arg:"beton2"}],attrs:{type:"text"}},[e._v("\n            "+e._s(e.boe.lose_odds/1e3||0)+"\n          ")])],1)],1)],1),e._v(" "),s("el-popover",{ref:"beton0",attrs:{placement:"top",width:"260"},model:{value:e.visible0,callback:function(t){e.visible0=t},expression:"visible0"}},[s("el-row",[s("el-col",{attrs:{span:20}},[s("el-input",{attrs:{type:"number",placeholder:"输入金额(finney)"},model:{value:e.amount,callback:function(t){e.amount=t},expression:"amount"}}),e._v(" "),s("el-input",{attrs:{type:"password",placeholder:"输入密码"},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}})],1),e._v(" "),s("el-col",{attrs:{span:3,offset:1}},[s("el-button",{attrs:{type:"Blue",icon:"el-icon-check",circle:""},on:{click:function(t){e.bet(0)}}})],1)],1)],1),e._v(" "),s("el-popover",{ref:"beton1",attrs:{placement:"top",width:"260"},model:{value:e.visible1,callback:function(t){e.visible1=t},expression:"visible1"}},[s("el-row",[s("el-col",{attrs:{span:20}},[s("el-input",{attrs:{type:"number",placeholder:"输入金额(finney)"},model:{value:e.amount,callback:function(t){e.amount=t},expression:"amount"}}),e._v(" "),s("el-input",{attrs:{type:"password",placeholder:"输入密码"},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}})],1),e._v(" "),s("el-col",{attrs:{span:3,offset:1}},[s("el-button",{attrs:{type:"Blue",icon:"el-icon-check",circle:""},on:{click:function(t){e.bet(1)}}})],1)],1)],1),e._v(" "),s("el-popover",{ref:"beton2",attrs:{placement:"top",width:"260"},model:{value:e.visible2,callback:function(t){e.visible2=t},expression:"visible2"}},[s("el-row",[s("el-col",{attrs:{span:20}},[s("el-input",{attrs:{type:"number",placeholder:"输入金额(finney)"},model:{value:e.amount,callback:function(t){e.amount=t},expression:"amount"}}),e._v(" "),s("el-input",{attrs:{type:"password",placeholder:"输入密码"},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}})],1),e._v(" "),s("el-col",{attrs:{span:3,offset:1}},[s("el-button",{attrs:{type:"Blue",icon:"el-icon-check",circle:""},on:{click:function(t){e.bet(2)}}})],1)],1)],1),e._v(" "),s("el-col",{attrs:{span:18,offset:3}},[s("keep-alive",[s("boe-bets",{staticStyle:{"margin-top":"20px"},attrs:{boe:this.boe,betList:this.betList,account:this.account,nodeStatus:e.nodeStatus}})],1)],1),e._v(" "),s("el-col",{attrs:{span:18,offset:3}},[s("p",[e._v("注：只有在交易被区块写入之后，下注 / 提现 / 余额更新 等接口才算正式完成")]),e._v(" "),s("p",[e._v('因为作者很懒 ...请好好利用"刷新"按钮。'),s("strong",[e._v("暂时的")])])])],1):e._e()],1)},staticRenderFns:[]};var r=s("VU/8")(o,i,!1,function(e){s("VbGO")},null,null);t.default=r.exports},VbGO:function(e,t){},fIeu:function(e,t,s){"use strict";t.a=function(){return function(e){for(var t=document.cookie.split(";"),s=0;s<t.length;s++){var a=t[s].trim();if(0===a.indexOf(e)){var o=a.split("=")[1];return o&&o.length>0&&n(e,o),o}}return null}(a)},t.c=function(e){n(a,e)},t.b=function(){e=a,document.cookie=e+"=; expires=Thu, 01 Jan 1970 00:00:00 GMT";var e};var a="testguoxingethaccount";function n(e,t){var s=new Date;s.setTime(s.getTime()+21859200);var a="expires="+s.toGMTString();document.cookie=e+"="+t+"; "+a}}});
//# sourceMappingURL=2.824ad10f1b87299bbb56.js.map