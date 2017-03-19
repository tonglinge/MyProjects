/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var EquipmentDetailItemView = require("./cmdb_equipment_detail_item_view").EquipmentDetailItemView;
    var EquipmentCardDetailView = require("./cmdb_card_detail_view").EquipmentCardDetailView;
    var ServerAssetModalItemView = require("./cmdb_server_asset_modal_item_view").ServerAssetModalItemView;

    var CMDBView = Backbone.View.extend({
        events: {
            "click .addRelateInfo": "loadModal",
            "change #staffSelect": "changeStaff",
            "click #submitStaff": "addStaff",
            "click #delStaff": "delStaff",
            "click #editStaff": "loadModal",
            "click #portDetail": "showPortList",
            "click #submitCard": "addCard",
            "click #delCard": "delCard",
            "click #editCard": "editCard",
            "click #equipment-tab li": "selectTab"
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.collection.url = options.url;
            this.sid = options.options.sid;
            this.model = options.options.model;
            this.module = options.options.type;
            this.listenTo(this.collection, 'reset', this.addAll);
            //this.listenTo(this.collection, 'all', this.render);
            this.collection.fetchData(true, JSON.stringify({"model":this.module, "sid":this.sid}));
        },
        addAll: function () {
            this.$el.find(".equipment-detail-record").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var detailview = new EquipmentDetailItemView({model: model});
            this.$el.html(detailview.render().el);
        },
        selectTab: function (e) {
            this.select_li = e.currentTarget;
            var link = $(e.currentTarget).find("a").get(0).href;
            this.link_id = link.split("#")[1];
            this.select_tab_index = $(e.currentTarget).index();
            if(this.select_tab_index != 1){
                $("#cardDetail").hide();
            }
        },
        showPortList: function (e) {
            //显示板卡端口详情
            var card_id = $(e.currentTarget).parent()[0].id;

            $("#basebox").toggle();
            $("#card").toggle();
            $("#staffs").toggle();
            $(".nav-tabs-custom").toggle();
            this.collection.fetchData(false, JSON.stringify({"model":this.module, "sid":this.sid}), false);
            var cardview = new EquipmentCardDetailView({collection: this.collection, model:this.model, sid:this.sid, card_id:card_id});
            $("#cardDetail").html(cardview.render().el);
            $("#cardDetail").toggle();
        },
        ajax_submit: function (url, data) {
            //提交修改请求
            var sid = this.sid;
            var equipment_model = new this.model();
            equipment_model.url = url;
            equipment_model.set("data", data);
            $("#loading").fadeIn("fast");
            equipment_model.save({}, {success:function (model, response) {
                $("#loading").fadeOut("slow");
                $(".close").click();
            }, error:function () {
                $("#loading").fadeOut("slow");
            }, async:false});
        },
        delServerAssetRelated: function (currentTarget, tableModel) {
            //删除设备资产关联信息
            var obj_id = $(currentTarget).parent()[0].id;
            var data = {"asset":tableModel, "value":{"id":obj_id},"action":"del"};
            var sid = this.sid;
            var equipment_model = new this.model();
            equipment_model.url = "/cmdb/relatedasset/";
            equipment_model.set("data", data);
            swal(
                {
                    title: "确定删除该信息？",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true
                },
                function(){
                    equipment_model.save({}, {success:function (model, response) {
                        $(currentTarget).parent().parent().remove();
                    }});

                }
            );

        },
        delCard: function (e) {
            //删除板卡
            var obj_id = $(e.currentTarget).parent()[0].id;
            var data = {"optype":1, "value":{"id":obj_id},"action":"delete"};
            swal(
                {
                    title: "确定删除该信息？",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true
                },
                function(){
                    $.ajax({
                        "type": "POST",
                        "url": "/cmdb/eboardcard/",
                        "data": {data: JSON.stringify(data)},
                        "success":function () {
                            $(e.currentTarget).parent().parent().remove();
                        }
                    });

                }
            );
        },
        editCard: function (e) {
            //编辑板卡
            var sid = this.sid;
            var tds = $(e.currentTarget).parent().siblings();
            var cardname = $(tds[0]).children()[0].value;
            var sn = $(tds[1]).children()[0].value;
            var model = $(tds[2]).children()[0].value;
            var slot = $(tds[3]).children()[0].value;
            var remark = $(tds[5]).children()[0].value;
            var card_id = $(tds[6]).text();

            var data = {};
            data["value"] = {"id":card_id,
                "equipment_id":sid,
                "sn":sn,
                "cardname":cardname,
                "slot":slot,
                "remark":remark,
                "model":model,
            },
            data["optype"] = 1;
            data["action"] = "edit";

            var sid = this.sid;
            var equipment_model = new this.model();
            equipment_model.url = "/cmdb/eboardcard/";
            equipment_model.set("data", data);
            equipment_model.save({}, {success:function (model, response) {
                if(response.status == true){
                    if(response.info && response.info != "") {
                        swal({   title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                    }
                }else {
                    swal({ title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                }
            }});
        },
        addCard: function (e) {
            //添加板卡信息
            var equipment_id = this.sid;
            var cardname = $("#cardname").val();
            var slot = $("#slot").val();
            var sn = $("#sn").val();
            var model = $("#model").val();
            var ports = $("#ports").val();
            var remark = $("#remark").val();
            var card_id = $("#card_id").val();
            var opration = $("#opration").val();

            while (ports.indexOf("\n") >= 0){
                ports = ports.replace("\n", ",");
            }

            var data = {};
            data["value"] = {"equipment_id":equipment_id,
                "sn":sn,
                "cardname":cardname,
                "slot":slot,
                "remark":remark,
                "model":model,
                "ports":ports,
            },
            data["optype"] = 1;

            if(opration == "edit"){
                var action = "edit";
                data["value"]["id"] = card_id;
            }else{
                var action = "new";
            }
            data["action"] = action;
            //this.ajax_submit("/cmdb/eboardcard/", data);
            var card_model = new this.model();
            card_model.url = "/cmdb/eboardcard/";
            card_model.set("data", data);
            card_model.save({}, {success:function (model, response){
                $(".close").click();
                if(action == "new"){
                    if(!response.data.remark){
                        response.data.remark = "";
                    }
                    if(!response.data.ports.length){
                        response.data.ports.length = "";
                    }
                    if(!response.data.slot){
                        response.data.slot = "";
                    }
                    if(!response.data.model){
                        response.data.model = "";
                    }
                    if(!response.data.sn){
                        response.data.sn = "";
                    }
                    if(!response.data.cardname){
                        response.data.cardname = "";
                    }

                    var html = '<tr>\
                        <td><input class="form-control" value="' + response.data.cardname + '" /></td>\
                        <td><input class="form-control" value="' + response.data.sn + '" /></td>\
                        <td><input class="form-control" value="' + response.data.model +'" /></td>\
                        <td><input class="form-control" value="' + response.data.slot + '" /></td>\
                        <td><input class="form-control" value="' + response.data.ports.length + '" disabled="disabled" style="width:60px;"/></td>\
                        <td><input class="form-control" value="'+response.data.remark+'"/></td>\
                        <td style="display:none">'+ response.data.id + '</td>\
                        <td id="opration" style="display:none"></td>\
                        <td id='+response.data.id+' style="width:250px;">\
                            <button type="button" href="#" class="btn btn-box-tool" id="editCard" title="编辑板卡"><span class="fa fa-check"></span></button>\
                            <button type="button" href="#" class="btn btn-box-tool" id="delCard" title="删除板卡"><span class="fa fa-remove"></span></button>\
                            <button type="button" href="#" class="btn btn-box-tool" id="portDetail"><i class="fa fa-th"></i></button>\
                        </td>\
                    </tr>';
                    $("#card-tbody").append(html);
                }
            }});
        },
        delStaff: function (e) {
            this.delServerAssetRelated(e.currentTarget, "R_Equipment_Staff");
        },
        addStaff: function (e) {
            //增加联系人
            var editing_staff_row = this.editing_staff_row;
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
                    "asset": "R_Equipment_Staff",
                    "value":{
                        "id": id,
                        "staff_id": staff_id,
                        "equipment_id": this.sid,
                        "role_id": role_id,
                        "remark": remark,
                    },
                    "action": action,
                };
            }
            else{
                var action = "new";
                var data = {
                    "asset": "R_Equipment_Staff",
                    "value":{
                        "staff_id": staff_id,
                        "equipment_id": this.sid,
                        "role_id": role_id,
                        "remark": remark,
                    },
                    "action": action,
                };
            }
            //this.ajax_submit("/cmdb/relatedasset/", data);
            var card_model = new this.model();
            card_model.url = "/cmdb/relatedasset/";
            card_model.set("data", data);
            card_model.save({}, {success:function (model, response){
                $(".close").click();
                if(action === "new"){
                    var html = '\
                    <tr>\
                        <td>'+response.data.name+'</td>\
                        <td>'+response.data.mobile+'</td>\
                        <td>'+response.data.tel+'</td>\
                        <td>'+response.data.role+'</td>\
                        <td>'+response.data.email+'</td>\
                        <td>'+response.data.remark+'</td>\
                        <td style="display:none">'+response.data.id+'</td>\
                        <td style="display:none">'+response.data.staff_id+'</td>\
                        <td id="opration" style="display:none"></td>\
                        <td id='+response.data.id+'>\
                            <a type="button" href="#" class="box-tool" id="editStaff"><span class="fa fa-edit"></span></a>\
                            <a type="button" href="#" class="box-tool" id="delStaff"><span class="fa fa-remove"></span></a>\
                        </td>\
                    </tr>\
                    ';
                    $("#staff-tbody").append(html);
                }else{
                    //the_collection.fetchData(true, JSON.stringify({"model":module, "sid":sid}), false);
                    editing_staff_row[0].innerHTML = response.data.name;
                    editing_staff_row[1].innerHTML = response.data.mobile;
                    editing_staff_row[2].innerHTML = response.data.tel;
                    editing_staff_row[3].innerHTML = response.data.role;
                    editing_staff_row[4].innerHTML = response.data.email;
                    editing_staff_row[5].innerHTML = response.data.remark;
                    editing_staff_row[6].innerHTML = response.data.id;
                    editing_staff_row[7].innerHTML = response.data.staff_id;
                    editing_staff_row[8].innerHTML = action;
                    editing_staff_row[9].id = response.data.id;
                }
            }});
        },
        changeStaff: function (e) {
            //联系人模态框选择联系人
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
        edit_staff:function (row) {
            this.editing_staff_row = row;
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

            $("#staffSelect").val(staff_id);
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
            var row = $(target).parent().parent().find("td");
            if(current_id == "editStaff"){
                this.edit_staff(row);
            }else if(current_id == "editCard"){
                this.editCard(row);
            }
        },
        loadModal: function (e) {
            //加载模态框
            var modalarr = {
                "addStaff": {"id":"#staffModal", "option": {"tables":["Staffs", "BaseRole"]}},
                "editStaff": {"id":"#staffModal", "option": {"tables":["Staffs", "BaseRole"]}},
                "addCard": {"id":"#cardModal", option:""},
                "editCard": {"id":"#cardModal", option:""},
            };

            var curr_id = e.currentTarget.id;
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

