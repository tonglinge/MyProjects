/**
 * Created by zengchunyun on 16/9/20.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var EventItemViewTemplate = require("text!./templates/event_template.tpl");
    var EventGroupsMenuItemViewTemplate = require("text!./templates/event_groups_menu.tpl");
    var EventHostsMenuItemViewTemplate = require("text!./templates/event_hosts_menu.tpl");

    var EventItemView = Backbone.View.extend({
        events: {
            "click .arrow-right": "menuOpen",
            "click .arrow-down": "menuClose"
        },
        tagName: "tr",
        className:function () {
            var style = "treeview";
            if(this.model.get('data_parentid') != 0){
                style = "hide"
            }
            return style
        },
        template: _.template(EventItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;

        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        switchTreeMenu: function (e) {
            var triggerID = this.$el.find("td[data-switcherid]").attr("data-switcherid");
            this.$el.parents("tbody").find("tr").find("[data-parentid="+triggerID +"]").parent().toggleClass('hide');
        },
        menuOpen: function (e) {
            this.$el.children(":first").find("span.arrow-right").addClass("arrow-down").removeClass("arrow-right");
            this.switchTreeMenu(e)
        },
        menuClose: function (e) {
            this.$el.children(":first").find("span.arrow-down").addClass("arrow-right").removeClass("arrow-down");
            this.switchTreeMenu(e)
        }
    });

    //获取主机组菜单列表
    var EventGroupsMenuItemView = Backbone.View.extend({
        events: {},
        template: _.template(EventGroupsMenuItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    //获取主机菜单列表
    var EventHostsMenuItemView = Backbone.View.extend({
        events: {},
        template: _.template(EventHostsMenuItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return {
        EventItemView: EventItemView,
        EventGroupsMenuItemView: EventGroupsMenuItemView,
        EventHostsMenuItemView: EventHostsMenuItemView
    }
});