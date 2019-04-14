(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{33:function(e,t,n){e.exports=n(67)},66:function(e,t,n){},67:function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),c=n(16),o=n.n(c),l=n(3),s=n(4),i=n(8),u=n(5),d=n(7),h=n(1),m=n(14),p=n.n(m),f=n(9),y=n.n(f),b=function(e){function t(){return Object(l.a)(this,t),Object(i.a)(this,Object(u.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(s.a)(t,[{key:"render",value:function(){return r.a.createElement(y.a,{open:this.props.open},r.a.createElement(f.DialogTitle,null,"Add Course"),r.a.createElement(f.DialogContent,null),r.a.createElement(f.DialogFooter,null,r.a.createElement(f.DialogButton,{action:"dismiss"},"Dismiss"),r.a.createElement(f.DialogButton,{action:"accept",isDefault:!0},"Accept")))}}]),t}(a.Component),v=function(e){function t(){return Object(l.a)(this,t),Object(i.a)(this,Object(u.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(s.a)(t,[{key:"render",value:function(){return r.a.createElement(y.a,{open:this.props.open},r.a.createElement(f.DialogTitle,null,"Add Schedule"),r.a.createElement(f.DialogContent,null),r.a.createElement(f.DialogFooter,null,r.a.createElement(f.DialogButton,{action:"dismiss"},"Dismiss"),r.a.createElement(f.DialogButton,{action:"accept",isDefault:!0},"Accept")))}}]),t}(a.Component),E=n(20),g=n(10),O=n.n(g),C=n(27),k=n.n(C),S=n(17),j=n.n(S),w=n(28),D=n.n(w),N=n(29),_="ADD_SECTION",x="REMOVE_SECTION",T="ADD_COURSE",A="REMOVE_COURSE",I="ADD_SCHEDULE",L="REMOVE_SCHEDULE",M="SELECT_SCHEDULE",B="LOAD_SCHEDULES";var H=n(6),F={A:"#00BCD4",B:"#A5D6A7",C:"#FFEE58",D:"#E57373",F:"#90A4AE",Q:"#D1C4E9"},R=function(e){var t=e.historical_performance;if(null===t.A)return r.a.createElement("div",null);var n=[],a=0;for(var c in F){var o=t[c];a+=o||0}for(var l in F){var s=t[l];s&&n.push(r.a.createElement("div",{key:l,style:{backgroundColor:F[l],width:"".concat((s/a*100-.1).toFixed(2),"%"),display:"inline-block",border:"1px solid white",boxSizing:"border-box",height:20}}))}return r.a.createElement("div",{style:{width:"40%",marginLeft:"auto"}},n)},U=function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(i.a)(this,Object(u.a)(t).call(this,e))).checkboxClickHandler=n.checkboxClickHandler.bind(Object(h.a)(Object(h.a)(n))),n.isChecked=n.isChecked.bind(Object(h.a)(Object(h.a)(n))),n.checkboxClickHandler=n.checkboxClickHandler.bind(Object(h.a)(Object(h.a)(n))),n}return Object(d.a)(t,e),Object(s.a)(t,[{key:"isChecked",value:function(){return!!this.props.selectedCrns&&this.props.selectedCrns.has(this.props.section.crn)}},{key:"checkboxClickHandler",value:function(){this.isChecked()?this.props.removeSection(this.props.section.crn):this.props.addSection(this.props.section.crn)}},{key:"render",value:function(){var e=this.props.section,t=e.section_num,n=e.instructor,a=e.historical_performance;return r.a.createElement(g.ListItem,null,r.a.createElement(N.Checkbox,{initRipple:function(){},checked:this.isChecked(),onChange:this.checkboxClickHandler}),r.a.createElement(g.ListItemText,{primaryText:t,secondaryText:n}),r.a.createElement(g.ListItemGraphic,{graphic:r.a.createElement(R,{historical_performance:a})}))}}]),t}(r.a.Component),W=Object(H.b)(function(e){var t=new Set;if(e.currScheduleName){var n=e.schedules.get(e.currScheduleName);n&&(t=n.selectedCrns)}return{selectedCrns:t}},function(e){return{addSection:function(t){return e(function(e){return{type:_,payload:e}}(t))},removeSection:function(t){return e(function(e){return{type:x,payload:e}}(t))}}})(U),z=function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(i.a)(this,Object(u.a)(t).call(this,e))).state={checked:!1,indeterminate:!1},n.handleDeleteClick=n.handleDeleteClick.bind(Object(h.a)(Object(h.a)(n))),n}return Object(d.a)(t,e),Object(s.a)(t,[{key:"handleDeleteClick",value:function(){this.props.removeCourse(this.props.dept,this.props.course_num)}},{key:"render",value:function(){var e=r.a.createElement(g.ListItem,{className:"course-list-item"},r.a.createElement(g.ListItemText,{primaryText:"".concat(this.props.dept,"-").concat(this.props.course_num),secondaryText:this.props.name}),r.a.createElement(g.ListItemMeta,{meta:r.a.createElement(k.a,{onClick:this.handleDeleteClick},r.a.createElement(j.a,{icon:"delete"}))}));return r.a.createElement(D.a,{trigger:e,transitionTime:250},r.a.createElement(O.a,{twoLine:!0,className:"course-sections"},this.props.sections.map(function(e,t){var n=e.section;return r.a.createElement(W,{key:t,section:n})})))}}]),t}(r.a.Component),V=Object(H.b)(null,function(e){return{removeCourse:function(t,n){return e(function(e,t){return{type:A,payload:{dept:e,course_num:t}}}(t,n))}}})(z),G=function(e){function t(){return Object(l.a)(this,t),Object(i.a)(this,Object(u.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(s.a)(t,[{key:"render",value:function(){var e=[];for(var t in this.props.courses){var n=this.props.courses[t],a=n.dept,c=n.name,o=n.course_num,l=n.sections.map(function(e){return{section:e}});e.push(r.a.createElement(V,{key:"".concat(a,"-").concat(o),name:c,dept:a,course_num:o,sections:l}))}return r.a.createElement(O.a,{twoLine:!0,avatarList:!0},e)}}]),t}(r.a.Component),J=Object(H.b)(function(e){var t={};if(e.currScheduleName){var n=e.schedules.get(e.currScheduleName);n&&(t=Object(E.a)({},n.courses))}return{courses:t}})(G),Q=n(31),X=n.n(Q),$=n(32),q=n.n($),K=function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(i.a)(this,Object(u.a)(t).call(this,e))).handleSelectionChange=n.handleSelectionChange.bind(Object(h.a)(Object(h.a)(n))),n}return Object(d.a)(t,e),Object(s.a)(t,[{key:"componentDidMount",value:function(){this.props.currScheduleName||this.props.scheduleNames.length>0&&this.props.selectSchedule(this.props.scheduleNames[0])}},{key:"handleSelectionChange",value:function(e){e.target?this.props.selectSchedule(e.target.value):console.log("Event target is undefined?")}},{key:"render",value:function(){return 0===this.props.scheduleNames.length?null:r.a.createElement(q.a,{className:"schedule-select",onChange:this.handleSelectionChange,options:this.props.scheduleNames})}}]),t}(r.a.Component),P=Object(H.b)(function(e){return{currScheduleName:e.currScheduleName}},function(e){return{selectSchedule:function(t){return e(function(e){return{type:M,payload:e}}(t))}}})(K),Y=n(19),Z=n(13),ee=function(e){return r.a.createElement("div",{style:{position:"absolute",top:100*e.start+"%",height:100*e.duration+"%",width:"100%",borderRadius:3,background:"red"}},r.a.createElement(Z.Body1,null,e.displayText))},te=function(e){var t=e%1,n=e-t;if(t*=60,t=Math.round(t),n>24){Math.floor(n/24);n%=24}var a=new Date;a.setHours(n),a.setMinutes(t),a.setSeconds(0);a.toTimeString().split(" ")[0];return a.toTimeString().split(" ")[0]},ne=Object(H.b)(function(e){var t=[];if(e.currScheduleName){var n=e.schedules.get(e.currScheduleName);n&&n.selectedCrns.forEach(function(e){for(var a in n.courses){var r=!0,c=!1,o=void 0;try{for(var l,s=n.courses[a].sections[Symbol.iterator]();!(r=(l=s.next()).done);r=!0){var i=l.value;if(i.crn===e&&t.push(i),t.length===n.selectedCrns.size)return{sections:t}}}catch(u){c=!0,o=u}finally{try{r||null==s.return||s.return()}finally{if(c)throw o}}}})}return{sections:t}})(function(e){var t={M:[],T:[],W:[],R:[],F:[]},n=!0,a=!1,c=void 0;try{for(var o,l=e.sections[Symbol.iterator]();!(n=(o=l.next()).done);n=!0){var s=o.value,i=!0,u=!1,d=void 0;try{for(var h,m=s.meetings[Symbol.iterator]();!(i=(h=m.next()).done);i=!0){var p=h.value;if(p.start_time&&p.end_time&&p.meeting_days){console.log(p);var f=(p.start_time-420)/900;console.log("start time =",f);var y=(p.end_time-420)/900-f,b="".concat(s.dept,"-").concat(s.course_num,"-").concat(s.section_num),v=!0,E=!1,g=void 0;try{for(var O,C=p.meeting_days[Symbol.iterator]();!(v=(O=C.next()).done);v=!0)t[O.value].push(r.a.createElement(ee,{key:Math.random()*Number.MAX_SAFE_INTEGER,start:f,duration:y,displayText:b}))}catch(A){E=!0,g=A}finally{try{v||null==C.return||C.return()}finally{if(E)throw g}}}}}catch(A){u=!0,d=A}finally{try{i||null==m.return||m.return()}finally{if(u)throw d}}}}catch(A){a=!0,c=A}finally{try{n||null==l.return||l.return()}finally{if(a)throw c}}for(var k=[],S=0,j=[["Monday","M"],["Tuesday","T"],["Wednesday","W"],["Thursday","R"],["Friday","F"]];S<j.length;S++){var w=j[S],D=Object(Y.a)(w,2),N=D[0],_=D[1];k.push(r.a.createElement("div",{className:"day",key:_},r.a.createElement("strong",{className:"week-heading"},r.a.createElement(Z.Body1,null,N)),t[_]))}for(var x=[],T=0;T<=15;++T)x.push(r.a.createElement("tr",{className:"week-row",key:T},r.a.createElement("td",{style:{width:"20px",height:T?"auto":"36px",color:"grey",textAlign:"left",padding:"3px 10px 0 0",paddingLeft:10,borderBottom:"1px solid grey",verticalAlign:"top"}},r.a.createElement(Z.Body1,null,T?te(T+7-1):"")),r.a.createElement("td",{style:{borderBottom:"1px solid grey",boxSizing:"border-box"}})));return r.a.createElement("div",null,r.a.createElement("div",{className:"week-wrap"},r.a.createElement("div",{className:"week-container"},r.a.createElement("table",{className:"week-grid"},r.a.createElement("tbody",null,x)),r.a.createElement("div",{className:"days"},k))))}),ae=function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(i.a)(this,Object(u.a)(t).call(this,e))).state={addCourseDialogIsOpen:!1,addScheduleDialogIsOpen:!1},n.handleClick=n.handleClick.bind(Object(h.a)(Object(h.a)(n))),n}return Object(d.a)(t,e),Object(s.a)(t,[{key:"componentDidMount",value:function(){var e=this;fetch("/api/schedules/").then(function(e){return e.json()}).then(function(t){e.props.loadSchedules(t)}).catch(function(e){return console.log(e)})}},{key:"handleClick",value:function(e){this.props.anySchedulesCreated?this.setState({addCourseDialogIsOpen:!0}):this.setState({addScheduleDialogIsOpen:!0})}},{key:"render",value:function(){var e=this.props.schedules;return r.a.createElement("div",{className:"drawer-container"},r.a.createElement(p.a,{className:"drawer"},r.a.createElement(m.DrawerHeader,null,r.a.createElement(P,{scheduleNames:Array.from(e.keys())})),r.a.createElement(m.DrawerContent,{className:"drawer-content"},r.a.createElement(J,null))),r.a.createElement(m.DrawerAppContent,{className:"drawer-app-content"},r.a.createElement("div",{className:"week"},r.a.createElement(ne,null)),r.a.createElement(X.a,{className:"fab",icon:r.a.createElement(j.a,{icon:"add"}),onClick:this.handleClick})),r.a.createElement(v,{open:this.state.addScheduleDialogIsOpen}),r.a.createElement(b,{open:this.state.addCourseDialogIsOpen}))}}]),t}(a.Component),re=Object(H.b)(function(e){return{anySchedulesCreated:0!==Array.from(e.schedules.keys()).length,schedules:e.schedules,currScheduleName:e.currScheduleName}},function(e){return{loadSchedules:function(t){return e(function(e){return{type:B,payload:e}}(t))}}})(ae);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var ce=n(18),oe=(new Map,{schedules:new Map,currScheduleName:void 0}),le=function(e){console.log(e);var t=e.split(":").map(function(e){return Number.parseInt(e)}),n=Object(Y.a)(t,3),a=n[0],r=n[1],c=n[2];return console.log(60*a+r+c/60),60*a+r+c/60};n(56),n(57),n(58),n(59),n(60),n(61),n(62),n(63),n(64),n(65),n(66);var se=Object(ce.b)(function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:oe,t=arguments.length>1?arguments[1]:void 0;le("08:00:00");var n=Object(E.a)({},e),a=n.currScheduleName;if(t.type===M&&(n.currScheduleName=t.payload),a){var r=n.schedules.get(a);if(r)switch(t.type){case _:r.selectedCrns.add(t.payload);break;case x:r.selectedCrns.delete(t.payload);break;case T:r.courses["".concat(t.payload.dept,"-").concat(t.payload.course_num)]=t.payload;break;case A:var c=t.payload,o=c.dept,l=c.course_num;delete r.courses["".concat(o,"-").concat(l)],n.schedules.set(a,r);break;case L:n.schedules.delete(t.payload)}else{if(t.type!==I)throw Error("The schedule attempting to be accessed does not exist.");var s={name:t.payload.name,term_code:t.payload.term_code,courses:{},selectedCrns:new Set};n.schedules.set(t.payload.name,s)}}else if(t.type===B)for(var i in t.payload){var u=t.payload[i];for(var d in u.courses){var h=u.courses[d],m=!0,p=!1,f=void 0;try{for(var y,b=h.sections[Symbol.iterator]();!(m=(y=b.next()).done);m=!0){var v=y.value,g=!0,O=!1,C=void 0;try{for(var k,S=v.meetings[Symbol.iterator]();!(g=(k=S.next()).done);g=!0){var j=k.value;j.start_time&&(j.start_time=le(j.start_time)),j.end_time&&(j.end_time=le(j.end_time))}}catch(w){O=!0,C=w}finally{try{g||null==S.return||S.return()}finally{if(O)throw C}}}}catch(w){p=!0,f=w}finally{try{m||null==b.return||b.return()}finally{if(p)throw f}}}u.selectedCrns=new Set(u.sections.map(function(e){return Number.parseInt(e.split("_")[0])})),delete u.sections,n.schedules.set(i,u)}return console.log(n),n});o.a.render(r.a.createElement(H.a,{store:se},r.a.createElement(re,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[33,1,2]]]);
//# sourceMappingURL=main.8bbe7750.chunk.js.map