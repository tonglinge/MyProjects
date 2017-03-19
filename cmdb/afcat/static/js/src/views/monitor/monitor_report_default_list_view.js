/**
 * Created by zengchunyun on 2016/10/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var ReportDefaultItemView = require("./monitor_report_default_item_view").ReportDefaultItemView;

    var ReportDefaultView = Backbone.View.extend({
        events: {
            "click .filter_btn": "getTriggerEvent",
            "click .export_btn": "getExcelFile"
        },
        initialize: function (options) {
            this.page = 1;
            this.collection.url = options.url;
            this.condition = null;
            this.listenTo(this.collection, 'reset', this.addAll);
            var self = this;
            $(window).on("scroll", function () {
                if($(window).scrollTop() == $(document).height() - $(window).height()){
                    if(self.collection.has_next && self.condition != null){
                        $("#loading").show();
                        self.collection.fetchData(false, self.condition,{success:function(self){self.collection.trigger("reset")}, args: self});
                    }
                }
            })
        },
        addAll: function () {
            if(this.collection.reseted && typeof this.collection.models[0].get("get_hosts") == 'undefined'){
                this.$el.find(".export_table tbody").html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var event_trigger = new ReportDefaultItemView({model: model});
            this.$el.find(".export_table tbody").append(event_trigger.render().el)
        },
        getTriggerEvent: function (e) {
            this.$el.find(".export_table tbody").html('');
            //点击搜索按钮时获取搜索结果
            var group_id = this.$el.find("#group_id").val();
            var host_id = this.$el.find("#host_id").val();
            var host_status = this.$el.find('[name="host_status"]').val();
            var ip_address = this.$el.find("[name=ip_address]").val();
            var issue_level = this.$el.find('[name="issue-level"]').val();
            var issue_status = this.$el.find('[name="issue-status"]').val();
            var ack = this.$el.find('[name="ack"]').val();
            var start_time = this.$el.find('[name="start_time"]').val();
            var end_time = this.$el.find('[name="end_time"]').val();
            this.condition = {
                group_id: group_id,
                host_id: host_id,
                host_status: host_status,
                ip_address: ip_address,
                issue_level: issue_level,
                issue_status: issue_status,
                ack: ack,
                start_time: start_time,
                end_time: end_time
            };
            this.collection.fetchData(true, this.condition);
        },
        getExcelFile: function (e) {
            this.collection.fetchData(false, {condition: '123'});
        }
    });

    return ReportDefaultView;

});