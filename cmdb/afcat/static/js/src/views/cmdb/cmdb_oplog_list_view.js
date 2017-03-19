/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var OperationLogItemView = require("./cmdb_oplog_item_view").OperationLogItemView;
    var CMDBPaginationView = require("./cmdb_pagination_view").PaginationView;
    var CMDBView = Backbone.View.extend({
        events: {
            "click #search_submit": "searchData",
            "click .paginate_button": "changePage",
            "click #log-refresh": "logRefresh"
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.collection.url = options.url;
            this.module = options.options.type;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'all', this.render);
            this.listenTo(this.collection, 'reset', this.paginator);

            var form_data = {page: this.page, method: "cmdb.reportindex.audit"};
            this.collection.fetchData(true, form_data);
            var self = this;
        },
        logRefresh: function (e) {
           var form_data = {page: 1, method: "cmdb.reportindex.audit"};
            this.collection.fetchData(true, form_data);
        },
        addAll: function () {
            this.$el.find(".oplog-body").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            console.log("model:", model.toJSON())
            var oplogs = model.toJSON();
            $.each(oplogs.record, function (index, oplog) {
                var view = new OperationLogItemView({oplog:oplog});
                $(".oplog-body").append(view.render().el);
            })

        },
        exportExcel: function (e) {
            $("#search-form").submit()
        },
        searchData: function (e) {
            //搜索数据
            var curr_page = e.currentTarget.id;
            var formData = {};
            var formData = {method: "cmdb.reportindex.audit", "page":1};
            var search_value = $('#search_value').val();
            formData["condition"] = search_value;

            //$(".asset-body").remove();
            console.log("formData:", formData)
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, formData);
        },
        paginator: function (model) {
            //页面分页
            var view = new CMDBPaginationView({model: model});
            $("#pagination").html(view.render().el);
        },
        changePage: function (e) {
            //切换分页
            var curr_page = e.currentTarget.id;
            var formData = {method: "cmdb.reportindex.audit", "page":curr_page};
            var search_value = $('#search_value').val();
            if(search_value){
                formData["condition"] = search_value;
            }
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, formData);
        },

    });

    return CMDBView;
})
