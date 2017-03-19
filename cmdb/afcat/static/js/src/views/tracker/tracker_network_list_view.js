/**
 * Created by zengchunyun on 2016/11/16.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var NetworkItemView = require("./tracker_network_item_view").NetworkItemView;

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

    $('#mem').highcharts(Highcharts.merge(gaugeOptions, {
        chart: {
            type: 'area'
        },
        title: {
            text: '内存状态'
        },
        xAxis: {
            allowDecimals: false,
            labels: {
                formatter: function () {
                    return this.value; // clean, unformatted number for year
                }
            }
        },
        yAxis: {
            title: {
                text: '使用大小'
            },
            labels: {
                formatter: function () {
                    return this.value / 1000 + 'k';
                }
            }
        },
        tooltip: {
            pointFormat: '{series.name} produced <b>{point.y:,.0f}</b><br/>warheads in {point.x}'
        },
        plotOptions: {
            area: {
                pointStart: 2010,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [{
            name: '可用大小',
            color:"#5cb85c",
            data: [null, null, null, null, null, 6, 11, 32, 110, 235, 369, 640,
                22380, 21004, 17287, 14747, 13076, 12555, 12144, 11009, 10950,
                1005, 1436, 2063, 3057, 4618, 6444, 9822, 15468, 20434, 24126,

                26956, 27912, 28999, 28965, 27826, 25579, 25722, 24826, 24605,
                24304, 23464, 23708, 24099, 24357, 24237, 24401, 24344, 23586,
                27387, 29459, 31056, 31982, 32040, 31233, 29224, 27342, 26662,
                10871, 10824, 10577, 10527, 10475, 10421, 10358, 10295, 10104]
        }, {
            name: '使用大小',
            color: "#DC0000",
            data: [5, 25, 50, 120, 150, 200, 426, 660, 869, 1060, 1605, 2471, 3322,
                15915, 17385, 19055, 21205, 23044, 25393, 27935, 30062, 32049,
                5, 25, 50, 120, 150, 200, 426, 660, 869, 1060, 1605, 2471, 3322,
                4238, 5221, 6129, 7089, 8339, 9399, 10538, 11643, 13092, 14478,
                35000, 33000, 31000, 29000, 27000, 25000, 24000, 23000, 22000,
                33952, 35804, 37431, 39197, 45000, 43000, 41000, 39000, 37000,
                21000, 20000, 19000, 18000, 18000, 17000, 16000]
        }]

    }));

    $('#disk').highcharts(Highcharts.merge(gaugeOptions, {
        chart: {
            type: 'area'
        },
        credits: {
            enabled: false
        },
        title: {
            text: '磁盘状态'
        },
        xAxis: {
            allowDecimals: false,
            labels: {
                formatter: function () {
                    return this.value; // clean, unformatted number for year
                }
            }
        },
        yAxis: {
            title: {
                text: '使用大小'
            },
            labels: {
                formatter: function () {
                    return this.value / 1000 + 'k';
                }
            }
        },
        tooltip: {
            pointFormat: '{series.name} produced <b>{point.y:,.0f}</b><br/>warheads in {point.x}'
        },
        plotOptions: {
            area: {
                pointStart: 1940,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [{
            name: '可用大小',
            color:"#5cb85c",
            data: [null, null, null, null, null, 6, 11, 32, 110, 235, 369, 640,
                1005, 1436, 2063, 3057, 4618, 63444, 9822, 15468, 20434, 24126,
                27387, 29459, 31056, 31982, 32040, 31233, 29224, 27342, 26662,
                26956, 27912, 28999, 128965, 27826, 25579, 25722, 24826, 24605,
                24304, 23464, 23708, 24099, 24357, 24237, 24401, 24344, 23586,
                22380, 21004, 17287, 14747, 13076, 12555, 12144, 11009, 10950,
                10871, 10824, 10577, 10527, 10475, 10421, 10358, 10295, 10104]
        }, {
            name: '使用大小',
            color: "#DC0000",
            data: [null, null, null, null, null, null, null, null, null, null,
                5, 25, 50, 120, 150, 200, 426, 660, 869, 1060, 1605, 2471, 3322,
                4238, 5221, 61229, 7089, 8339, 9399, 10538, 11643, 13092, 14478,
                15915, 17385, 19055, 21205, 23044, 25393, 27935, 30062, 32049,
                33952, 35804, 37431, 39197, 45000, 43000, 41000, 39000, 37000,
                35000, 33000, 31000, 290200, 27000, 25000, 24000, 23000, 22000,
                21000, 20000, 19000, 18000, 18000, 17000, 16000]
        }]

    }));


    var NetworkView = Backbone.View.extend({
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
            var view = new NetworkItemView({model: model});
            this.$el.find(".hosts_tbody").append(view.render().el);
        }
    });
    return NetworkView;

});