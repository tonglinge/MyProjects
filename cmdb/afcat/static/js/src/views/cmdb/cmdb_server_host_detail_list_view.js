/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var ServerAssetDetailItemView = require("./cmdb_server_host_detail_item_view").ServerAssetDetailItemView;
    var ServerAssetModalItemView = require("./cmdb_server_asset_modal_item_view").ServerAssetModalItemView;
    var HostCardDetailView = require("./cmdb_card_detail_view").HostCardDetailView;
    var VolumeGroupDetailView = require("./cmdb_volume_group_detail_view").VolumeGroupDetailView;

    var CMDBView = Backbone.View.extend({
        events: {
            "click .addRelateInfo": "loadModal",
            "change #staffSelect": "changeStaff",
            "click #submitStaff": "addStaff",
            "click #delStaff": "delServerAssetRelated",
            "click #editStaff": "loadModal",
            "click #submitCPU": "addCPU",
            "click #editCPU": "loadModal",
            "click #delCPU": "delServerAssetRelated",
            "click #submitIP": "addIP",
            "click #delIP": "delServerAssetRelated",
            "click #editIP": "loadModal",
            "click #submit-volume-group": "addVolumeGroup",
            "click #vg-detail": "volumeGroupDetail",
            "click #del-vg": "delVolumeGroup",
            "click #edit-vg": "loadModal",
            "click #submitServerHostCard": "addCard",
            "click #delServerHostCard": "delServerHostCard",
            "click #editServerHostCard": "loadModal",
            "click #server-host-card-detail": "serverHostCardDetail",
            "click #submitSoft": "addSoft",
            "click #delSoft": "delServerAssetRelated",
            "click #editSoft": "loadModal",
            "click #history-back": 'historyBack',
            "click #edit-lv": "editLV",
            "click #del-lv": "delLV",
            "click #add-lv": "addLV",
            "click #edit-pv": "editPV",
            "click #del-pv": "delPV",
            "click #add-pv": "addPV",
            "click #host-tabs li": "selectTab"
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.url = options.url;
            this.collection.url = options.url;
            this.sid = options.options.sid;
            this.model = options.options.model;
            this.module = options.options.type;
            this.listenTo(this.collection, 'reset', this.addAll);
            //this.listenTo(this.collection, 'all', this.render);
            this.collection.fetchData(true, JSON.stringify({"model":this.module, "sid":this.sid}));
        },
        addAll: function () {
            this.$el.find(".server-detail-record").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var detailview = new ServerAssetDetailItemView({model: model});
            this.$el.html(detailview.render().el);
        },
        selectTab: function (e) {
            this.select_li = e.currentTarget;
            var link = $(e.currentTarget).find("a").get(0).href;
            this.link_id = link.split("#")[1];
            this.select_tab_index = $(e.currentTarget).index();
        },
        historyBack: function (e) {
            window.location.href = "/cmdb/server_host_detail/list?sid=" + this.sid;
        },
        addPV: function (e) {
            //添加LV
            var pv_html = ' <tr>\
                 <td><input type="text" class="form-control"   /><span style="color: red;"></span></td>\
                 <td><input type="number" class="form-control"  /><span style="color: red;"></span></td>\
                 <td><input type="text" class="form-control"  /></td>\
                 <td style="display:none"></td>\
                 <td>\
                     <button href="#" class="btn btn-box-tool" title="编辑" id="edit-pv" title="编辑"><i class="fa fa-check"></i></button>&nbsp;\
                     <button href="#" class="btn btn-box-tool" title="删除"  id="del-pv" titile="删除"><i class="fa fa-remove"></i></button>\
                 </td>\
             </tr>';
            var vg_id = $(e.currentTarget).attr("vg-id");
            $("#pv-tbody").append(pv_html);
        },
        delPV: function (e) {
            //删除PV
            var pv_id = $(e.currentTarget).parent().prev().text();
            if(pv_id){
                var post_data = {
                    "asset":"StoragePV",
                    "value": {
                        "id":pv_id
                    },
                    "action":"del"
                }
                var vg_model = new this.model();
                vg_model.url = "/cmdb/relatedasset/";
                swal({
                    title: "确定删除该资产",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true},
                    function(){
                        vg_model.set("data", post_data, {validate: false});
                        vg_model.save({}, {success:function () {
                            var tr = $(e.target).closest('tr');
                            tr.remove();
                        }});
                    }
                );

            }else{
                var tr = $(e.target).closest('tr');
                tr.remove();
            }

        },
        editPV: function (e) {
            //更新PV信息
            var tds = $(e.currentTarget).parent().siblings();
            var pvname = $(tds[0]).children()[0].value;
            var pvsize = $(tds[1]).children()[0].value;
            var remark = $(tds[2]).children()[0].value;
            var pv_id = $(tds[3]).text();
            var vg_id = $(e.currentTarget).closest("tbody").attr("vg-id");
            var sid = this.sid;
            var post_data = {};

            if(pvname.length == 0){
                $($(tds[0]).children()[1]).text("输入有效值");
                return false
            }else{
                $($(tds[0]).children()[1]).text("")
            }
            if(pvsize.length == 0 || pvsize <= 0){
               $($(tds[1]).children()[1]).text("输入有效值");
                return false
            }else{
                $($(tds[1]).children()[1]).text("")
            }
            post_data["value"] = {};
            post_data["asset"] = "StoragePV";
            var action = pv_id?"edit":"new";
            post_data["action"] = action;
            post_data["value"] = {"pvname":pvname,
                "pvsize":pvsize,
                "vg_id":vg_id,
                "remark":remark
            }
            if(action == "edit"){post_data["value"]["id"] = pv_id};

            var the_collection = this.collection;
            var module = this.module;
            var the_select_li = this.select_li;
            var the_link_id = this.link_id;
            var select_tab_index = this.select_tab_index;
            var sid = this.sid;
            var vg_model = new this.model();
            vg_model.url = "/cmdb/relatedasset/";
            vg_model.set("data", post_data);
            vg_model.save({}, {success:function (response) {
                if(!pv_id){
                    var pv_id = response.id;
                    $(tds[3]).text(pv_id);
                }
            }});
        },
        addLV: function (e) {
            //添加LV
            var lv_html = ' <tr>\
                 <td><input type="text" class="form-control"  /><span style="color: red;"></span></td>\
                 <td><input type="number" class="form-control"  /><span  style="color: red;"></span></td>\
                 <td><input type="text" class="form-control"  /></td>\
                 <td><input type="text" class="form-control" /></td>\
                 <td style="display:none"></td>\
                 <td>\
                     <button href="#" class="btn btn-box-tool" title="编辑" id="edit-lv" title="编辑"><i class="fa fa-check"></i></button>&nbsp;\
                     <button href="#" class="btn btn-box-tool" title="删除"  id="del-lv" titile="删除"><i class="fa fa-remove"></i></button>\
                 </td>\
             </tr>';
             var vg_id = $(e.currentTarget).attr("vg-id");
            $("#lv-tbody").append(lv_html);
        },
        delLV: function (e) {
            //删除LV
            var lv_id = $(e.currentTarget).parent().prev().text();
            if(lv_id){
                var post_data = {
                    "asset":"StorageLV",
                    "value": {
                        "id":lv_id
                    },
                    "action":"del"
                }
                var vg_model = new this.model();
                vg_model.url = "/cmdb/relatedasset/";
                swal({
                    title: "确定删除该资产",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true},
                    function(){
                        vg_model.set("data", post_data);
                        vg_model.save({}, {success:function () {
                            var tr = $(e.target).closest('tr');
                            tr.remove();
                        }});
                    }
                );

            }else{
                var tr = $(e.target).closest('tr');
                tr.remove();
            }

        },
        editLV: function (e) {
            //更新LV信息
            var tds = $(e.currentTarget).parent().siblings();
            var lvname = $(tds[0]).children()[0].value;
            var lvsize = $(tds[1]).children()[0].value;
            var filesystem = $(tds[2]).children()[0].value;
            var remark = $(tds[3]).children()[0].value;
            var lv_id = $(tds[4]).text();
            var vg_id = $(e.currentTarget).closest("tbody").attr("vg-id");
            var sid = this.sid;
            var post_data = {};
            post_data["value"] = {};
            post_data["asset"] = "StorageLV";
            var action = lv_id?"edit":"new";
            post_data["action"] = action;
            post_data["value"] = {"lvname":lvname,
                "lvsize":lvsize,
                "filesystem":filesystem,
                "vg_id":vg_id,
                "remark":remark
            };
            if(lvname.length == 0){
                $($(tds[0]).children()[1]).text("输入有效值");
                return false
            }else{
                $($(tds[0]).children()[1]).text("")
            }
            if(lvsize.length == 0 || lvsize <= 0){
               $($(tds[1]).children()[1]).text("输入有效值");
                return false
            }else{
                $($(tds[1]).children()[1]).text("")
            }

            if(action == "edit"){post_data["value"]["id"] = lv_id}

            var the_collection = this.collection;
            var module = this.module;
            var the_select_li = this.select_li;
            var the_link_id = this.link_id;
            var select_tab_index = this.select_tab_index;
            var sid = this.sid;
            var vg_model = new this.model();
            vg_model.url = "/cmdb/relatedasset/";
            vg_model.set("data", post_data);
            vg_model.save({}, {success:function (response) {
                if(!lv_id){
                    $(tds[4]).text(response.id)
                }
            }});
        },
        ajax_submit: function (data) {
            //ajax提交修改relatedasset的请求
            var the_collection = this.collection;
            var module = this.module;
            var the_select_li = this.select_li;
            var the_link_id = this.link_id;
            var select_tab_index = this.select_tab_index;
            var sid = this.sid;

            var server_host_model = new this.model();
            server_host_model.url = "/cmdb/relatedasset/";
            server_host_model.set("data", data);
            server_host_model.save({}, {success:function (response) {
                $(".modal").modal("hide");
                $(".modal-backdrop").fadeOut();
                the_collection.fetchData(true, JSON.stringify({"model":module, "sid":sid}), {async:false});
                $("#host-tabs li:first").removeClass("active");
                $("#tab_0").removeClass("active");
                $("#host-tabs li:eq("+select_tab_index+")").addClass("active");
                //$("#host-tabs li:eq(select_tab_index)").attr("class", "active");
                //$("#host-tabs").find("li").eq(select_tab_index).trigger("click");
                $("#tab_"+select_tab_index).addClass("active");
            }});
        },
        delServerAssetRelated: function (e) {
            //删除服务器相关资产
            var modelarr = {
                "delSoft": "InstalledSoftList",
                "delStorageCard": "StorageCard",
                "delStorage": "StorageInfo",
                "delNic": "Nic",
                "delIP": "IPConfiguration",
                "delCPU": "CpuMemory",
                "delStaff": "R_Server_Staff",
            };
            var obj_id = $(e.currentTarget).parent()[0].id;
            var operation = e.currentTarget.id;
            var tableModel = modelarr[operation];
            swal({
                    title: "确定删除该资产信息?",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    cancelButtonText: '取消',
                    confirmButtonText: "确定",
                    confirmButtonColor: "#DD6B55",
                    closeOnConfirm: true
                },
                function(){
                    var data = {"asset":tableModel, "value":{"id":obj_id},"action":"del"};
                    $.ajax({
                        "type": "POST",
                        "url": "/cmdb/relatedasset/",
                        "data": {data: JSON.stringify(data)},
                    });
                    $(e.currentTarget).parent().parent().remove();
                });

        },
        addSoft: function (e) {
            //添加软件安装记录
            var soft_type = $("#soft_type").val();
            var soft_id = $("#softname").val();
            var license = $("#license").val();
            var port = $("#port").val();
            var remark = $("#remark").val();
            var softid = $("#soft_id").val();
            var id = $("#basesoft").val();

            var data = {"asset":"InstalledSoftList",
                "value": {"server_id":this.sid,
                    "soft_id":soft_id,
                    "lisence_id":license,
                    "port":port,
                    "remark":remark
                },
            };
            if(id){
                var  action = "edit";
                data["value"]["id"] = id;
            }else{
                var action = "new";
            }
            data["action"] = action;
            this.ajax_submit(data);
        },
        addCard: function (e) {
            //添加板卡记录
            var form_data = $("#card-form").serializeArray();
            var post_data = {};
            post_data["value"] = {};
            post_data["value"]["server_id"] = this.sid;
            $.each(form_data, function (index, field) {
                if(field.name == "id" && field.value != ""){
                    post_data["action"] = "edit";
                    post_data["value"][field.name] = field.value;
                }else if(field.name == "id" && field.value == ""){
                    post_data["action"] = "new";
                }else{
                    post_data["value"][field.name] = field.value;
                }
            });
            if(post_data["value"]["ports"]){
                while (post_data["value"]["ports"].indexOf("\n") >= 0){
                    post_data["value"]["ports"] = post_data["value"]["ports"].replace("\n", ",");
                }
            }
            var the_collection = this.collection;
            var module = this.module;
            var the_select_li = this.select_li;
            var the_link_id = this.link_id;
            var select_tab_index = this.select_tab_index;
            var sid = this.sid;
            var host_model = new this.model();
            host_model.url = "/cmdb/servboardcard/";
            host_model.set("data", post_data, {validate: false});
            host_model.save({}, {success:function () {
                $(".modal").modal("hide");
                $(".modal-backdrop").fadeOut();
                the_collection.fetchData(true, JSON.stringify({"model":module, "sid":sid}), {async:false});
                $("#host-tabs li:first").removeClass("active");
                $("#tab_0").removeClass("active");
                $("#host-tabs li:eq(select_tab_index)").addClass("active");
                //$("#host-tabs li:eq(select_tab_index)").attr("class", "active");
                $("#"+the_link_id).attr("class", "tab-pane active");
                $("#host-tabs li:eq(select_tab_index)").trigger("click");
            }});
        },
        delServerHostCard: function (e) {
            //删除板卡
            var card_id = $(e.currentTarget).parent().prev().text();
            var post_data = {};
            post_data = {
                "value": {
                    "id": card_id,
                },
                "action": "del"
            }
            var host_model = new this.model();
            swal({
                    title: "确定删除该资产信息?",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    cancelButtonText: '取消',
                    confirmButtonText: "确定",
                    confirmButtonColor: "#DD6B55",
                    closeOnConfirm: true
                },
                function(){
                    host_model.url = "/cmdb/servboardcard/";
                    host_model.set("data", post_data);
                    host_model.save({}, {success:function () {
                    }});
                    $(e.currentTarget).parent().parent().remove();
                }
            );

        },
        addVolumeGroup: function (e) {
            //添加VG信息
            var form_data = $("#volume-group-form").serializeArray();
            var post_data = {};
            post_data["value"] = {};

            post_data["asset"] = "StorageVG";
            post_data["value"]["server_id"] = this.sid;
            $.each(form_data, function (index, field) {
                if(field.name == "id" && field.value != ""){
                    post_data["value"][field.name] = field.value;
                    post_data["action"] = "edit";
                }else if(field.name == "id" && field.value == ""){
                    post_data["action"] = "new";
                }else{
                    post_data["value"][field.name] = field.value;
                }
            });
            if(post_data["value"]["vgname"].length == 0){
                $("#err-vgname").text("请输入有效值");
                return false
            }else{
                $("#err-vgname").text("*");
            }
            if(post_data["value"]["vgsize"].length == 0 || post_data["value"]["vgsize"] <=0 ){
                 $("#err-vgsize").text("请输入有效值");
                return false
            }else{
                $("#err-vgsize").text("*");
            }
            var the_collection = this.collection;
            var module = this.module;
            var the_select_li = this.select_li;
            var the_link_id = this.link_id;
            var select_tab_index = this.select_tab_index;
            var sid = this.sid;
            var host_model = new this.model();
            host_model.url = "/cmdb/relatedasset/";
            host_model.set("data", post_data);
            host_model.save({}, {success:function () {
                $(".modal").modal("hide");
                $(".modal-backdrop").fadeOut();
                the_collection.fetchData(true, JSON.stringify({"model":module, "sid":sid}), {async:false});
                $("#host-tabs li:first").removeClass("active");
                $("#tab_0").removeClass("active");
                $("#host-tabs li:eq(select_tab_index)").addClass("active");
                //$("#host-tabs li:eq(select_tab_index)").attr("class", "active");
                $("#"+the_link_id).attr("class", "tab-pane active");
                $("#host-tabs li:eq(select_tab_index)").trigger("click");
            }});
        },
        delVolumeGroup: function (e) {
            //删除VG
            var volume_group_id = $(e.currentTarget).parent().prev().text();
            var post_data = {};
            post_data = {
                "asset":"StorageVG",
                "value": {
                    "id": volume_group_id,
                },
                "action": "del"
            }
            var host_model = new this.model();
            swal({
                    title: "确定删除该资产信息?",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    cancelButtonText: '取消',
                    confirmButtonText: "确定",
                    confirmButtonColor: "#DD6B55",
                    closeOnConfirm: true
                },
                function(){
                    host_model.url = "/cmdb/relatedasset/";
                    host_model.set("data", post_data);
                    host_model.save({}, {success:function () {
                    }});
                    $(e.currentTarget).parent().parent().remove();
                }
            );
        },
        volumeGroupDetail: function (e) {
            //VG详情
            var vg_id = $(e.currentTarget).parent().prev().text();
            this.$el.find(".server-detail-record").html('');
            this.collection.url = "/cmdb/vgdetail/";
            this.collection.fetchData(false, JSON.stringify({id:vg_id}), {async:false});
            this.collection.url = this.url;
            var view = new VolumeGroupDetailView({collection: this.collection, model:this.model, sid:this.sid, vg_id:vg_id});
            $(".server-detail-record").html(view.render().el);
        },
        serverHostCardDetail: function (e) {
            var card_id = $(e.currentTarget).parent().prev().text();
            this.$el.find(".server-detail-record").html('');
            this.collection.url = "/cmdb/servboardcard/";
            this.collection.fetchData(false, JSON.stringify({cardid:card_id}), {async:false});
            this.collection.url = this.url;
            var view = new HostCardDetailView({collection: this.collection, model:this.model, sid:this.sid, card_id:card_id});
            $(".server-detail-record").html(view.render().el);
        },
        addIP: function (e) {
            var ipaddress = $("#ipaddress").val();
            var gateway = $("#gateway").val();
            var iptype = $("#iptype").val();
            var domain = $("#domain").val();
            var vlan = $("#vlan").val();
            var remark = $("#remark").val();
            var ip_id = $("#ip_id").val()
            if(!ip_id){
                var data = {
                    "asset":"IPConfiguration",
                    "value":{ "server_id":this.sid,
                        "ipaddress":ipaddress,
                        "gatway":gateway,
                        "iptype":iptype,
                        "domain":domain,
                        "vlan":vlan,
                        "remark":remark},
                    "action":"new"
                };
            }else{

                 var data = {
                    "asset":"IPConfiguration",
                    "value":{"id":ip_id,
                        "server_id":this.sid,
                        "ipaddress":ipaddress,
                        "gatway":gateway,
                        "iptype":iptype,
                        "domain":domain,
                        "vlan":vlan,
                        "remark":remark},
                    "action":"edit"
                };
            }
            if (ipaddress.length == 0){
                $("#err-ipaddr").text("请输入有效值");
                return false;
            }else{
                $("#err-ipaddr").text("*");
            }
            if (gateway.length == 0){
                $("#err-gatway").text("请输入有效值");
                return false;
            }else{
                $("#err-gatway").text("*");
            }
            this.ajax_submit(data);

        },
        addCPU: function (e) {
            //增加CPU信息
            var model = $("#model").val();
            var cpucount = $("#cpucount").val();
            var corecount = $("#corecount").val();
            var frequency = $("#frequency").val();
            var memory = $("#memory").val();
            var remark = $("#remark").val();
            var cpu_id = $("#cpu_id").val();
            if(!cpu_id){
                var action = "new";
                var data = {
                    "asset":"CpuMemory",
                    "value":{
                        "server_id":this.sid,
                        "model":model,
                        "cpucount":cpucount,
                        "corecount":corecount,
                        "frequency":frequency,
                        "memory":memory,
                        "remark":remark},
                    "action":action
                };
            }else{

                var action = "edit";
                var data = {
                    "asset":"CpuMemory",
                    "value":{
                        "id": cpu_id,
                        "server_id":this.sid,
                        "model":model,
                        "cpucount":cpucount,
                        "corecount":corecount,
                        "frequency":frequency,
                        "memory":memory,
                        "remark":remark},
                    "action":action
                };
            }
            if(cpucount.length ==  0 || cpucount <= 0){
                $("#err-cpucount").text("请输入有效值");
                return false;
            }else{
                $("#err-cpucount").text("*");
            }
            if(memory <= 0 || memory.length == 0){
                $("#err-memory").text("请输入有效值");
                return false;
            }else{
                 $("#err-memory").text("*");
            }
            this.ajax_submit(data);
        },
        addStaff: function (e) {
            //增加联系人
            var staff_id = $("#staffSelect").val();
            var mobile = $("#mobile").val();
            var telphone = $("#telphone").val();
            var email = $("#email").val();
            var remark = $("#remark").val();
            var role_id = $("#role").val();
            var id = $("#R_server_staff").val();
            var opration = $("#opration").val();
            if(opration == "edit"){
                var action = "edit";
                var data = {
                    "asset": "R_Server_Staff",
                    "value":{
                        "id": id,
                        "staff_id": staff_id,
                        "server_id": this.sid,
                        "role_id": role_id,
                        "remark": remark,
                    },
                    "action": action,
                };
            }
            else{
                var action = "new";
                var data = {
                    "asset": "R_Server_Staff",
                    "value":{
                        "staff_id": staff_id,
                        "server_id": this.sid,
                        "role_id": role_id,
                        "remark": remark,
                    },
                    "action": action,
                };
            }
            this.ajax_submit(data);
        },
        changeStaff: function (e) {
            //选择联系人模态框的联系人
            var staff_id = $("#staffSelect option:selected").val();
            var staffs = this.result.responseJSON.data.staffs;
            $.each(staffs, function (index, staff) {
                if(staff_id == staff.id){
                    $("#mobile").val(staff.mobile);
                    $("#telphone").val(staff.tel);
                    $("#email").val(staff.email);
                    $("#remark").val(staff.remark);
                    $("#staff_id").val(staff.id);
                }
            })
        },
        edit_cpu: function (row) {
            var model = $($(row)[0]).text();
            var cpucount = $($(row)[1]).text();
            var corecount = $($(row)[2]).text();
            var frequency = $($(row)[3]).text();
            var memory = $($(row)[4]).text();
            var remark = $($(row)[5]).text();
            var cpu_id = $($(row)[6]).text();
            $("#model").val(model);
            $("#cpucount").val(cpucount);
            $("#corecount").val(corecount);
            $("#frequency").val(frequency);
            $("#memory").val(memory);
            $("#remark").val(remark);
            $("#cpu_id").val(cpu_id);
        },
        edit_ip:function (row) {
            var ipaddress = $($(row)[0]).text();
            var gateway = $($(row)[1]).text();
            var iptype = $($(row)[2]).text();
            var domain = $($(row)[3]).text();
            var vlan = $($(row)[4]).text();
            var remark = $($(row)[5]).text();
            var ip_id = $($(row)[6]).text();
            $("#ipaddress").val(ipaddress);
            $("#gateway").val(gateway);
            $("#iptype").val(iptype);
            $("#domain").val(domain);
            $("#vlan").val(vlan);
            $("#remark").val(remark);
            $("#ip_id").val(ip_id);
        },
        edit_volumegroup: function (row) {
            var vgname = $($(row)[0]).text();
            var vgsize = $($(row)[1]).text();
            var raidtype_name = $($(row)[2]).text();
            var remark = $($(row)[3]).text();
            var volume_group_id = $($(row)[4]).text();

            var callback_data = this.result.responseJSON.data;
            var baseraidtype = callback_data.baseraidtype;
            $.each(baseraidtype, function (index, raid_type) {
                if(raid_type.typename == raidtype_name){
                    $("#raidtype_id").val(raid_type.id);
                }
            })

            $("#vgname").val(vgname);
            $("#vgsize").val(vgsize);
            $("#remark").val(remark);
            $("#id").val(volume_group_id);
        },
        edit_card:function (row) {
            //编辑板卡
            var sn = $($(row)[0]).text();
            var typename = $($(row)[1]).text();
            var model = $($(row)[2]).text();
            var factory_name = $($(row)[3]).text();
            var mac = $($(row)[4]).text();
            var slot = $($(row)[5]).text();
            var portcount = $($(row)[6]).text();
            var remark = $($(row)[7]).text();
            var card_id = $($(row)[8]).text();

            var cardtype_dict = {"网卡":1, "存储卡":2};
            var cardtype = cardtype_dict[typename];
            $("#cardtype").val(cardtype);

            var callback_data = this.result.responseJSON.data;
            var basefactory = callback_data.basefactory;
            var basestoragecardtype = callback_data.basestoragecardtype;
            $.each(basefactory, function (index, factory) {
                if(factory.name == factory_name){
                    $("#factory_id").val(factory.id);
                }
            });

            $("#sn").val(sn);
            $("#model").val(model);
            $("#mac").val(mac);
            $("#slot").val(slot);
            $("#id").val(card_id);
        },
        edit_soft:function (row) {
            var softname = $($(row)[0]).text();
            var soft_type = $($(row)[1]).text();
            var version = $($(row)[2]).text();
            var license = $($(row)[3]).text();
            var port = $($(row)[4]).text();
            var remark = $($(row)[5]).text();
            var id = $($(row)[6]).text();
            var soft_id = $($(row)[7]).text();

            var callback_data = this.result.responseJSON.data;
            var basesofttype = callback_data.basesofttype;
            var basesoft = callback_data.basesoft;
            var softlisence = callback_data.softlisence;
            //选择软件分类
            $.each(basesofttype, function (index, softtype) {
                var classname = $("#softname option").attr("class", softtype.id);
                if(softtype.name == soft_type){
                    $("#soft_type").val(softtype.id);
                    softtype_id = softtype.id;
                }

            });

            //选择软件
            $.each(basesoft, function (index, soft) {
                if(soft.type_id == softtype_id){
                    $("#softname option[value=" + soft.id + "]").css("display", "");
                }else{
                    $("#softname option[value=" + soft.id + "]").css("display", "none");
                }

            });
            $("#softname option[value=" + soft_id + "]").attr("selected", true)

            //选择license
            if(license){
                $.each(softlisence, function (index, sl) {
                    if(sl.soft_id == soft_id){
                        $("#license option[value=" +  sl.id +"]").css("display", "");
                    }
                    else{
                        $("#license option[value=" +  sl.id +"]").css("display", "none");
                    }
                    if(sl.lisence == license){
                        $("#license option[value=" +  sl.id +"]").attr("selected", true);
                    }
                });
            }else{
                $.each(softlisence, function (index, sl) {
                    if(sl.soft_id == soft_id){
                        $("#license option[value=" +  sl.id +"]").css("display", "");
                    }
                    else{
                        $("#license option[value=" +  sl.id +"]").css("display", "none");
                    }
                });
                $("#license").val("");
            }


            $("#port").val(port);
            $("#remark").val(remark);
            $("#basesoft").val(id);
            $("#soft_id").val(soft_id);
        },
        edit_staff:function (row) {
            var staff_name = $($(row)[0]).text();
            var mobile = $($(row)[1]).text();
            var telphone = $($(row)[2]).text();
            var role_name = $($(row)[3]).text();
            var email = $($(row)[4]).text();
            var remark = $($(row)[5]).text();
            var id = $($(row)[6]).text();
            var staff_id = $($(row)[7]).text();

            var callback_data = this.result.responseJSON.data;
            var baserole = callback_data.baserole;
            var staffs = callback_data.staffs;
            $.each(staffs, function (index, staff) {
                if(staff.name == staff_name){
                    $("#staffSelect option[value=" + staff.id + "]").attr("selected", true);
                }
            });

            $("#mobile").val(mobile);
            $("#telphone").val(telphone);
            $("#email").val(email);
            $("#remark").val(remark);
            $("#opration").val("edit");
            $.each(baserole, function (index, role) {
                if(role.role_name == role_name){
                    $("#role option[value=" + role.id + "]").attr("selected", true);
                }
            });
            $("#R_server_staff").val(id);
            $("#staff_id").val(staff_id);
        },
        get_row: function (current_id, target) {
            //指定tr一行数据进行编辑
            var row = $(target).parent().siblings("td");
            if(current_id == "editCPU"){
                this.edit_cpu(row);
            }else if(current_id == "editIP"){
                this.edit_ip(row);
            }else if(current_id == "edit-vg"){
                this.edit_volumegroup(row);
            }else if(current_id == "editServerHostCard"){
                this.edit_card(row);
            }else if(current_id == "editSoft"){
                this.edit_soft(row);
            }else if(current_id == "editStaff"){
                this.edit_staff(row);
            }
        },
        loadModal: function (e) {
            //加载模态框
            var modalarr = {
                "addStaff": {"id":"#staffModal", "option": {"tables":["Staffs", "BaseRole"]}},
                "editStaff": {"id":"#staffModal", "option": {"tables":["Staffs", "BaseRole"]}},
                "addSoft": {"id":"#softwareModal", "option": {"tables":["BaseSoft", "BaseSoftType", "SoftLisence"]}},
                "editSoft": {"id":"#softwareModal", "option": {"tables":["BaseSoft", "BaseSoftType", "SoftLisence"]}},
                "addServerHostCard": {"id":"#CardModal", "option": {"tables":["BaseFactory"]}},
                "editServerHostCard": {"id":"#CardModal", "option": {"tables":["BaseFactory"]}},
                "addCPU": {"id":"#CPUModal", "option": ""},
                "editCPU": {"id":"#CPUModal", "option": ""},
                "addIP": {"id":"#IPModal", "option": ""},
                "editIP": {"id":"#IPModal", "option": ""},
                "add-vg": {"id":"#VGModal", "option": {"tables":["BaseRaidType"]}},
                "edit-vg": {"id":"#VGModal", "option": {"tables":["BaseRaidType"]}},
            };

            var curr_id = e.currentTarget.id;
            //加载模态框
            if(modalarr[curr_id]["option"]){
                this.result  = $.ajax({
                    async: false,
                    "type":"get",
                    "url": "/cmdb/basedata/",
                    "dataType": "json",
                    "data": {data:JSON.stringify(modalarr[curr_id]["option"])},
                    "success": function (response) {
                        var modalview = new ServerAssetModalItemView({"current_id":curr_id, "data":response.data});
                        $(modalarr[curr_id]["id"]).append(modalview.render().el);
                        if(curr_id == "editServerHostCard"){
                            $("#portlist").hide();
                        }
                    }
                });
            }else{
                var modalview = new ServerAssetModalItemView({"current_id":curr_id});
                $(modalarr[curr_id]["id"]).append(modalview.render().el);
            }
            this.get_row(curr_id, e.currentTarget)
        },
    });

    return CMDBView;
})

