/**
 * Created by zengchunyun on 16/8/12.
 */
define(function (require, exports, module) {
    var Backbone = require('backbone');
    //自定义主机组model
    var GroupsModel = Backbone.Model.extend({
        defaults: function () {
            return {}
        }

    });
    //通用model
    var CommonModel = Backbone.Model.extend({
        parse: function (response) {
            return response
        }

    });
    return {
        GroupsModel: GroupsModel,
        CommonModel: CommonModel
    };
})