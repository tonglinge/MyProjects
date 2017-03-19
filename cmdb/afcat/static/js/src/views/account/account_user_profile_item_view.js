/**
 * Created by zengchunyun on 2016/12/5.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var UserProfileItemViewTemplate = require("text!./templates/settings_template.tpl");

    //监控主页模版
    var UserProfileItemView = Backbone.View.extend({
        tagName: "tr",
        events: {},
        template: _.template(UserProfileItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return {
        UserProfileItemView: UserProfileItemView
    }
});