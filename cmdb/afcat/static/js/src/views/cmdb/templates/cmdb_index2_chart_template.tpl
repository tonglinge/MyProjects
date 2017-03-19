<script>
require(['high_charts'], function (highcharts) {
    var chart_dom_map = {
        asset: 'server-chart-contain',
        asset_count: 'server-count-chart-contain',
        equipment: 'equipment-chart-contain',
        equipment_count: 'equipment-count-chart-contain',
        host: 'host-chart-contain',
        itemset: 'host-item-chart-contain'
    };
    var tagname = chart_dom_map["<%= name %>"];
Highcharts.setOptions({
    colors: ['#001F48','#F8B123','#C53C50','#2F4F4F','#D6626F','#26415C','#BC123F','#425891','#FAAB2A','#DB5D73','#4B657E']
});
var colors = Highcharts.getOptions().colors,
    categories = ['刀片服务器', '路由器','刀片','路由器'],
    data = [{
        y: 55.11,
        color: colors[0],
        drilldown: {
            name: '刀片服务器',
            categories: ['虚拟主机', '小型机', 'OC服务器', '刀片服务器'],
            data: [10.85, 7.35, 33.06, 3.85],
            color: colors[0]
        }
    }, {
        y: 16.89,
        color: colors[1],
        drilldown: {
            name: '路由器',
            categories: ['虚拟主机', '小型机', 'OC服务器', '刀片服务器'],
            data: [5.35, 6.54, 3, 1],
            color: colors[1]
        }
    }, {
        y: 10,
        color: colors[2],
        drilldown: {
            name: '刀片',
            categories: ['虚拟主机', '小型机', 'OC服务器', '刀片服务器'],
            data: [4, 2, 1, 3],
            color: colors[2]
        }
    },
            {
                y: 18,
                color: colors[3],
                drilldown: {
                    name: '服务器',
                    categories: ['虚拟主机', '小型机', 'OC服务器', '刀片服务器'],
                    data: [4, 8, 3, 3],
                    color: colors[3]
                }
            }],
    browserData = [],
    versionsData = [],
    i,
    j,
    dataLen = data.length,
    drillDataLen,
    brightness;
for (i = 0; i < dataLen; i += 1) {
    // 添加浏览器数据
    browserData.push({
        name: categories[i],
        y: data[i].y,
        color: data[i].color
    });
    // 添加版本数据
    drillDataLen = data[i].drilldown.data.length;
    for (j = 0; j < drillDataLen; j += 1) {
        brightness = 0.2 - (j / drillDataLen) / 5;
        versionsData.push({
            name: data[i].drilldown.categories[j],
            y: data[i].drilldown.data[j],
            color: Highcharts.Color(data[i].color).brighten(brightness).get()
        });
    }
}
Highcharts.chart(tagname, {
    chart: {
        type: 'pie'
    },
    title: {
        text: '监控'
    },
    subtitle: {
        text: '内环为浏览器品牌占比，外环为具体的版本'
    },
    yAxis: {
        title: {
            text: '总百分比市场份额'
        }
    },
    plotOptions: {
        pie: {
            shadow: false,
            center: ['50%', '50%']
        }
    },
    tooltip: {
        valueSuffix: '%'
    },
    series: [{
        name: '浏览器',
        data: browserData,
        size: '60%',
        dataLabels: {
            formatter: function () {
                return this.y > 5 ? this.point.name : null;
            },
            color: 'black',
            distance: -30
        }
    }, {
        name: '版本',
        data: versionsData,
        size: '80%',
        innerSize: '60%',
        dataLabels: {
            formatter: function () {
                // 大于1则显示
                return this.y > 1 ? '<b>' + this.point.name + ':</b> ' + this.y + '%'  : null;
            }
        }
    }]
});



})
</script>