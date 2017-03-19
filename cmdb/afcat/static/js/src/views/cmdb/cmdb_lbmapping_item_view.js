/**
 * Created by super on 2017/2/9.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var BalanceMappingTemplate = require("text!./templates/cmdb_lbmapping_template.tpl");
    var BalanceMappingDetailTemplate = require("text!./templates/cmdb_lbmapping_detail_template.tpl");
    var BalanceMappingEditTemplate = require("text!./templates/cmdb_lbmapping_edit_template.tpl");

    //显示所有记录模版
    var BalanceMappingItemView = Backbone.View.extend({
        tagName: "tr",
        events: {},
        template: _.template(BalanceMappingTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            // var model_to_json= this.model.toJSON();
            this.$el.html(this.template(this.model));
            return this;
        }
    });
    //显示详情渲染模板
    var BalanceMappingDetailItemView = Backbone.View.extend({
        tagName: "tbody",
        template: _.template(BalanceMappingDetailTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model));
            return this;
        }

    });
    //添加和编辑渲染模板
    var BalanceMappingEditItemView = Backbone.View.extend({
        tagName: "tbody",
        template: _.template(BalanceMappingEditTemplate),
        initialize: function (options) {
            this.model = options.model; //需要用到基表数据,这里传过来基表的数据
        },
        render: function () {
            this.$el.html(this.template(this.model));
            return this;
        }
    });

    return {
        BalanceMappingItemView: BalanceMappingItemView,
        BalanceMappingDetailItemView: BalanceMappingDetailItemView,
        BalanceMappingEditItemView: BalanceMappingEditItemView
    }
});