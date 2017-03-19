/**
 * Created by zhanghai on 2017/02/04.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var IPDetailItemViewTemplate = require('text!./templates/cmdb_ip_detail_template.tpl');
    var modifyIPItemTemplate = require('text!./templates/modify_ip_template.tpl');

    var IPDetailItemView = Backbone.View.extend({
        tagName: "tr",
        template: _.template(IPDetailItemViewTemplate),
        events: {
            "click .delete-ip": "deleteIP",
            "click .modify-ip": "initModifyIP"
        },
        initialize: function (options) {
            this.record = options.record;
            this.collection = options.collection;
            this.listenTo(this.record, 'destroy', this.remove);
        },
        initModifyIP: function (e) {
            //加载IP modal
            var request_data = {
                    "tables":["BaseDataCenter","BaseNetArea"]
                },
                self = this;

            $("#partition-subnet").empty();
            var view = new ModifyIPItemView({model: self.record});
            $("#partition-subnet").append(view.render().el);

        },
        deleteIP: function (e) {
            var self = this;

            self.collection.url = "/api/v1/afcat/";
            swal(
                {
                    title: "确定删除该IP/网络？",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true
                },
                function(){
                    var request_data = {
                        "value":{"id":self.record.id},
                        "action":"delete",
                        "type":"ip",

                    };
                    swal.setDefaults({closeOnConfirm:false});
                    self.collection.fetchData(false, {data: JSON.stringify(request_data), method: "cmdb.ipmanagement.allocation", async:false, success:function (model, collection, response) {
                        window.location.href = "/cmdb/cmdb_ip_management/list/";
                    }});
               }
            );
        },
        render: function () {
            //console.log(this.record)
            console.log("this.record:", this.record)
            this.$el.html(this.template(this.record));
            return this;
        }
    });

    var ModifyIPItemView = Backbone.View.extend({
        template: _.template(modifyIPItemTemplate),
        events: {
        },
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.record)
            console.log("model:", this.model)
            this.$el.html(this.template(this.model));
            return this;
        }
    });

    return {
        IPDetailItemView: IPDetailItemView,
        ModifyIPItemView: ModifyIPItemView,
    };
})