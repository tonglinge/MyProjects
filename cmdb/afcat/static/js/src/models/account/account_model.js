/**
 * Created by super on 2016/10/21.
 */

define(function (require, exports, module) {
    var Backbone = require("backbone");
    //所有权限的公用model, 都包含name和 不同权限的
    var PermCommonModel = Backbone.Model.extend({
        defaults: function () {
            return {
                name:"",
                view:0,
                change:0,
                deleted:0,
                url:""
            }
        },
        parse: function (response) {
            if(response.info && response.info != "") {
                    swal({ title: "", text: response.info, type: response.category, timer: 1500, showConfirmButton: false, alertType: response.category});
                }
            if(typeof response.data != "undefined"){
                // console.log("Here is Data:", response.data);
                return response.data;
            }else {
                return response;
            }
        },

    });

    //用户model
    var PermUserModel = Backbone.Model.extend({
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
        PermModel: PermCommonModel,
        UserModel: PermUserModel
    };
});