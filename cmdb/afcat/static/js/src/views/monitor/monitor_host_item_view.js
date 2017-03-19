/**
 * Created by zengchunyun on 16/8/31.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require("backbone");

    var HostCheckBoxItemViewTemplate = require("text!./templates/host_checkbox_template.tpl");
    var HostGraphItemViewTemplate = require("text!./templates/host_graph_template.tpl");

    //选择按钮视图
    var HostCheckBoxItemView = Backbone.View.extend({
        events: {
            "click :checkbox": "switchStatus"
        },
        className: "container-bg",
        tagName: "li",
        template: _.template(HostCheckBoxItemViewTemplate),

        initialize: function (options) {
            this.model = options.model;
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        switchStatus: function (e) {
            var graph_name = e.currentTarget.name;
            var graph_id = e.currentTarget.value;
            var show_item = e.currentTarget.checked;

            if(show_item){
                this.collection.fetchData(true,{graph_name: graph_name, graph_id: graph_id, show_item: show_item})
            }else {
                $("#graph"+ graph_id).parents(".host-data-graph-item").remove();
            }
        }
    });

    //图形显示视图
    var HostGraphItemView = Backbone.View.extend({
        events: {
            "click [name=switch_status]": "toggleStatus"
        },
        className: "host-data-graph-item",
        template: _.template(HostGraphItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            var modelToJSON = this.model.toJSON();
            var legend = [];
            var graphID = modelToJSON.graph_id;
            var itemPercent = '16';
            if(modelToJSON.data.length){
                var dateLine = modelToJSON.data[0].date;
                for(var index in modelToJSON.data){
                    var item_data = modelToJSON.data[index];
                    legend.push("'" + item_data.item_name + "'");
                }
                //此处500为canvs图所占高度
                // itemPercent = modelToJSON.data.length * 21 / 600 * 100 + 2;

            }else {
                dateLine = [];
                legend = [];
                modelToJSON.data = [];
            }
            this.$el.html(this.template({legend: legend, date:dateLine, data:modelToJSON.data, name: modelToJSON.name, graph_id: graphID, itemPercent: itemPercent}));
            return this
        },
        toggleStatus: function (e) {
            this.$el.find("[name=switch_status]").bootstrapSwitch()
        }
    });



    return {
        HostCheckBoxItemView: HostCheckBoxItemView,
        HostGraphItemView: HostGraphItemView
    }
});