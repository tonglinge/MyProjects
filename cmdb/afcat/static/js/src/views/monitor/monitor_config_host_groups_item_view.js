/**
 * Created by zengchunyun on 2016/10/8.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var ConfigHostGroupsItemViewTemplate = require("text!./templates/config_host_groups_template.tpl");

    //监控主页模版
    var ConfigHostGroupsItemView = Backbone.View.extend({
        tagName: "tr",
        events: {},
        template: _.template(ConfigHostGroupsItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return {
        ConfigHostGroupsItemView: ConfigHostGroupsItemView
    }
});