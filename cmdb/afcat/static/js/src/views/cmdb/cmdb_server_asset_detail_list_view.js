/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var ServerAssetDetailItemView = require("./cmdb_server_asset_detail_item_view").ServerAssetDetailItemView;
    var ServerAssetModalItemView = require("./cmdb_server_asset_modal_item_view").ServerAssetModalItemView;

    var CMDBView = Backbone.View.extend({
        events: {
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.url = options.url;
            this.collection.url = options.url;
            this.sid = options.options.sid;
            this.model = options.options.model;
            this.module = options.options.type;
            this.listenTo(this.collection, 'reset', this.addAll);
            //this.listenTo(this.collection, 'all', this.render);
            this.collection.fetchData(true, JSON.stringify({"model":this.module, "sid":this.sid}));
        },
        addAll: function () {
            this.$el.find(".server-detail-record").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var detailview = new ServerAssetDetailItemView({model: model});
            this.$el.html(detailview.render().el);
        },
    });

    return CMDBView;
})

