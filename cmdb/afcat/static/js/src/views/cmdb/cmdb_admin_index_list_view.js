/**
 * Created by zengchunyun on 2016/11/17.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var AdminIndexShowTablesItemView = require("./cmdb_admin_index_item_view").AdminIndexShowTablesItemView;
    var AdminIndexShowRecordsItemView = require("./cmdb_admin_index_item_view").AdminIndexShowRecordsItemView;


    return Backbone.View.extend({
        events: {
            "click #add-data-btn": "addRecord",
            "click .add_record": "getFormPage",
            "click .return_record": "returnList",
            "click .trash_record": "removeRecord",
            "click .all_checkbox": "toggleCheckALL",
            "click .show_previous_page": "showPreviousPage",
            "click .show_next_page": "showNextPage",
            "click a[href*='target']": "getFormPage"
        },
        initialize: function (options) {
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, {method:'cmdb.show.tables'});
        },
        addAll: function () {
            var models = this.collection.models;
            //针对每次reload数据时需要清空整个app页面数据，指定判断关键属性，用来决定是否对app内容清空
            if(this.collection.reseted && models.length > 0 && models[0].has("tables_data")){
                this.$el.find('.tables_data').html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            if(model.has('models_list')){
                var showTablesItemView = new AdminIndexShowTablesItemView({model: model, self: this});
                this.$el.find(".show_tables").append(showTablesItemView.render().el);
            }
            if(model.has('tables_data')){
                this.$el.find('.record_area').removeClass('hide');
                var showRecordsItemView = new AdminIndexShowRecordsItemView({model: model, self: this});
                this.$el.find(".tables_data").html(showRecordsItemView.render().el);
                this.$el.find(".show_previous_page").toggleClass('disabled', !this.collection.has_previous);
                this.$el.find(".show_next_page").toggleClass('disabled', !this.collection.has_next);
                this.$el.find(".return_record").addClass('disabled');
                this.$el.find(".trash_record").removeClass('disabled');
                $('[data-record-id]').each(function () {
                    $(this).data('id', this.getAttribute("data-record-id"))
                });
            }
        },
        addRecord: function (e) {
            var form = {};
            form['method'] = 'cmdb.edit.record';
            var table_name = this.$el.find('#table_name').attr('data-model-name');
            var formData = this.$el.find(".tables_data form").serializeArray();
            var record_id = this.$el.find("#id_id").data("id");
            if(table_name != null){
                form['table_name'] = table_name;
            }
            for(var index in formData){
                var field_data = formData[index];
                if(field_data.name == "id"){
                    form[field_data.name] = record_id;
                }else {
                    form[field_data.name] = field_data.value;
                }
            }
            this.collection.fetchData(false, form,{type:'POST', append:false, error: this.formPage, args: this,update_page:false});
        },
        getFormPage: function (e) {
            var tag = e.currentTarget;
            var href = tag.getAttribute("href");
            var reg = new RegExp("(^|&)" + 'id' + "=([^&]*)(&|$)");
            var r = href.substr(1).match(reg);
            var id = r != null ? decodeURI(r[2]) : "";
            var table_name = this.$el.find('#table_name').attr('data-model-name');
            if(id == ""){
                this.$el.find(".trash_record").addClass('disabled');
            }else {
                this.$el.find(".trash_record").removeClass('disabled');
            }
            this.collection.fetchData(false, {method:'cmdb.edit.record', table_name: table_name, id:id},{type:'GET', append:false, error: this.formPage, args: this,update_page:false});
            return false
        },
        formPage: function (self, xhr, textStatus, errorThrown) {
            if(textStatus.status == 200){
                $(".tables_data").html(textStatus.responseText);
                self.$el.find(".return_record").removeClass('disabled');
                var record_id = self.$el.find("#id_id").val();
                self.$el.find("#id_id").data("id", record_id)
            }
            return false
        },
        toggleCheckALL: function (e) {
            var tag = e.currentTarget;
            var checked = tag.checked;
            this.$el.find(".record_checkbox").each(function () {
                $(this).prop("checked", checked)
            })
        },
        removeRecord: function (e) {
            var tag = e.currentTarget;
            var className = tag.getAttribute("class");
            if(className.indexOf('disabled') == -1){
                var self=this;
                var deleteRecordIDs = [];
                self.$el.find(".record_checkbox:checked").each(function () {
                    deleteRecordIDs.push(self.$el.find(this).data("id"))
                });
                self.$el.find("#id_id").each(function () {
                    deleteRecordIDs.push(self.$el.find("#id_id").data("id"))
                });
                var table_name = self.$el.find('#table_name').attr('data-model-name');
                if(deleteRecordIDs.length > 0){
                    swal({
                            title: "确定删除该服务器资产",
                            text: "删除后将无法恢复！",
                            type: "warning",
                            showCancelButton: true,
                            confirmButtonColor: "#DD6B55",
                            cancelButtonText: '取消',
                            confirmButtonText: "删除",
                            closeOnConfirm: false
                        },
                        function(){
                            self.collection.fetchData(false, {method:'cmdb.drop.records',records_id: JSON.stringify(deleteRecordIDs), table_name:table_name}, {success: self.removeRecordDom,args:self, update_page:false});
                        }
                    );
                }
            }
        },
        removeRecordDom: function (self, collection, response, options) {
            if(response.status){
                var delete_records = response.data;
                if(typeof self.$el.find("#id_id").data("id") != 'undefined'){
                    var table_name = self.$el.find('#table_name').attr('data-model-name');
                    self.collection.currentPage();
                    self.collection.fetchData(false,{method:'cmdb.show.records', table_name: table_name}, {success: function(self){self.collection.trigger("reset")}, args: self});
                }else {
                    self.$el.find(".record_checkbox:checked").each(function () {
                        var record_id = this.getAttribute("data-record-id");
                        if(delete_records.indexOf(record_id) != -1){
                            $(this).parents('tr').remove()
                        }
                    });
                }
            }
        },
        showPreviousPage: function (e) {
            var tag = e.currentTarget;
            var className = tag.getAttribute("class");
            if(className.indexOf('disabled') == -1){
                var table_name = this.$el.find('#table_name').attr('data-model-name');
                if(this.collection.has_previous){
                    this.collection.previousPage();
                    this.collection.fetchData(false,{method:'cmdb.show.records', table_name: table_name}, {success: function(self){self.collection.trigger("reset")}, args: this});
                }
            }
        },
        showNextPage: function (e) {
            var tag = e.currentTarget;
            var className = tag.getAttribute("class");
            if(className.indexOf('disabled') == -1){
                var table_name = this.$el.find('#table_name').attr('data-model-name');
                if(this.collection.has_next){
                    this.collection.fetchData(false,{method:'cmdb.show.records', table_name: table_name}, {success: function(self){self.collection.trigger("reset")}, args: this});
                }
            }
        },
        returnList: function (e) {
            var tag = e.currentTarget;
            var className = tag.getAttribute("class");
            if(className.indexOf('disabled') == -1){
                var table_name = this.$el.find('#table_name').attr('data-model-name');
                this.collection.currentPage();
                this.collection.fetchData(false,{method:'cmdb.show.records', table_name: table_name},{success: function(self){self.collection.trigger("reset")}, args: this});
            }
        }
    });
});