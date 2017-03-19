/**
 * Created by zengchunyun on 16/8/31.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var HostGraphItemView = require("./monitor_host_item_view").HostGraphItemView;
    var HostCheckBoxItemView = require("./monitor_host_item_view").HostCheckBoxItemView;

    var HostView = Backbone.View.extend({
        events: {},
        initialize: function (options) {
            //主机图形item列表
            this.checkboxList = this.$el.find('.data-graph-list');
            //主机图形显示区域
            this.graphList = this.$el.find('.host-data-graph-item');
            this.page = 1;
            this.collection.url = options.url;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'all', this.render);
            this.collection.fetchData(true, {host_id: options.options.host_id}, {success:this.intervalFetch, args: this});
        },
        addAll: function () {
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var modelToJSON = model.toJSON();
            if(modelToJSON && modelToJSON.data){
                var graphView = new HostGraphItemView({model: model});
                var graphViewHtml = graphView.render().el;
                if($("#"+ modelToJSON.graph_id).length){
                    this.$el.children('.graph-show-area').find("#"+ modelToJSON.graph_id).html(graphViewHtml)
                }else {
                    this.$el.children('.graph-show-area').append(graphViewHtml);
                }

            }else {
                var checkboxItem = new HostCheckBoxItemView({model: model, collection: this.collection});
                this.checkboxList.append(checkboxItem.render().el);
            }
        },
        refreshGraph: function (checkboxElement, self) {
            var graph_name = checkboxElement.name;
            var graph_id = checkboxElement.value;
            var show_item = checkboxElement.checked;
            self.collection.fetchData(true,{graph_name: graph_name, graph_id: graph_id, show_item: show_item})
        },
        intervalFetch: function (self) {
            setInterval(function () {
                $('.data-graph-list').find(':checked').each(function (index, checkbox) {
                    self.refreshGraph(checkbox, self)
                });
            }, 55000)
        }
    });

    return HostView;
});