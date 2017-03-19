/**
 * Created by zengchunyun on 2016/11/16.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var EventsItemViewTemplate = require("text!./templates/events_template.tpl");

    //监控主页模版
    var EventsItemView = Backbone.View.extend({
        tagName: "tr",
        events: {},
        template: _.template(EventsItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return {
        EventsItemView: EventsItemView
    }
});