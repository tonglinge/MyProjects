/**
 * Created by zengchunyun on 2016/10/19.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var ReportDefaultItemViewTemplate = require("text!./templates/report_default_template.tpl");

    //获取主机菜单列表
    var ReportDefaultItemView = Backbone.View.extend({
        events: {},
        tagName: "tr",
        template: _.template(ReportDefaultItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return {
        ReportDefaultItemView: ReportDefaultItemView
    }
});