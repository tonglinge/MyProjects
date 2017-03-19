/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var ServerAssetItemView = require("./cmdb_server_asset_item_view").ServerAssetItemView;
    var CMDBPaginationView = require("./cmdb_pagination_view").PaginationView;
    var CMDBView = Backbone.View.extend({
        events: {
            "click #search_submit": "searchData",
            "click .paginate_button": "changePage",
            "click #export_server_asset": "exportExcel",
            "change .toggle-vis": "toggleColumn"
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

            var form_data = JSON.stringify({page: this.page, model: this.module});
            this.collection.fetchData(true, form_data);
        },
        addAll: function () {
            this.$el.find(".asset-body").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var server_asset_model = model.toJSON();
            var records = server_asset_model.record;
            var addperm =server_asset_model.addperm;
            var assettypelist = server_asset_model.baseassettype;
            var asset_module = this.module;
            var asset_model = this.model;
            $.each(records, function (index, record) {
                var view = new ServerAssetItemView({record: record, module:asset_module, model:asset_model});
                $(".asset-body").append(view.render().el);
            });
            this.fillAssetTypeSelect(assettypelist);
            this.check_perm("#btn_add_server_asset", addperm);
            this.check_perm(".clone-server-asset", addperm);
        },
        toggleColumn: function (e) {
            //自定义显示或者隐藏列
            var is_checked = $(e.currentTarget).get(0).checked;
            var column_index = $(e.currentTarget).attr("data-column");
            console.log($(e.currentTarget).find("tr").children("th").eq(column_index))
            if(is_checked){
                console.log($(".asset-table").find("tr").find("th"))
                $(".asset-table").find("tr").each(function () {
                    $(this).children("th").eq(column_index).hide();
                });
                $(".asset-table").find("tr").each(function () {
                    $(this).children("td").eq(column_index).hide();
                });
            }else{
                $(".asset-table").find("tr").each(function () {
                    $(this).children("th").eq(column_index).show();
                });
                $(".asset-table").find("tr").each(function () {
                    $(this).children("td").eq(column_index).show();
                });
            }
        },
        fillAssetTypeSelect: function (assettype_models) {
            $(".search_key").empty();
            $(".search_key").append("<option value='-1'>所有设备</option>");
            $.each(assettype_models, function (index, model) {
                $(".search_key").append("<option value='" + model.id + "'>" + model.name + "</option>");
            });
        },
        exportExcel: function (e) {
            $("#search-form").submit()
        },
        check_perm: function (el, permission) {
            var display = permission?"":"none";
            $(el).css("display", display);
        },
        searchData: function (e) {
            //获取搜索服务器资产表单数据
            var formData = {};
            var formData = {"model":this.module, "page":curr_page};
            var search_key = $(".search_key").find("option:selected").val();
            var search_value = $('#search_value').val();
            formData["condition"] = {"type":search_key, "content": search_value};

            //$(".asset-body").remove();
            var curr_page = e.currentTarget.id;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, JSON.stringify(formData));
        },
        paginator: function (model) {
            //页面分页
            var view = new CMDBPaginationView({model: model});
            $("#pagination").html(view.render().el);
        },
        changePage: function (e) {
            //切换分页

            var curr_page = e.currentTarget.id;
            var formData = {"model":this.module, "page":curr_page};
            var search_key = $(".search_key").find("option:selected").val();
            var search_value = $('#search_value').val();
            if(search_value){
                formData["condition"] = {"key":search_key, "value": search_value};
            }
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, JSON.stringify(formData));
        },

    });

    return CMDBView;
})
