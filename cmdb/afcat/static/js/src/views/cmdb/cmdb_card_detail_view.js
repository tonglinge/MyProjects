/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var EquipmentCardDetailTemplate = require('text!./templates/equipment_card_detail_template.tpl');
    var HostCardDetailTemplate = require('text!./templates/host_card_detail_template.tpl');
    var EquipmentCardDetailView = Backbone.View.extend({
        className: "",
        tagName: "div",
        template: _.template(EquipmentCardDetailTemplate),
        events: {
            "click #choose-port": "ChoosePort",
            "click #search-port": "SearchPort",
            "click #addPort": "addPort",
            "click #addMap": "addMap",
            "click #delPort": "delPort",
            "click #editPort": "editPort",
            "click #delMap": "delMap",
            "click #editMap": "editMap",
            "blur #localport": "portValid",
        },
        initialize: function (options) {
            this.model = options.model;
            this.collection = options.collection;
            this.url = options.url;
            this.sid = options.sid;
            this.card_id = options.card_id;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        SearchPort: function (e) {
            //搜索对端端口
            $("#port-form").submit();
        },
        ChoosePort: function (e) {
            //选择对端端口
            var tds = $(e.currentTarget).parent().parent().parent().siblings();
            var targetport_id = $(tds[4]).find("input")[0].value;
            $("#currChoose").attr("chooseport", targetport_id);
            var pageUrl = "/cmdb/equipment_card_port_search/list?sid=" + this.sid;
            window.open(pageUrl,window,'height=600px,width=500px,left=500px,top=0px,resizable=no,scrollbars=yes');
        },
        portValid: function (e) {
            var porttags = $("#portlist tr").find("td:eq(0)").find("input");
            var used_ports_tags = $(e.currentTarget).parent().parent().siblings().find("td:eq(0)").find("input");
            var ports = [];
            var used_ports = [];
            var new_port = $(e.currentTarget)[0].value;
            $.each(porttags, function (index, tags) {
                ports.push(tags.value);
            });
            $.each(used_ports_tags, function (index, tags) {
                used_ports.push(tags.value);
            });
            var port_is_used = used_ports.indexOf(new_port);
            if(port_is_used != -1){
                swal({title: "",
                    text: '端口"'+new_port+'"已做映射！',
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true}
                );
                return false;
            }
            var find_port = ports.indexOf(new_port);
            if(find_port == -1){
                swal({title: "",
                    text: '端口"'+new_port + '"不存在,请使用有效端口！',
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true}
                );
                return false;
            }
        },
        addPort: function (e) {
            //添加板卡端口
            var html = "<tr>";
            html += '<td><input class="form-control" style="width:100px" /></td>';
            html += '<td><input class="form-control" style="width:100px" value="" /></td>';
            html += '<td><input class="form-control" style="width:100px" value="" /></td>';
            html += '<td><input class="form-control" style="width:300px" value="" /></td> \
                        <td style="display:none"><input class="form-control" type="text" value="" /></td> \
                        <td> \
                            <button type="button" href="#" class="btn btn-box-tool" id="editPort"><span class="fa fa-check"></span></button> \
                            <button type="button" href="#" class="btn btn-box-tool" id="delPort"><span class="fa fa-remove"></span></button> \
                        </td> \
                    </tr>';
            $("#portlist").append(html);
        },
        addMap: function (e) {
            //添加板卡端口映射
            var html = "<tr>";
            html += '<td><input class="form-control" id="localport"  style="width:100px" value=""  /></td>';
            html += '<td>';
            html += '<div class="input-group input-group-sm" style="width: 80px;">';
            html += '<div class="input-group-btn">';
            html += '<button type="button" class="btn btn-primary" id="choose-port"><i class="fa fa-list"></i></button> \
                              </div> \
                              <input class="form-control" type="text" name="table_search" class="form-control pull-right" id="targetport-0" disabled="disabled" style="width: 70px;"> \
                            </div> \
                        </td> \
                        <td><input class="form-control" style="width:300px" value="" id="targetasset-0" disabled="disabled"/></td>\
                        <td><input class="form-control" style="width:80px" value="" id="targettype-0" disabled="disabled"/></td> \
                        <td><input class="form-control" style="width:300px" value="" /></td> \
                        <td style="display:none"><input type="text" value="0" /></td> \
                        <td style="display:none"><input type="text" id="targetid-0" value="0" /></td> \
                        <td> \
                            <button type="button" href="#" class="btn btn-box-tool" id="editMap"><span class="fa fa-check"></span></button> \
                            <button type="button" href="#" class="btn btn-box-tool" id="delMap"><span class="fa fa-remove"></span></button> \
                        </td> \
                    </tr>';
            $("#portmap").append(html);
        },
        delPort: function (e) {
            //删除板卡端口
            var port_id = $(e.currentTarget).parent().prev().children()[0].value;
            if(!port_id){
                var tr = $(e.target).closest('tr');
                tr.remove();
            }else{
                var data = {"action":"delete",
                    "value":{"id":port_id },
                    "table": "PortList"
                };
                var port_model = new this.model();
                port_model.url = "/cmdb/basedata/";
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
                        port_model.set("data", data);
                        port_model.save();
                        var tr = $(e.target).closest('tr');
                        tr.remove();
                    }
                );

            }

        },
        editPort: function (e) {
            //添加或编辑板卡的端口
            var tds = $(e.currentTarget).parent().siblings();
            var portname = $(tds[0]).find("input")[0].value;
            var porttype = $(tds[1]).find("input")[0].value;
            var vlan = $(tds[2]).find("input")[0].value;
            var remark = $(tds[3]).find("input")[0].value;
            var portid = $(tds[4]).find("input")[0].value;
            var data = {};
            var port_tags = $(e.currentTarget).parent().parent().siblings().find("td:eq(0)");
            var portlist = [];
            $.each(port_tags, function (index, tag) {
                portlist.push(tag.value);
            })
            var has_port = portlist.indexOf(portname);
            if(has_port > -1){
                swal({title: "",
                    text: '端口"'+portname+'"已存在!',
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true}
                );
                return false;
            }
            if(!portname){
                swal({title: "",
                    text: "请输入有效端口!",
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true}
                );
                return false;
            }
            var action = portid?"edit":"new";
            if(action == "new"){
                data = {"action":action,
                    "table":"PortList",
                    "value":{
                        "object_pk":this.card_id,
                        "portname":portname,
                        "porttype":porttype,
                        "flag":2,
                        "vlan":vlan,
                        "remark": remark,
                    },
                }
            }else{
                data = {
                    "action": action,
                    "table":"PortList",
                    "value": {
                        "id": portid,
                        "portname": portname,
                        "porttype": porttype,
                        "vlan": vlan,
                        "remark": remark,
                    },
                }
            }
            var port_model = new this.model();
            port_model.url = "/cmdb/basedata/";
            port_model.set("data", data);
            port_model.save({},{success:function (model, response) {
                if(!portid){
                    $(tds[4]).find("input")[0].value = response.data.id;
                }
            }});
        },
        delMap: function (e) {
            //删除端口映射
            var map_id = $(e.currentTarget).parent().prev().prev().children()[0].value;
            if(map_id === "0"){
                var tr = $(e.target).closest('tr');
                tr.remove();
            }else{
                var data = {"action":"delete",
                    "value":{"id":map_id },
                };
                var map_model = new this.model();
                map_model.url = "/cmdb/modifyportmap/";
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
                        map_model.set("data", data);
                        map_model.save({}, {success:function () {

                        }});
                        var tr = $(e.target).closest('tr');
                        tr.remove();
                    }
                );

            }

        },
        editMap: function (e) {
            //添加或编辑板卡的映射
            var tds = $(e.currentTarget).parent().siblings();
            var localport = $(tds[0]).find("input")[0].value;
            var targetport = $(tds[1]).find("input")[0].value;
            var targetasset = $(tds[2]).find("input")[0].value;
            var targetporttype = $(tds[3]).find("input")[0].value;
            var remark = $(tds[4]).find("input")[0].value;
            var portmap_id = $(tds[5]).find("input")[0].value;
            var targetport_id = $(tds[6]).find("input")[0].value;
            var data = {};
            var action = portmap_id==0?"new":"edit";

            if(!localport || !targetport){
                swal({title: "",
                    text: "映射端口不可为空!",
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true}
                );
                return false;
            }
            data = {"action":action,
                "value":{
                    "card_id":this.card_id,
                    "portname":localport,
                    "remark":remark
                },
            }
            if(action == "new"){
                data["value"]["targetport_id"] = $("#currChoose").attr("targetportid")
            }else{
                data["id"] = portmap_id;
                data["value"]["targetport_id"] = targetport_id;
            }
            var portmap_model = new this.model();
            portmap_model.url = "/cmdb/modifyportmap/";
            portmap_model.set("data", data);
            portmap_model.save({},{success:function (model, response) {
                if(response.status == true){
                    var portmap = $(tds[5]).find("input")[0];
                    var targetport = $(tds[6]).find("input")[0];
                    if(portmap_id === "0"){
                        $(portmap).attr("value", response.data.id);
                        $(targetport).attr("id", "targetid-"+response.data.targetport_id);
                        $(targetport).attr("value", response.data.targetport_id);
                        $(tds[0]).find("input")[0].disabled = true;
                    }
                }else{
                    swal({ title: response.info,
                        type: response.category,
                        timer: 1500,
                        showConfirmButton: false
                    });
                }


            }, async:false});
        },
        render: function () {
            var selected_card_id = this.card_id;
            $(this.collection.toJSON()[0].card).each(function (index, card) {
                if(card.id == selected_card_id){
                    selected_card = card;
                    return;
                }
            })
            this.$el.html(this.template({"card":selected_card}));
            return this;
        }
    });


    var HostCardDetailView = Backbone.View.extend({
        className: "",
        tagName: "div",
        template: _.template(HostCardDetailTemplate),
        events: {
            "click #add-port": "addPort",
            "click #del-port": "delPort",
            "click #edit-port": "editPort",
            "click #history-back": "historyBack",
        },
        initialize: function (options) {
            this.model = options.model;
            this.collection = options.collection;
            this.url = options.url;
            this.sid = options.sid;
            this.card_id = options.card_id;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        addPort: function (e) {
            //添加板卡端口
            var html = "<tr>";
            html += '<td style="width:100px"><input class="form-control input-sm"  value=""  /></td>';
            html += '<td style="width:150px"><input class="form-control input-sm"  value="" /></td>';
            html += '<td style="width:80px"><input class="form-control input-sm"  value="" /></td>';

            html += '<td style="width:150px">';
            html += ' <input type="text" name="table_search"  class="form-control input-sm" id="targetport-0" disabled="disabled"> \
                        </td> \
                        <td style="width:180px"><input class="form-control input-sm"  value="" id="targetasset-0" disabled="disabled"/></td>\
                        <td style="width:150px"><input class="form-control input-sm"  value="" id="targettype-0" disabled="disabled"/></td> \
                        <td style="width:200px"><input class="form-control input-sm"  value="" /></td> \
                        <td style="display:none"><input type="text" /></td> \
                        <td style="width:100px"> \
                            <button type="button" href="#" class="btn btn-box-tool" id="edit-port"><span class="fa fa-check"></span></button> \
                            <button type="button" href="#" class="btn btn-box-tool" id="del-port"><span class="fa fa-remove"></span></button> \
                        </td> \
                    </tr>';
            $("#portmap").append(html);
        },
        delPort: function (e) {
            //删除板卡端口
            var port_id = $(e.currentTarget).parent().prev().children()[0].value;
            if(!port_id){
                var tr = $(e.target).closest('tr');
                tr.remove();
            }else{
                var data = {"action":"del",
                    "value":{"id":port_id },
                    "table": "PortList"
                };
                var portmap_model = new this.model();
                portmap_model.url = "/cmdb/basedata/";
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
                        portmap_model.set("data", data);
                        portmap_model.save();
                        var tr = $(e.target).closest('tr');
                        tr.remove();
                    }
                );

            }

        },
        editPort: function (e) {
            //添加或编辑板卡的端口映射
            var tds = $(e.currentTarget).parent().siblings();
            var portname = $(tds[0]).find("input")[0].value;
            var porttype = $(tds[1]).find("input")[0].value;
            var vlan = $(tds[2]).find("input")[0].value;
            var remark = $(tds[6]).find("input")[0].value;
            var portmap_id = $(e.currentTarget).parent().prev().children()[0].value;

            if(!portname){
                swal({title: "",
                    text: '请输入有效端口！',
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true}
                );
                return false;
            }
            var port_tags = $(e.currentTarget).parent().parent().siblings().find("input:eq(0)");
            var portlist = [];
            $.each(port_tags, function (index, tag) {
                portlist.push(tag.value)
            });
            var has_port = portlist.indexOf(portname);
            if(has_port > -1){
                swal({title: "",
                text: '端口"'+portname+'"已存在！',
                type: "warning",
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定",
                closeOnConfirm: true
                });
                return false;
            }
            var post_data = {};
            post_data["value"] = {};
            post_data["table"] = "PortList";
            var action = portmap_id?"edit":"new";
            post_data["action"] = action;
            post_data["value"] = {
                "portname":portname,
                "porttype":porttype,
                "flag":1,
                "vlan":vlan,
                "remark":remark,
                "object_pk":this.card_id
            }
            if(action == "edit"){
                post_data["value"]["id"] = portmap_id
            }
            var port_model = new this.model();
            port_model.url = "/cmdb/basedata/";
            port_model.set("data", post_data);
            port_model.save({},{success:function (model, response) {
                $(e.currentTarget).parent().prev().children()[0].value = response.data.id;
            }});
        },
        historyBack: function (e) {
            window.location.href = "/cmdb/server_host_detail/list?sid=" + this.sid;
        },
        render: function () {
            this.$el.html(this.template(this.collection.toJSON()[0]));
            return this;
        }
    });
    return {
        EquipmentCardDetailView: EquipmentCardDetailView,
        HostCardDetailView: HostCardDetailView,
    };
})