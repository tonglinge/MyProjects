/**
 * Created by zhanghai on 2016/9/27.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    //引入服务器资产页面模板
    var ServerAssetItemViewTemplate = require('text!./templates/modify_server_asset_template.tpl');
    //服务器资产item
    var ServerAssetItemView = Backbone.View.extend({
        className: "row",
        tagName: "div",
        template: _.template(ServerAssetItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.model);
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return {
        ServerAssetItemView: ServerAssetItemView,
    };
})