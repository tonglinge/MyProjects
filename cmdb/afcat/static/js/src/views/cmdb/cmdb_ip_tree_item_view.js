/**
 * Created by zhanghai on 2017/02/04.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var IPTreeItemViewTemplate = require('text!./templates/cmdb_ip_tree_template.tpl');
    var IPTreeItemView = Backbone.View.extend({
        //tagName: "tr",
        template: _.template(IPTreeItemViewTemplate),
        events: {
        },
        initialize: function (options) {
            this.record = options.record;
            this.listenTo(this.record, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.record)
            this.$el.html(this.template(this.record));
            return this;
        }
    });

    return {
        IPTreeItemView: IPTreeItemView,
    };
})