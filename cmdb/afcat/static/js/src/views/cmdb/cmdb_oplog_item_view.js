/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var OperationLogItemViewTemplate = require('text!./templates/cmdb_oplog_template.tpl');
    var OperationLogItemView = Backbone.View.extend({
        tagName: "tr",
        template: _.template(OperationLogItemViewTemplate),
        events: {
        },
        initialize: function (options) {
            this.oplog = options.oplog;
            this.listenTo(this.oplog, 'destroy', this.remove);
        },
        render: function () {
            console.log("oplog:", this.oplog)
            this.$el.html(this.template(this.oplog));
            return this;
        }
    });

    return {
        OperationLogItemView: OperationLogItemView,
    };
})