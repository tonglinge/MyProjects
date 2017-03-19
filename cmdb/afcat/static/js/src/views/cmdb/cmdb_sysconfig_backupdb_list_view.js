/**
 * Created by super on 2016/12/12.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var BackupDBItemView = require("./cmdb_sysconfig_backupdb_item_view").BackupDBItemView;


    var BackupDBView = Backbone.View.extend({
        events: {
            "click #id-btn-newbackup": "createBackup",
            "click #id-del-backup": "operatorBackup",
            "click #id-restore-backup": "operatorBackup",
            "click .show_previous_page": "showPreviousPage",
            "click .show_next_page": "showNextPage"
        },
        initialize: function (options) {
            this.index = 1;
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, {method: 'cmdb.configure.db_record'});
        },
        addAll: function () {
            var models = this.collection.models;
            //针对每次reload数据时需要清空整个app页面数据，指定判断关键属性，用来决定是否对app内容清空
            if (models.length > 0) {
                this.$el.find('.backupdb-body').html('')
            }
            this.collection.each(this.addOne, this);
            // this.index = 1;

            // 设置上一页、下一页属性
            this.$el.find(".show_previous_page").toggleClass('disabled', !this.collection.has_previous);
            this.$el.find(".show_next_page").toggleClass('disabled', !this.collection.has_next);
            // console.log("collection..", this.collection.has_next, this.collection.has_previous);
        },
        addOne: function (model) {
            var view = new BackupDBItemView({model: model, showindex: this.index});
            this.$el.find(".backupdb-body").append(view.render().el);
            this.index += 1;
        },
        afterCreated: function (args, collection, response, options) {
            $("#id-backupmemo").val("");
            collection.fetchData(true, {method: 'cmdb.configure.db_record'});
        },
        createBackup: function () {
            var remark = $("#id-backupmemo").val();
            this.collection.fetchData(false, {remark: remark, method: 'cmdb.configure.db_backup'},
                {type: "get", success: this.afterCreated})
        },
        afterDeleted: function (args, collection, response, options) {
            var self = args.self;
            var curr_target = args.opel;
            if (args.rec_count == 1){
                curr_target.parent().parent().remove();
            }else {
                self.index = ((self.collection.page-1)*self.collection.per_records + 1);
                // self.collection.fetchData(true, {method: 'configure.db_record'});
                self.collection.fetchData(false,{method:'cmdb.configure.db_record'}, {success: function(self){self.collection.trigger("reset")}, args: self})
            }
        },
        operatorBackup: function (e) {
            var curr_target = $(e.currentTarget);
            var rec_id = curr_target.attr("rec");
            var action = curr_target.attr("act");
            var self = this;
            var _collection = this.collection;
            var alert_text = "";
            if (action == "del"){alert_text = "确定要删除该备份集吗?"; alert_title = "删除确认";}
            if (action == "restore"){alert_text="确定要恢复到当前备份集吗?"; alert_title = "恢复确认";}
            swal({
                title: alert_title,
                text: alert_text,
                type: "warning",
                showCancelButton: true,
                confirmButtonText: "确认",
                cancelButtonText: "取消",
                closeOnConfirm: true,
                closeOnCancel: true
                },
                function (isConfirm) {
                    if (isConfirm) {
                        if (action == "del"){
                            var rec_count = self.collection.length;
                            self.collection.currentPage();
                            _collection.fetchData(false, {id: rec_id, method: "cmdb.configure.db_remove"},
                            {success: self.afterDeleted, args: {self: self, rec_count:rec_count,opel: curr_target}}
                            // {success: function(self){self.collection.trigger("reset")}, args: self}
                            )}
                        if (action == "restore"){
                            self.collection.currentPage();
                            _collection.fetchData(false, {id: rec_id, method: "cmdb.configure.db_restore"})
                        }

                    }
                });

        },
        showPreviousPage: function (e) {
            var tag = e.currentTarget;
            var className = tag.getAttribute("class");
            if(className.indexOf('disabled') == -1){
                if(this.collection.has_previous){
                    this.collection.previousPage();
                    this.collection.fetchData(false,{method:'cmdb.configure.db_record'}, {success: function(self){self.collection.trigger("reset")}, args: this});
                }
            }
            this.index = ((this.collection.page-1)*this.collection.per_records + 1);
        },
        showNextPage: function (e) {
            var tag = e.currentTarget;
            var className = tag.getAttribute("class");
            if(className.indexOf('disabled') == -1){
                if(this.collection.has_next){
                    this.collection.fetchData(false,{method:'cmdb.configure.db_record'}, {success: function(self){self.collection.trigger("reset")}, args: this});
                }
            }
        },
    });
    return BackupDBView;

});