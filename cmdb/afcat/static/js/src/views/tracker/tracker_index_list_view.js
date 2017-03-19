/**
 * Created by zengchunyun on 2016/11/16.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var IndexItemView = require("./tracker_index_item_view").IndexItemView;

    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        credits: {
            enabled: false
        },
        title: {
            text: '未处理的事件'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    },
                    connectorColor: 'silver'
                }
            }
        },
        series: [{
            type: 'pie',
            name: '事件比例',
            data: [
                ['系统',   45.0],
                ['物理机',       26.8],
                {
                    name: '虚拟机',
                    y: 12.8,
                    sliced: true,
                    selected: true
                },
                ['网络',    8.5],
                ['存储',     6.2],
                ['数据库',   0.7]
            ]
        }]
    });


    var IndexView = Backbone.View.extend({
        events: {},
        initialize: function (options) {
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            var self = this;
            // this.collection.fetchData(false, {method: "groups.get"},{callback:this.getGroupsStatus, args:self})
        },
        addAll: function () {
            var models = this.collection.models;
            //针对每次reload数据时需要清空整个app页面数据，指定判断关键属性，用来决定是否对app内容清空
            if(this.collection.reseted && models.length > 0 && models[0].has("groups_status")){
                this.$el.find('.hosts_tbody').html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new IndexItemView({model: model});
            this.$el.find(".index_hosts_status").html(view.render().el);
        },
        getGroupsStatus: function (self) {
            var models = self.collection.models;
            if(models.length > 0 && models[0].has("groups_id")){
                var groups_id = models[0].get('groups_id');
                // self.collection.fetchData(true, {get_groups_status: true,groups_id: JSON.stringify(groups_id)})
            }
        }
    });
    return IndexView;

});