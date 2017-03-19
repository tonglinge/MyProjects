/**
 * Created by zengchunyun on 16/9/20.
 */

//告警页面事件
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var EventItemView = require("./monitor_event_item_view").EventItemView;
    var EventGroupsMenuItemView = require("./monitor_event_item_view").EventGroupsMenuItemView;
    var EventHostsMenuItemView = require("./monitor_event_item_view").EventHostsMenuItemView;

    var EventView = Backbone.View.extend({
        events: {
            "change #group_id": "getHosts",
            "click #search-btn": "getTriggerEvent",
            "mychange #group_id": "getGroups"
        },
        initialize: function (options) {
            this.page = 1;
            this.collection.url = options.url;
            this.condition = null;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'all', this.render);
            this.collection.fetchData(true, {group_id:0, get_hosts: true, get_groups: true});
            var self = this;
            $(window).on("scroll", function () {
                if($(window).scrollTop() == $(document).height() - $(window).height()){
                    if(self.collection.has_next && self.condition != null){
                        self.collection.fetchData(false, self.condition, {success: function (self) {self.collection.trigger("reset")}, args: self});
                    }
                }
            })
        },
        addAll: function () {
            if(this.collection.reseted && typeof this.collection.models[0].get("get_hosts") == 'undefined'){
                this.$el.find('.search-tbody').html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            // 如果是只有一条触发器的历史数据，则没有这个属性，需要设置默认属性
            if(!model.has('parent')){
                model.set('parent', false)
            }
            //只有选择了事件历史触发器数据，才会有下面这个属性
            if(!model.has('data_parentid')){
                model.set('data_parentid', 0)
            }
            if(!model.has('data_switcherid')){
                model.set('data_switcherid', 0)
            }
            var modelToJSON = model.toJSON();
            if(modelToJSON.get_groups){
                var groups_menu = new EventGroupsMenuItemView({model: model});
                this.$el.find("#group_id").html($(groups_menu.render().el).html())
            }
            if(modelToJSON.get_hosts){
                var hosts_menu = new EventHostsMenuItemView({model: model});
                this.$el.find("#host_id").html($(hosts_menu.render().el).html());
                var dest = document.getElementById("host_set");
                if(dest){
                    var src = document.getElementById("host_id");
                    for(var j=0; j < dest.length; j++){
                        for(var i=0;i < src.length; i++){
                            if(src.options[i].value == dest.options[j].value){
                                src.options.remove(i);
                            }
                        }
                    }
                }
            } else {
                var event_trigger = new EventItemView({model: model});
                this.$el.find('.search-tbody').append(event_trigger.render().el);
            }
        },
        getHosts: function (e) {
            //获取主机列表信息
            var group_id = this.$el.find("#group_id").val();
            this.collection.fetchData(true, {group_id:group_id, get_hosts: true});
        },
        getGroups: function (e) {
            var group_id = this.$el.find("#group_id").val();
            this.collection.fetchData(true, {group_id:group_id, get_hosts: true, get_groups: true});
        },
        getTriggerEvent: function (e) {
            //点击搜索按钮时获取搜索结果
            var group_id = this.$el.find("#group_id").val();
            var host_id = this.$el.find("#host_id").val();
            var ip_address = this.$el.find("[name=ip_address]").val();
            var issue_level = this.$el.find('[name="issue-level"]').val();
            var ack = this.$el.find('[name="ack"]').val();
            var trigger_end_time = this.$el.find('[name="trigger_end_time"]').val();
            var start_time = this.$el.find('[name="start_time"]').val();
            var end_time = this.$el.find('[name="end_time"]').val();
            this.condition = {
                group_id: group_id,
                host_id: host_id,
                ip_address: ip_address,
                issue_level: issue_level,
                ack: ack,
                trigger_end_time: trigger_end_time,
                start_time: start_time,
                end_time: end_time
            };
            this.collection.fetchData(true, this.condition);
        }
    });

    return EventView;

});