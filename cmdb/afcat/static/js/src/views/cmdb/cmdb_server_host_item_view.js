/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var ServerHostItemViewTemplate = require('text!./templates/server_host_template.tpl');
    var ServerHostItemView = Backbone.View.extend({
        tagName: "tr",
        template: _.template(ServerHostItemViewTemplate),
        events: {
            "click #delete-server-asset": "deleteServerAsset",
        },
        initialize: function (options) {
            this.record = options.record;
            this.module = options.module;
            this.model = options.model;
            this.search_key = options.search_key;
            this.listenTo(this.record, 'destroy', this.remove);
        },
        deleteServerAsset: function (e) {
            //删除服务器资产
            var asset_model = new this.model();
            var sid = this.record.id;
            var post_data = {
                "action":"delete",
                "model":this.module,
                "value":{"id":sid}
            };
            swal({
                    title: "确定删除该服务器资产",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true
                },
                function(){
                    asset_model.url = "/cmdb/assetmodify/";
                    asset_model.set("data", post_data);
                    asset_model.save({}, {success: function () {
                        var tr = $(e.target).closest('tr');
                        tr.remove();
                    }});
                }
            );
        },
        render: function () {
            this.record["search_key"] = this.search_key;
            //console.log(this.record)
            this.$el.html(this.template(this.record));
            return this;
        }
    });

    return {
        ServerHostItemView: ServerHostItemView,
    };
})