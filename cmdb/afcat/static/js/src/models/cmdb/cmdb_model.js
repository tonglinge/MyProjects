/**
 * Created by zengchunyun on 16/8/12.
 */
define(function (require, exports, module) {
    var Backbone = require('backbone');

    //服务器资产model
    var AssetModel = Backbone.Model.extend({
        default: function () {
        },
        parse: function (response) {
            if(response.status == true && typeof response.category != "undefined"){
                if(response.info && response.info != "") {
                    swal({ title: response.info, type: response.category, timer: 1000, showConfirmButton: false, alertType: response.category});
                }

            }
            // return response;
            if(typeof response.data != "undefined"){
                // console.log("Here is Data:", response.data);
                return response.data;
            }else {
                return response;
            }
        },
    });

    //主机model
    var HostModel = Backbone.Model.extend({
        parse: function (response) {
            if(response.status == true && typeof response.category != "undefined"){
                if(response.info && response.info != "") {
                    swal({ title: response.info, type: response.category, timer: 1000, showConfirmButton: false, alertType: response.category});
                }

            }
            // return response;
            if(typeof response.data != "undefined"){
                // console.log("Here is Data:", response.data);
                return response.data;
            }else {
                return response;
            }
        },
    });

    //网络设备model
    var EquipmentModel = Backbone.Model.extend({
        parse: function (response) {
            if(response.status == true && typeof response.category != "undefined"){
                if(response.info && response.info != "") {
                    swal({ title: response.info, type: response.category, timer: 1000, showConfirmButton: false, alertType: response.category});
                }

            }
            // return response;
            if(typeof response.data != "undefined"){
                // console.log("Here is Data:", response.data);
                return response.data;
            }else {
                return response;
            }
        },
    });
    return {
        AssetModel: AssetModel,
        HostModel: HostModel,
        EquipmentModel: EquipmentModel,
    }
})