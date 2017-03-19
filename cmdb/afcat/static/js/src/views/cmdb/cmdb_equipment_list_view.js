/**
 * Created by zhanghai on 2016/10/21.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var EquipmentItemView = require("./cmdb_equipment_item_view").ServerAssetItemView;
    var CMDBPaginationView = require("./cmdb_pagination_view").PaginationView;
    var CMDBView = Backbone.View.extend({
        events: {
            "click #search_submit": "searchData",
            "click .paginate_button": "changePage",
            "click #export_equipment": "exportExcel",
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
            this.fetchLabel();
            this.collection.url = options.url;
            this.collection.fetchData(true, JSON.stringify({"page":1, "model":this.module}));
        },
        fetchLabel: function(){
            this.collection.url = "/api/v1/afcat/";
            var request_data = {
                models: "Equipment"
            };
            this.collection.fetchData(false, JSON.stringify(request_data), {async:false, method:"cmdb.tableproperty.load_filed_alias"});
            var labels = this.collection.toJSON()[0];
            console.log("labels:", labels)
            if(labels){
                this.loadLabel(labels);
            }

        },
        loadLabel: function (labels) {
            //加载table head
            $("#equipment-label").empty();
            $("#equipment-label").append("<th>" + labels.Equipment.assetname +"</th>");
            $("#equipment-label").append("<th>" + labels.Equipment.usetype +"</th>");
            $("#equipment-label").append("<th>" + labels.Equipment.netarea_id +"</th>");
            $("#equipment-label").append("<th>" + labels.Equipment.room_id +"</th>");
            $("#equipment-label").append("<th>" + labels.Equipment.cabinet +"</th>");
            $("#equipment-label").append("<th>" + labels.Equipment.slotindex +"</th>");
            $("#equipment-label").append("<th>" + labels.Equipment.model +"</th>");
            $("#equipment-label").append("<th>" + labels.Equipment.manageip +"</th>");
            $("#equipment-label").append("<th>" + labels.R_Equipment_Staff.staff_id +"</th>");
            $("#equipment-label").append("<th>操作</th>");
        },
        check_perm: function (el, permission) {
            var display = permission?"":"none";
            $(el).css("display", display);
        },
        addAll: function () {
            this.$el.find(".equipment-body").html('');
            this.collection.each(this.addOne, this)
        },
        addOne: function (model) {
            var parse_model = model.toJSON();
            var records = parse_model.record;
            var addperm = parse_model.addperm;
            this.check_perm("#btn_add_equipment", addperm);
            this.check_perm(".clone-equipment", addperm);
            this.$el.find(".equipment-body").html('');
            var equipment_model = this.model;
            $.each(records, function (index, record) {
                var view = new EquipmentItemView({record: record, model:equipment_model});
                $(".equipment-body").append(view.render().el);
            })
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
            //导出Excel
            $("#search-form").submit();
        },
        searchData: function (e) {
            //获取搜索设备资产表单数据
            var formData = {};
            var formData = {"model":this.module, "page":this.page};
            var search_value = $('#search_value').val();
            formData["condition"] = search_value;

            this.$el.find(".server-body").html('');
            var curr_page = e.currentTarget.id;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, JSON.stringify(formData));
        },
        paginator: function (model) {
            //页面分页
            //console.log(model.toJSON()[0].curr_page)
            var view = new CMDBPaginationView({model: model});
            $("#pagination").html(view.render().el);
        },
        changePage: function (e) {
            //切换分页
            this.$el.find(".server-body").html('');
            var curr_page = e.currentTarget.id;
            var formData = {"model":this.module, "page":curr_page};
            var search_value = $('#search_value').val();
            if(search_value){
                formData["condition"] = search_value;
            }
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, JSON.stringify(formData));
        },
    });

    return CMDBView;
})
