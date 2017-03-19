/**
 * Created by zengchunyun on 2016/9/28.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var IndexDashboardItemView = require("./monitor_index_item_view").IndexDashboardItemView;
    var IndexEventItemView = require("./monitor_index_item_view").IndexEventItemView;
    var IndexTopDataItemView = require("./monitor_index_item_view").IndexTopDataItemView;
    var IndexTopDataTableItemView = require("./monitor_index_item_view").IndexTopDataTableItemView;

    var IndexView = Backbone.View.extend({
        events: {},
        initialize: function (options) {
            this.page = 1;
            this.collection.url = options.url;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'all', this.render);
            this.collection.fetchData(true, {group_status_info:true, get_event_triggers_status: true, get_top_data: true},{success:this.intervalFetch, args:this});
        },
        addAll: function () {
            this.$el.find(".top_data_show").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var modelToJSON = model.toJSON();
            if(modelToJSON.group_status_info){
                var total_normal_count = modelToJSON.group_status_info.total_normal_count;
                var total_issue_count = modelToJSON.group_status_info.total_issue_count;
                var total_count = total_normal_count + total_issue_count;
                $("#total_normal_count").find(".progress-number").html("<b>"+total_normal_count+"</b>/"+total_count+"");
                $("#total_normal_count").find(".progress-bar").css('width',total_normal_count/total_count * 100 + '%');
                $("#total_issue_count").find(".progress-number").html("<b>"+total_issue_count+"</b>/"+total_count+"");
                $("#total_issue_count").find(".progress-bar").css('width',total_issue_count/total_count * 100 + '%');
                var group_status = new IndexDashboardItemView({model: model});
                this.$el.find(".host_groups_status").html(group_status.render().el)
            }
            if(modelToJSON.get_event_triggers_status){
                var event_trigger = new IndexEventItemView({model: model});
                this.$el.find(".event_trigger_status").find('tbody').remove();
                this.$el.find(".event_trigger_status").append(event_trigger.render().el)
            }
            if(modelToJSON.get_top_data){
                var top_data = modelToJSON.get_top_data;
                for(var i=0; i<top_data.length; i++){
                    var name = top_data[i].name;
                    var value = top_data[i].value;
                    var unit = top_data[i].unit;

                    if(top_data[i].type == "table"){
                        var top_data_table_view = new IndexTopDataTableItemView({model: model, name: name, value: value, unit: unit});
                        this.$el.find(".top_data_show").append(top_data_table_view.render().el)
                    }else {
                        var top_data_view = new IndexTopDataItemView({model: model, name: name, value: value, unit: unit, html_id:top_data[i].id});
                        this.$el.find(".top_data_show").append(top_data_view.render().el)
                    }
                }
            }
        },
        intervalFetch: function (self) {
            //120秒更新一次页面数据
            setTimeout(function () {
                self.collection.fetchData(true, {group_status_info:true, get_event_triggers_status: true, get_top_data: true}, {args:self, success:self.intervalFetch});
            }, 120000)

        }
    });

    return IndexView;

});