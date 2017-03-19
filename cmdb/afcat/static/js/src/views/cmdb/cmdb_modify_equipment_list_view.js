/**
 * Created by zhanghai on 2016/9/27.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    //引入服务器资产item view
    var EquipmentItemView = require("./cmdb_modify_equipment_item_view").EquipmentItemView;

    //服务器资产view,页面渲染
    var CMDBView = Backbone.View.extend({
        events: {
            "click .submit-btn": "modifyEquipment",
            "change #datacenter": "selectMachineRoom",
            //"change #machineroom": "selectCabinet",
            "blur .must-input": "checkValid",
            "click .must-input": "backBorderColor"
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.collection.url = options.url;
            this.model = options.options.model;
            this.module = "equipment";
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
            this.$el.find(".equipment").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new EquipmentItemView({model: model});
            $(".equipment").append(view.render().el);
            this.init_baseasset(model);
        },
        init_baseasset: function (view_model) {
            var base_info = view_model.toJSON();
            var asset_info = base_info.asset_info;
            if(asset_info){
                var assetname = asset_info.assetname;
                var serialno = asset_info.sn;
                var assettype = asset_info.assettype;

                var datacenter = asset_info.datacenter;
                var room = asset_info.room;
                var cabinet = asset_info.cabinet;

                var tradedate = asset_info.tradedate;
                var expiredate = asset_info.expiredate;
                var slotindex = asset_info.slotindex;

                var factory = asset_info.factory;
                var porvider = asset_info.provider;
                var serviceprovider = asset_info.serviceprovider;
                var model = asset_info.model;
                var netarea = asset_info.netarea;

                var portcount = asset_info.portcount;
                var manageip = asset_info.manageip;
                var status = asset_info.status;
                var powertype = asset_info.powertype;
                var usetype = asset_info.usetype;
                var remark = asset_info.remark;

                var customers = $(".customer");
                $(customers).each(function (index, customer) {
                    var customer_key = $(customer).attr("name");
                    var customer_value = asset_info[customer_key];
                    $(customer).val(customer_value);
                });

                //选中设备分类
                $("#equipmenttype option[value="+ assettype + "]").attr("selected", true);

                //选中厂商
                // $("#factory option[value="+ factory + "]").attr("selected", true);
                $("#factory").val(factory);

                //选中供应商
                $("#provider").val(provider);

                //选中服务提供商
                $("#serviceprovider").val(serviceprovider);

                //选择数据中心
                $(base_info.basedatacenter).each(function () {
                    if(this.id == datacenter){
                        $("#datacenter option[value='" + this.id + "']").attr("selected", true);
                    }
                });

                //选中机房
                $("#machineroom option[value=" + room + "]").attr("selected", true);

                //选中机柜
                //$("#cabinet option[value="+ cabinet + "]").attr("selected", true);
                $("#cabinet").val(cabinet);

                //选中环境
                $("#netarea option[value="+ netarea + "]").attr("selected", true);


                //选中状态
                $("#asset_status").val(status);

                $("#assetname").val(assetname);
                $("#sn").val(serialno);
                $("#model").val(model);
                $("#slotindex").val(slotindex);
                $("#powertype").val(powertype);
                $("#usetype").val(usetype);
                $("#tradedate").val(tradedate);
                $("#expiredate").val(expiredate);

                $("#portcount").val(portcount);
                $("#manageip").val(manageip);
                $("#remark").val(remark);
            }

        },
        checkValid: function (e) {
            var message = "请输入有效值！"
            if(!e.currentTarget.value){
                $(e.currentTarget).css("border","1px solid red");
                $("#error-message").html("<b>"+message+"</b>");
                $("#error-message").css("color", "red");
                setTimeout(function () {
                    $("#error-message").text("");
                }, 3000)
            }
            return;
        },
        backBorderColor: function (e) {
            $(e.currentTarget).css("border","");
        },
        modifyEquipment: function (e) {
            //编辑设备资产
            var operation = e.currentTarget.id;
            var data = {};
            var value = {};
            var assetname = $("#assetname").val();
            var sn = $("#sn").val();
            var equipmenttype = $("#equipmenttype").val();

            var datacenter = $("#datacenter").val();
            var machine_room = $("#machineroom>option:selected").val();
            var cabinet = $("#cabinet").val();

            var tradedate = $("#tradedate").val();
            var expiredate = $("#expiredate").val();
            var slotindex = $("#slotindex").val();

            var factory = $("#factory>option:selected").val();
            var provider = $("#provider").val();
            var serviceprovider = $("#serviceprovider").val();
            var model = $("#model").val();
            var netarea = $("#netarea>option:selected").val();

            var portcount = $("#portcount").val();
            var manageip = $("#manageip").val();
            var asset_status = $("#asset_status>option:selected").val();
            var powertype = $("#powertype").val();
            var usetype = $("#usetype").val();
            var remark = $("#remark").val();

            var message = "请输入有效值！";
            if(!assetname){
                $("#assetname").css("border","1px solid red");
                $("#error-message").html("<b>"+message+"</b>");
                $("#error-message").css("color", "red");
                setTimeout(function () {
                    $("#error-message").text("");
                }, 3000)
                return;
            }
            if(!slotindex){
                $("#slotindex").css("border","1px solid red");
                $("#error-message").html("<b>"+message+"</b>");
                $("#error-message").css("color", "red");
                setTimeout(function () {
                    $("#error-message").text("");
                }, 3000)
                return;
            }
            if(!model){
                $("#model").css("border","1px solid red");
                $("#error-message").html("<b>"+message+"</b>");
                $("#error-message").css("color", "red");
                setTimeout(function () {
                    $("#error-message").text("");
                }, 3000)
                return;
            }
            if(!cabinet){
                $("#model").css("border","1px solid red");
                $("#error-message").html("<b>"+message+"</b>");
                $("#error-message").css("color", "red");
                setTimeout(function () {
                    $("#error-message").text("");
                }, 3000)
                return;
            }
            //asset数据
            value = {"manageip": manageip,
                "remark": remark,
                "assetname": assetname,
                "model": model,
                "cabinet": cabinet,
                "assettype_id": equipmenttype,
                "sn": sn,
                "tradedate": tradedate,
                "expiredate": expiredate,
                "factory_id":factory,
                "provider": provider,
                "serviceprovider": serviceprovider,
                "slotindex": slotindex,
                "portcount": portcount,
                "room_id": machine_room,
                "netarea_id": netarea,
                "status_id": asset_status,
                "powertype": powertype,
                "usetype": usetype,
                "id":this.sid
            };

            var customers = $(".customer");
            $(customers).each(function (index, customer) {
                var customer_key = $(customer).attr("name");
                var customer_value = $(customer).val();
                value[customer_key] = customer_value;
            });

            data = {"value":value, "action":this.action, "model":this.module};
            console.log("data:", data)
            var equipment_id = this.sid;
            //post请求添加或修改数据
            var equipment_model = new this.model();
            equipment_model.url = "/cmdb/assetmodify/";
            equipment_model.set("data", data);
            equipment_model.save({}, {success:function (model, response) {
                if(response.status == true){
                    if(response.info && response.info != "") {
                        swal({   title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                    }
                    if(operation === "save-and-add"){
                         window.location.href = "/cmdb/modify_equipment/list?action=new";
                    }else if(operation === "save-and-back"){
                        window.location.href = "/cmdb/equipment/list";
                    }else if(operation === "save-and-detail"){
                        var sid = equipment_id?equipment_id:response.data.id;
                        window.location.href = "/cmdb/equipment_detail/list?sid=" + sid;
                    }
                }else {
                    swal({ title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                }
            }});
        },
        selectMachineRoom: function () {
            var datacenter = $("#datacenter>option:selected").val();
            var machine_room = this.collection.toJSON()[0].basemachineroom;
            $("#machineroom").empty();
            for(var i=machine_room.length-1;i>=0;i--){
                if(machine_room[i].center_id == datacenter){
                    $("#machineroom").append("<option value='" + machine_room[i].id + "'>" + machine_room[i].name + "</option>")
                }
            }
        },
       selectCabinet: function () {
            var machine_room = $("#machineroom>option:selected").val();
            var cabinets = this.collection.toJSON()[0].baseassetcabinet;
            $("#cabinet").empty();
            for(var i=cabinets.length-1;i>=0;i--){
                if(cabinets[i].room_id == machine_room){
                    $("#cabinet").append("<option value='" + cabinets[i].id + "'>" + cabinets[i].numbers + "</option>")
                }
            }
        },
    });

    return CMDBView;
})
