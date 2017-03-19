/**
 * Created by zhanghai on 2016/10/8.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    //引入服务器资产页面Modal模板
    var ServerAssetStaffTemplate = require('text!./templates/server_asset_staff_template.tpl');
    var ServerAssetSoftTemplate = require('text!./templates/server_asset_soft_template.tpl');
    var ServerAssetCPUTemplate = require('text!./templates/server_asset_cpu_template.tpl');
    var ServerAssetIPTemplate = require('text!./templates/server_asset_ip_template.tpl');
    var ServerAssetCardTemplate = require('text!./templates/server_asset_card_template.tpl');
    var ServerHostCardTemplate = require('text!./templates/server_host_card_template.tpl');
    var ServerHostVolumeGroupTemplate = require('text!./templates/server_host_volume_group_template.tpl');

    //服务器资产item
    var ServerAssetModalItemView = Backbone.View.extend({
        //className: "pagination",
        //tagName: "tr",
        //template: _.template(ServerAssetStaffTemplate),
        events:{
            "click #soft_type": "chooseSoft",
            "change #soft_type": "chooseSoft",
            "click #softname": "softFilter",
            "change #softname": "chooseLicense",
            "click #license": "licenseFilter",
        },
        initialize: function (options) {
            this.model = options.model;
            this.current_id = options.current_id;
            if(options.data){
                this.data = options.data;
            }
            this.listenTo(this.model, 'destroy', this.remove);
            this.template = this.select_template(this.current_id);
        },
        softFilter: function (e) {
            //初始化指定软件分类下的软件列表
            var soft_type = $("#soft_type option:selected").val();
            $("#softname option").each(function () {
                if($(this).attr("name") == soft_type){
                    $(this).css("display", "");
                    $(this).attr("selected", true);

                }else{
                    $(this).css("display", "none");
                    $(this).attr("selected", false);
                }
            });
            this.chooseLicense();
        },
        licenseFilter: function (e) {
            //根据指定软件初始化license列表
            var id = $("#softname option:selected").val();
            $("#license option").each(function () {
                var soft_id = $(this).attr("name")
                if(id == soft_id){
                    $(this).css("display", "");
                    $(this).attr("selected", true);
                }else{
                    $(this).css("display", "none");
                    $(this).attr("selected", false);
                }
            });
        },
        chooseSoft: function (e) {
            //modal根据软件分类选择soft
            var soft_type = $("#soft_type option:selected").val();
            $("#softname option").each(function () {
                if($(this).attr("name") == soft_type){
                    $(this).css("display", "");
                    $(this).attr("selected", true);

                }else{
                    $(this).css("display", "none");
                    $(this).attr("selected", false);
                }
            });
            this.chooseLicense();
        },
        chooseLicense: function () {
            //选择license
            var id = $("#softname option:selected").val();
            $("#soft_id").val(id);

            $("#license option").each(function () {
                var soft_id = $(this).attr("name")
                if(id == soft_id){
                    $(this).css("display", "");
                    $(this).attr("selected", true);
                }else{
                    $(this).css("display", "none");
                    $(this).attr("selected", false);
                }
            });
        },
        select_template: function (current_id) {
            //根据id选择模板
            var templates = {
                'addStaff': _.template(ServerAssetStaffTemplate),
                'editStaff': _.template(ServerAssetStaffTemplate),
                'addSoft': _.template(ServerAssetSoftTemplate),
                'editSoft': _.template(ServerAssetSoftTemplate),
                'addServerHostCard': _.template(ServerHostCardTemplate),
                'editServerHostCard': _.template(ServerHostCardTemplate),
                'addCPU': _.template(ServerAssetCPUTemplate),
                'editCPU': _.template(ServerAssetCPUTemplate),
                'addIP': _.template(ServerAssetIPTemplate),
                'editIP': _.template(ServerAssetIPTemplate),
                'add-vg': _.template(ServerHostVolumeGroupTemplate),
                'edit-vg': _.template(ServerHostVolumeGroupTemplate),
                'addCard': _.template(ServerAssetCardTemplate),
                'editCard': _.template(ServerAssetCardTemplate),
            }
            return templates[current_id];
        },
        render: function () {
            if(this.data){
                //console.log(this.data)
                this.$el.html(this.template(this.data));
            }
            else{
                this.$el.html(this.template());
            }
            return this;
        }
    });

    return {
        ServerAssetModalItemView: ServerAssetModalItemView,
    };
})