/**
 * Created by zengchunyun on 2016/11/17.
 */
define(function (require, exports, module) {
    var Backbone = require('backbone');
    //通用model
    var CommonModel = Backbone.Model.extend({
        parse: function (response) {
            return response
        }

    });
    return {
        CommonModel: CommonModel
    };
})