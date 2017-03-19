/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var ImportExcelItemViewTemplate = require('text!./templates/import_excel_template.tpl');
    var ImportExcelItemView = Backbone.View.extend({
        //tagName: "",
        template: _.template(ImportExcelItemViewTemplate),
        events: {
        },
        initialize: function (options) {
            this.listenTo(this.record, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.record)
            this.$el.html(this.template());
            return this;
        }
    });

    return {
        ImportExcelItemView: ImportExcelItemView,
    };
})