/**
 * Created by super on 2016/10/27.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var PermUserslistItemViewTemplate = require("text!./templates/account_user_list.tpl");
    // 用户列表模版
    var PermUserslistItemView = Backbone.View.extend({
        tagName: "tr",
        events: {},
        template: _.template(PermUserslistItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            // console.log(this.template());
            this.$el.html(this.template({user:this.model}));
            return this;
        }
    });

    return {
        PermUserslistItemView: PermUserslistItemView
    }
});