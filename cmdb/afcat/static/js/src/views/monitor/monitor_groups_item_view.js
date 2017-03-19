/**
 * Created by zengchunyun on 16/8/12.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');

    var Backbone = require('backbone');
    var GroupsItemViewTemplate = require('text!./templates/groups_template.tpl');
    var GroupsMenuItemViewTemplate = require('text!./templates/groups_menu_template.tpl');
    var GroupsItemView = Backbone.View.extend({
        className: "",
        tagName: "tr",
        template: _.template(GroupsItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    var GroupsMenuItemView = Backbone.View.extend({
        className: "host-groups-menu hide",
        tagName: "div",
        template: _.template(GroupsMenuItemViewTemplate),
        events: {
            "mouseleave ul": "removeMenu"
        },
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        showMenu: function () {
            this.$el.removeClass('hide');
        },
        removeMenu: function (e) {
            this.$el.addClass('hide')
        }
    });

    return {
        GroupsItemView: GroupsItemView,
        GroupsMenuItemView: GroupsMenuItemView
    };
})