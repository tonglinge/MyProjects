/**
 * Created by zengchunyun on 16/8/12.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var GroupsItemView = require("./monitor_groups_item_view").GroupsItemView;
    var GroupsMenuItemView = require("./monitor_groups_item_view").GroupsMenuItemView;

    var GroupsView = Backbone.View.extend({
        events: {
            "click .host-groups-menu-item": "showMenu",
            "click #search-btn": "searchData"
        },
        initialize: function (options) {
            this.pathname = location.pathname;
            this.pathNameList = this.pathname.split("/");
            this.group_id = $.trim(this.pathNameList[this.pathNameList.length-1]);
            var formData = {};
            if(this.group_id){
                formData['group_id'] = this.group_id;
            }
            this.page = 1;
            this.collection.url = options.url;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'all', this.render);
            this.collection.fetchData(true, formData);
        },
        addAll: function () {
            this.$el.find(".groups-body").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new GroupsItemView({model: model});
            $(".groups-body").append(view.render().el);
            var menuView = new GroupsMenuItemView({model: model});
            $(".groups-body").find('tr:last').find(".host-groups-menu-item").append(menuView.render().el)
        },
        showMenu: function (e) {
            $(e.currentTarget).find(".host-groups-menu").css({'left': e.offsetX,'top':e.offsetY});
            $(e.currentTarget).find(".host-groups-menu").removeClass('hide').parents('tr').siblings().find('.host-groups-menu').addClass('hide');
        },
        searchData: function (e) {
            //获取搜索主机组表单数据
            var searchForm = this.$el.find('#search-form');
            var formData = {};
            formData['host_name'] = searchForm.find('[name="host-name"]').val();
            formData['ip_address'] = searchForm.find('[name="ip"]').val();
            formData['status'] = searchForm.find('[name="status"]').val();
            formData['issue_time'] = searchForm.find('[name="issue-time"]').val();
            formData['issue_level'] = searchForm.find('[name="issue-level"]').val();
            formData['group_id'] = this.group_id;
            this.collection.fetchData(true, formData)
        }

    });

    return GroupsView;
})