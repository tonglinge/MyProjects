/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var ServerAssetDetailItemViewTemplate = require('text!./templates/server_asset_detailinfo_template.tpl');
    var ServerAssetDetailItemView = Backbone.View.extend({
        className: "server-detail-record",
        tagName: "div",
        template: _.template(ServerAssetDetailItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.model.toJSON());
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return {
        ServerAssetDetailItemView: ServerAssetDetailItemView,
    };
})