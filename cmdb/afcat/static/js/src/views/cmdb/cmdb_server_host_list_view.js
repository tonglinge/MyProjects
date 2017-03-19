/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var ServerHostItemView = require("./cmdb_server_host_item_view").ServerHostItemView;
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
            this.search_key = "";
            this.listenTo(this.collection, 'reset', this.addAll);
            //this.listenTo(this.collection, 'all', this.render);
            this.listenTo(this.collection, 'reset', this.paginator);

            var form_data = JSON.stringify({page: this.page, model: this.module})
            this.collection.fetchData(true, form_data);
            this.loadHeader();
        },
        loadHeader: function (mode) {
            this.$el.find(".server-head").empty();
            this.$el.find(".server-foot").empty();
            if(mode == "sys"){
                var title = "<tr>\
                <th>应用系统名称</th>\
                <th>业务模块</th>\
                <th>主机名</th>\
                <th>主机类型</th>\
                <th>机柜</th>\
                <th>单元信息</th>\
                <th>联系人</th>\
                <th>型号</th>\
                <th>分区</th>\
                <th>网络域</th>\
                <th>备注</th>\
                <th>操作</th>\
                </tr>";
            }else{
                var title = "<tr>\
                <th>主机名</th>\
                <th>主机类型</th>\
                <th>业务模块</th>\
                <th>机柜</th>\
                <th>单元信息</th>\
                <th>联系人</th>\
                <th>型号</th>\
                <th>分区</th>\
                <th>网络域</th>\
                <th>备注</th>\
                <th>操作</th>\
                </tr>";
            }
            this.$el.find(".server-head").html(title);
        },
        addAll: function () {
            this.$el.find(".server-body").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var parse_model = model.toJSON();
            var records = parse_model.record;
            var addperm = parse_model.addperm;
            var asset_module = this.module;
            var asset_model = this.model;
            search_key = this.search_key;
            $.each(records, function (index, record) {
                var view = new ServerHostItemView({record: record, module:asset_module, model:asset_model, search_key:search_key});
                $(".server-body").append(view.render().el);
            });
            this.check_perm("#btn-add-server-host", addperm);
            this.check_perm(".clone-server-host", addperm);
        },
        toggleColumn: function (e) {
            //自定义显示或者隐藏列
            var is_checked = $(e.currentTarget).get(0).checked;
            var column_index = $(e.currentTarget).attr("data-column");
            console.log($(e.currentTarget).find("tr").children("th").eq(column_index))
            if(is_checked){
                console.log($(".server-table").find("tr").find("th"))
                $(".server-table").find("tr").each(function () {
                    $(this).children("th").eq(column_index).hide();
                });
                $(".server-table").find("tr").each(function () {
                    $(this).children("td").eq(column_index).hide();
                });
            }else{
                $(".server-table").find("tr").each(function () {
                    $(this).children("th").eq(column_index).show();
                });
                $(".server-table").find("tr").each(function () {
                    $(this).children("td").eq(column_index).show();
                });
            }
        },
        exportExcel: function (e) {
            $("#search-form").submit()
        },
        check_perm: function (el, permission) {
            var display = permission?"":"none";
            $(el).css("display", display);
        },
        searchData: function (e) {
            //搜索主机设备信息
            var formData = {};
            var formData = {"model":this.module, "page":curr_page};
            var search_key = $(".search_key").find("option:selected").val();
            var search_value = $('#search_value').val();
            formData["condition"] = {"key":search_key, "value": search_value};

            var curr_page = e.currentTarget.id;
            this.loadHeader(search_key);
            this.search_key = search_key;
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
