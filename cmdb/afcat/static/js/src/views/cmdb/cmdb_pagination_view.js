/**
 * Created by zhanghai on 2016/9/28.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    //引入服务器资产页面模板
    var ServerAssetPaginationTemplate = require('text!./templates/page_template.tpl');
    //服务器资产item
    var PaginationView = Backbone.View.extend({
        //className: "pagination",
        //tagName: "div",
        //el: $(".pagination"),
        template: _.template(ServerAssetPaginationTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.model.toJSON())
            try{
                var model = this.model.toJSON()[0];
            }catch(err){
                var model = this.model;
            }
            this.$el.html(this.template(model));
            return this;
        }
    });

    return {
        PaginationView: PaginationView,
    };
})