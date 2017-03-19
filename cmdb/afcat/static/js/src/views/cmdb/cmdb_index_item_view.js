/**
 * Created by zengchunyun on 2016/11/16.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");

    //审计模板
    var IndexItemView = Backbone.View.extend({
        events: {},
        initialize: function (options) {
            // this.tagName = options.tagname;
            // this.className = options.classname,
            // this.model = options.model;
            this.template = _.template(options.template);
        },
        attributes:{},
        render: function () {
            var model = this.model.toJSON();
            // console.log("model:", model)
            this.$el.html(this.template(model));
            return this;
        }
    });
    return {
        IndexItemView: IndexItemView
    }
});