/**
 * Created by zengchunyun on 2016/11/16.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var IndexItemViewTemplate = require("text!./templates/index_template.tpl");

    //监控主页模版
    var IndexItemView = Backbone.View.extend({
        tagName: "div",
        events: {},
        className:"box-body",
        template: _.template(IndexItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return {
        IndexItemView: IndexItemView
    }
});