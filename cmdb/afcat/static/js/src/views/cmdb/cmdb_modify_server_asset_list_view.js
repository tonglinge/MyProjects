/**
 * Created by zhanghai on 2016/9/27.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    //引入服务器资产item view
    var ServerAssetItemView = require("./cmdb_modify_server_asset_item_view").ServerAssetItemView;

    //服务器资产view,页面渲染
    var CMDBView = Backbone.View.extend({
        events: {
            "click #submit-btn": "modifyServerAsset",
            "click #move-left": "moveLeft",
            "click #move-right": "moveRight",
            "change #usetype_id": "initAssetSubType",
            "click #assettype_id": "initAssetSubType",
            "change #datacenter": "selectMachineRoom",
            "click #datacenter": "changeBorderColor",
            "click #room_id": "changeBorderColor"
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.collection.url = options.url;
            this.model = options.options.model;
            this.module = options.options.type;
            this.listenTo(this.collection, 'reset', this.addAll);
            if(options.options.action == "clone"){
                this.action = "new";
            }else{
                this.action = options.options.action;
            }
            var data = {"action":this.action, "model":this.module};
            if(options.options.action !== "new"){
                this.sid = options.options.sid;
                data["sid"] = this.sid;
            }
            this.collection.fetchData(true, JSON.stringify(data));
        },
        addAll: function () {
            this.$el.find(".server-asset").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new ServerAssetItemView({model: model});
            $(".server-asset").append(view.render().el);
            this.init_baseasset(model);
        },
        init_baseasset: function (view_model) {
            var base_info = view_model.toJSON();
            var asset_info = base_info.asset_info;
            if(asset_info){
                var sn = asset_info.sn;
                var usetype_id = asset_info.usetype_id;
                var assettype_id = asset_info.assettype_id;
                var factory_id = asset_info.factory_id;
                var integrator_id = asset_info.integrator_id;
                var model = asset_info.model;
                var datacenter = asset_info.basedatacenter;
                var room_id = asset_info.room_id;
                var cabinet = asset_info.cabinet;
                var netarea_id = asset_info.netarea_id;
                var manageip = asset_info.manageip;
                var clusterinfo = asset_info.clusterinfo;
                var unitinfo = asset_info.unitinfo;
                var cpu = asset_info.cpu;
                var memory = asset_info.memory;
                var contact = asset_info.contact;
                var tradedate = asset_info.tradedate;
                var expiredate = asset_info.expiredate;
                var startdate = asset_info.startdate;
                var assetstatus_id = asset_info.assetstatus_id;
                var remark = asset_info.remark;
                var host_count = asset_info.host_count;
                $("#sn").val(sn);
                $("#usetype_id").val(usetype_id);
                $("#assettype_id").val(assettype_id);
                $("#factory_id").val(factory_id);
                $("#integrator_id").val(integrator_id);
                $("#model").val(model);
                $("#datacenter").val(datacenter);
                $("#room_id").val(room_id);
                $("#cabinet").val(cabinet);
                $("#netarea_id").val(netarea_id);
                $("#manageip").val(manageip);
                $("#clusterinfo").val(clusterinfo);
                $("#unitinfo").val(unitinfo);
                $("#cpu").val(cpu);
                $("#memory").val(memory);
                $("#contact").val(contact);
                $("#tradedate").val(tradedate);
                $("#expiredate").val(expiredate);
                $("#startdate").val(startdate);
                $("#remark").val(remark);
                $("#status").children("option[value='"+assetstatus_id+"']").attr("selected",true);
                $("#asset_host_count").text(host_count);
            }

        },
        changeBorderColor: function (e) {
            $(e.currentTarget).css("border","");
        },
        checkValid: function () {
            //修改服务器表单有效性检测

            var room_id = $("#room_id").val();
            var datacenter_id = $("#datacenter").val();
            var model = $("#model").val();
            var usetype_id = $("#usetype_id").val();
            var assettype_id = $("#assettype_id").val();

            if(!room_id || !datacenter_id || !model || !usetype_id || !assettype_id){
                if(!model){
                    $("#model").css("border","1px solid red");
                }

                if(!room_id){
                    $("#room_id").css("border","1px solid red");
                }

                if(!datacenter_id){
                    $("#datacenter").css("border","1px solid red");
                }

                if(!usetype_id){
                    $("#usetype_id").css("border","1px solid red");
                }

                if(!assettype_id){
                    $("#assettype_id").css("border","1px solid red");
                }

                $("#error-message").text("请填写完整信息");
                $("#error-message").css("color", "red");
                setTimeout(function () {
                    $("#error-message").text("");
                }, 3000);
                return false;
            }
            return true;
        },
        modifyServerAsset: function (e) {
            //编辑服务器资产
            this.checkValid();
            var post_data = {};
            var value = {};
            var asset_form = $("form").serializeArray();
            if(this.changeStauts() == false){
                swal({title: "",
                      text:"该资产包含 "+ $("#asset_host_count").text()+" 台主机,请迁移主机后再执行此操作!！",
                      type: 'warning',   timer: 5500,   showConfirmButton: true });
                return false;
            }
            $.each(asset_form, function (index, field) {
                if(field.name !== "q"){
                    value[field.name] = field.value;
                }
            });
            //sn号为必填项
            console.log(value)
            post_data["value"] = value;
            post_data["action"] = this.action;
            post_data["model"] = this.module;

            if(this.action == "edit"){
                post_data["value"]["id"] = this.sid;
            }
            //post请求添加或修改数据
            var asset_model = new this.model();
            asset_model.url = "/cmdb/assetmodify/";
            asset_model.set("data", post_data, {validate: true});
            if(this.checkValid()){
                asset_model.set("data", post_data);
                asset_model.save({}, {success:function (model, response) {
                    if(response.status == true){
                        if(response.info && response.info != "") {
                            swal({   title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                        }
                        window.location.href = "/cmdb/server_asset/list";
                    }else {
                        swal({ title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                    }
                }})
            }

        },
        initAssetSubType: function (e) {
            //服务器子分类初始化
            var tag = e.currentTarget;
            var baseasset_subtype = this.collection.toJSON()[0].baseassetsubtype;
            var selected_flag = $("#usetype_id option:selected").attr("flag");
            var usetype_id = $("#usetype_id").val();

            $(baseasset_subtype).each(function () {
                if(this.type_id == usetype_id){
                    var display = "";
                }else{
                    var display = "none";
                }
                $("#assettype_id option[value='"+ this.id + "']").css("display", display);

            });
            if (tag.id == "usetype_id") {
                $("#assettype_id").val("");
            }
        },
        selectMachineRoom: function () {
            //选择机房
            var datacenter = $("#datacenter").val();
            var machine_room = this.collection.toJSON()[0].basemachineroom;
            $(machine_room).each(function () {
                if(this.center_id == datacenter){
                    var display = "";
                }else{
                    var display = "none";
                }
                $("#room_id option[value=" + this.id + "]").css("display", display);
            });
            $("#room_id").val("-1")
            //this.selectCabinet();
        },
        selectCabinet: function () {
            //选择机柜
            var selected_room = $("#room_id").val();
            var cabinets = this.collection.toJSON()[0].baseassetcabinet;
            $(cabinets).each(function () {
                if(this.room_id == selected_room){
                    var display = "";
                }else{
                    var display = "none";
                }
                $("#cabinet_id option[value=" + this.id + "]").css("display", display);
            });
            $("#cabinet_id").val("-1");
        },
        changeStauts:function () {
            var contain_host_count = $("#asset_host_count").text();
            var choose_status = $("#status").children(":selected").attr("flag");
            if(choose_status == 1 && contain_host_count > 0 && this.action == "edit"){
                return false;
            }else{
                return true;
            }
        },
    });

    return CMDBView;
})
