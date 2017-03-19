/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var EquipmentDetailItemViewTemplate = require('text!./templates/equipment_detailinfo_template.tpl');
    var EquipmentDetailItemView = Backbone.View.extend({
        className: "equipment-detail-record",
        tagName: "div",
        template: _.template(EquipmentDetailItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.model.toJSON());
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return {
        EquipmentDetailItemView: EquipmentDetailItemView,
    };
})