/**
 * Created by zengchunyun on 2016/9/28.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require("backbone");
    var IndexDashboardItemViewTemplate = require("text!./templates/index_dashboard_template.tpl");
    var IndexEventItemViewTemplate = require("text!./templates/index_event_template.tpl");
    var IndexTopDataItemViewTemplate = require("text!./templates/index_top_data_template.tpl");
    var IndexTopDataTableItemViewTemplate = require("text!./templates/index_top_data_table_template.tpl");

    //监控主页模版
    var IndexDashboardItemView = Backbone.View.extend({
        events: {},
        template: _.template(IndexDashboardItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    //监控主页告警信息模版
    var IndexEventItemView = Backbone.View.extend({
        events: {},
        tagName:"tbody",
        template: _.template(IndexEventItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    //监控主页TOP10信息模版
    var IndexTopDataItemView = Backbone.View.extend({
        events: {},
        tagName:"div",
        className:"col-md-6",
        template: _.template(IndexTopDataItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.item_key = options.name;
            this.item_value = options.value;
            this.unit = options.unit;
            this.html_id = options.html_id;
        },
        render: function () {
            var chart_data = _.map(this.item_value, function (data) {
                return data.unit == '%' ? (100 - data.value).toFixed(2) : data.value
            });
            var chart_category = _.map(this.item_value, function (data) {
                return data.host_name
            });
            this.$el.html(this.template({name: this.item_key, value: chart_data, chart_category: chart_category, unit: this.unit, html_id:this.html_id}));
            return this;
        }
    });

    //监控主页TOP10信息表格模版
    var IndexTopDataTableItemView = Backbone.View.extend({
        events: {},
        tagName:"div",
        className:"col-md-12",
        template: _.template(IndexTopDataTableItemViewTemplate),
        initialize: function (options) {
            this.item_key = options.name;
            this.item_value = options.value;
            this.unit = options.unit;
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template({item_value: this.item_value, name: this.item_key, unit: this.unit}));
            return this;
        }
    });

    return {
        IndexDashboardItemView: IndexDashboardItemView,
        IndexEventItemView: IndexEventItemView,
        IndexTopDataItemView: IndexTopDataItemView,
        IndexTopDataTableItemView: IndexTopDataTableItemView
    }
});