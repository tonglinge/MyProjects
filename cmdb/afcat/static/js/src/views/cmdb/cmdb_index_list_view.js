/**
 * Created by zengchunyun on 2016/11/16.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var IndexItemView = require("./cmdb_index_item_view").IndexItemView;
    var IndexItemViewChartTemplate = require("text!./templates/cmdb_index_chart_template.tpl");
    var IndexItemViewAuditTemplate = require("text!./templates/cmdb_index_audit_record_template.tpl");
    var IndexView = Backbone.View.extend({
        events: {
            "click .cmdb-title": "chooseCarousel"
        },
        initialize: function (options) {
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            var self = this;
            this.collection.fetchData(true, {method: "cmdb.reportindex.get_record"},{callback:this.getGroupsStatus, args:self});
        },
        addAll: function () {
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var op_model = model.toJSON();

            if(op_model.name == "totalcount"){
                $("#server-count").html(op_model.values.assets);
                $("#equipment-count").text(op_model.values.equipment);
                $("#host-count").text(op_model.values.server);
            }else if(op_model.name == "audit"){
                var view = new IndexItemView({model: model, template:IndexItemViewAuditTemplate});
                this.$el.find('#opration-log').html(view.render().el);
            }else{
                var chart_dom_map = {
                    asset: '#server-chart-contain',
                    asset_count: '#server-count-chart-contain',
                    equipment: '#equipment-chart-contain',
                    equipment_count: '#equipment-count-chart-contain',
                    host: '#host-chart-contain',
                    itemset: '#host-item-chart-contain'
                }
                var tagname = chart_dom_map[op_model.name];
                var view = new IndexItemView({model: model, template:IndexItemViewChartTemplate, tagname: tagname});
                this.$el.find(tagname).html(view.render().el);
                this.widthStyle()
            }
        },
        chooseCarousel: function (e) {
            //点击首页title选择相应的carousel图表

            var cmdb_title = $(e.currentTarget).find(".cmdb-count").get(0).id;
            var dom_map = {
                "server-count": 0,
                "equipment-count": 1,
                "host-count": 2,
            };
            var dom_index = dom_map[cmdb_title];
            $($(".carousel-indicators").children("li").get(dom_index)).trigger("click")
        },
        widthStyle: function(){
            var width = $('.chart-box').width();
            $('.chart-info').width(width)
            console.log(width);
            $(window).resize(function(){
                var width2 = $('.chart-box').width();
                $('.chart-info').width(width2)
            })
        }
    });
    return IndexView;

});