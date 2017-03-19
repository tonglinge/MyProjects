/**
 * Created by zengchunyun on 2016/11/16.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var ApplicationItemView = require("./tracker_application_item_view").ApplicationItemView;

    $("[name='switch_status']").bootstrapSwitch();
    $("[name='cpu']").bootstrapSwitch();
    $("[name='mem']").bootstrapSwitch();
    $("[name='disk']").bootstrapSwitch();
    $("[name='network']").bootstrapSwitch();
    var gaugeOptions = {
        chart: {
            type: 'solidgauge'
        },
        credits: {
            enabled: false
        },
        title: null,
        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
        tooltip: {
            enabled: true
        },
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickAmount: 10,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };
    $('#cpu').highcharts(Highcharts.merge(gaugeOptions, {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'CPU状态'
        },
        xAxis: {
            type: 'datetime',
            labels: {
                overflow: 'justify'
            }
        },
        yAxis: {
            title: {
                text: ' speed (m/s)'
            },
            minorGridLineWidth: 0,
            gridLineWidth: 0,
            alternateGridColor: null,
            plotBands: [{ // Light air
                from: 0,
                to: 5,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: '正常',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Light breeze
                from: 5,
                to: 9,
                color: 'rgba(92, 184, 92, 1)',
                label: {
                    text: '轻微',
                    style: {
                        color: '#5cb85c'
                    }
                }
            }, { // Gentle breeze
                from: 9,
                to: 13,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: '一般',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Moderate breeze
                from: 13,
                to: 16,
                color: 'rgba(0, 0, 0, 0)',
                label: {
                    text: '警告',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Fresh breeze
                from: 16,
                to: 18,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: '严重',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Strong breeze
                from: 18,
                to: 20,
                color: 'rgba(0, 0, 0, 0)',
                label: {
                    text: '告急',
                    style: {
                        color: '#606060'
                    }
                }
            }]
        },
        tooltip: {
            valueSuffix: ' m/s'
        },
        plotOptions: {
            spline: {
                lineWidth: 4,
                states: {
                    hover: {
                        lineWidth: 5
                    }
                },
                marker: {
                    enabled: false
                },
                pointInterval: 3600000, // one hour
                pointStart: Date.UTC(2016, 11, 11, 0, 0, 0)
            }
        },
        series: [{
            name: '5min avg',
            color:"#5cb85c",
            data: [0.2, 0.8, 0.8, 0.8, 1, 1.3, 1.5, 2.9, 1.9, 2.6, 1.6, 3, 4, 3.6, 4.5, 4.2, 4.5, 4.5, 4, 3.1, 2.7, 4, 2.7, 2.3, 2.3, 4.1, 7.7, 7.1, 5.6, 6.1, 5.8, 8.6, 7.2, 9, 10.9, 1.5, 11.6, 1.1, 2, 2.3, 10.7, 9.4, 9.8, 9.6, 9.8, 9.5, 8.5, 7.4, 7.6]

        }, {
            name: '使用率',
            color: '#DC0000',
            data: [0, 0, 0.6, 0.9, 0.8, 0.2, 0, 0, 0, 0.1, 0.6, 0.7, 0.8, 0.6, 0.2, 0, 0.1, 0.3, 0.3, 0, 0.1, 0, 0, 0, 0.2, 0.1, 0, 0.3, 0, 0.1, 0.2, 0.1, 0.3, 0.3, 0, 3.1, 3.1, 2.5, 1.5, 1.9, 2.1, 1, 2.3, 1.9, 1.2, 0.7, 1.3, 0.4, 0.3]
        }],
        navigation: {
            menuItemStyle: {
                fontSize: '10px'
            }
        }

    }));
    //
    // // Bring life to the dials
    // setInterval(function () {
    //     // Speed
    //     var chart = $('#cpu').highcharts(),
    //         point,
    //         newVal,
    //         inc;
    //
    //     if (chart) {
    //         point = chart.series[0].points[0];
    //         inc = Math.round((Math.random() - 0.5) * 100);
    //         newVal = point.y + inc;
    //
    //         if (newVal < 0 || newVal > 200) {
    //             newVal = point.y - inc;
    //         }
    //
    //         point.update(newVal);
    //     }
    //
    // }, 2000);
    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
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


    var ApplicationView = Backbone.View.extend({
        events: {},
        initialize: function (options) {
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true)
        },
        addAll: function () {
            var models = this.collection.models;
            //针对每次reload数据时需要清空整个app页面数据，指定判断关键属性，用来决定是否对app内容清空
            if(this.collection.reseted && models.length > 0 && models[0].has("hosts_status")){
                this.$el.find('.hosts_tbody').html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new ApplicationItemView({model: model});
            this.$el.find(".hosts_tbody").append(view.render().el);
        }
    });
    return ApplicationView;

});