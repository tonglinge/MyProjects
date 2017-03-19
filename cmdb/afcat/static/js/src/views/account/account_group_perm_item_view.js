/**
 * Created by super on 2016/10/21.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var GroupPermMenuItemViewTemplate = require("text!./templates/account_group_perm_menu.tpl");
    var GroupPermAssetItemViewTemplate = require("text!./templates/account_group_perm_asset.tpl");
    var GroupPermGroupsItemViewTemplate = require("text!./templates/account_group_perm_groups.tpl");

    //组权限管理菜单权限模版
    var GroupPermMenuItemView = Backbone.View.extend({
        tagName: "tbody",
        events: {},
        template: _.template(GroupPermMenuItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            // console.log(this.template());
            this.$el.html(this.template({menu:this.model}));
            return this;
        }
    });
    var GroupPermAssetItemView = Backbone.View.extend({
        tagName:"tbody",
        events:{},
        template:_.template(GroupPermAssetItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.classattrname = options.classattrname
        },
        render: function () {
            this.$el.html(this.template({project:this.model,classattrname:this.classattrname}));
            return this;
        }
    });
    var GroupPermGroupItemView = Backbone.View.extend({
        tagName:"li",
        events:{},
        template:_.template(GroupPermGroupsItemViewTemplate),
        initialize: function (options) {
            this.model = options.model
        },
        render: function () {
            this.$el.html(this.template({group:this.model}));
            return this
        }

    });

    return {
        GroupPermMenuItemView: GroupPermMenuItemView,
        GroupPermAssetItemView: GroupPermAssetItemView,
        GroupPermGroupsItemsView: GroupPermGroupItemView
    }
});