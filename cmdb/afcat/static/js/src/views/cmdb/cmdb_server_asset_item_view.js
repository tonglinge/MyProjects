/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var ServerAssetItemViewTemplate = require('text!./templates/server_asset_baseinfo_template.tpl');
    var ServerAssetItemView = Backbone.View.extend({
        tagName: "tr",
        template: _.template(ServerAssetItemViewTemplate),
        events: {
            "click #delete-server-asset": "deleteServerAsset"
        },
        initialize: function (options) {
            this.record = options.record;
            this.module = options.module;
            this.model = options.model;
            this.listenTo(this.record, 'destroy', this.remove);
        },
        deleteServerAsset: function (e) {
            //删除服务器资产
            var asset_model = new this.model();
            // console.log(asset_model);
            var sid = this.record.id;
            var post_data = {
                "action":"delete",
                "model":this.module,
                "value":{"id":sid}
            };

            var related_hosts = $(e.currentTarget).parent().siblings(".hostcount").text();
            if(related_hosts > 0){
                swal({title: "",
                    text: "此资产包含主机,请先迁移或移除主机",
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true});
                return false
            }
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
            //console.log(this.record)
            this.$el.html(this.template(this.record));
            return this;
        }
    });

    return {
        ServerAssetItemView: ServerAssetItemView,
    };
})