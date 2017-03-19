/**
 * Created by zengchunyun on 2016/11/17.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var AdminIndexShowTablesItemViewTemplate = require("text!./templates/admin_index_show_tables_template.tpl");
    var AdminIndexShowRecordsItemViewTemplate = require("text!./templates/admin_index_show_records_template.tpl");

    //基表列表模版
    var AdminIndexShowTablesItemView = Backbone.View.extend({
        tagName: "ul",
        className: "nav nav-pills nav-stacked",
        events: {
            "click a": "getTableData"
        },
        template: _.template(AdminIndexShowTablesItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.parent_view = options.self;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        getTableData: function (e) {
            var table_name = e.currentTarget.getAttribute('data-model-name');
            var alias_name = e.currentTarget.getAttribute('data-table-alias');
            this.parent_view.collection.fetchData(true,{method:'cmdb.show.records', table_name: table_name});
            this.parent_view.$el.find('#table_name').html(alias_name);
            this.parent_view.$el.find('#table_name').attr('data-model-name', table_name);
            this.parent_view.$el.find('.add_record').attr("href","?target="+table_name);
            this.parent_view.$el.find('.mailbox-controls').removeClass('hide');
            this.parent_view.$el.find('.record_area').addClass('hide');
        }
    });

    //显示基表数据模版
    var AdminIndexShowRecordsItemView = Backbone.View.extend({
        tagName: "table",
        className: "table table-hover table-striped",
        events: {},
        template: _.template(AdminIndexShowRecordsItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.parent_view = options.self;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return {
        AdminIndexShowTablesItemView: AdminIndexShowTablesItemView,
        AdminIndexShowRecordsItemView: AdminIndexShowRecordsItemView
    }
});