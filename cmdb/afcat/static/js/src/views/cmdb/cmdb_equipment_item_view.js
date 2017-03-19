/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var ServerAssetItemViewTemplate = require('text!./templates/equipment_baseinfo_template.tpl');
    var ServerAssetItemView = Backbone.View.extend({
        className: "",
        tagName: "tr",
        template: _.template(ServerAssetItemViewTemplate),
        events: {
            "click #btn_delete_equipment": "deleteEquipment"
        },
        initialize: function (options) {
            this.model = options.model;
            this.record = options.record;
            this.url = "/cmdb/assetmodify/";
            this.listenTo(this.record, 'destroy', this.remove);
        },
        deleteEquipment: function (e) {
            //删除设备资产
            //this.sid = $("#"+e.currentTarget.id).parent()[0].id;
            var sid = this.record.id;
            var equipment_model = new this.model();
            equipment_model.url = this.url;
            if (this.record.portmapcount > 0){
                swal({title: "",
                    text: "设备包含端口映射,请先删除映射关系",
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true});
                return false
            }
            swal(
                {
                    title: "确定删除该设备资产？",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true
                },
                function(){
                    var data = {
                        "action":"delete",
                        "model":"equipment",
                        "value":{"id": sid},
                    };
                    swal.setDefaults({closeOnConfirm:false});
                    equipment_model.save({data: data, type:"POST"}, {success:function (response) {
                        var tr = $(e.target).closest('tr');
                        tr.remove();
                    }});
                }
            );
        },
        render: function () {
            this.$el.html(this.template(this.record));
            return this;
        }
    });

    return {
        ServerAssetItemView: ServerAssetItemView,
    };
});