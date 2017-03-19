<div id="main" style="height:300px;"></div>
<script type="text/javascript">
    Highcharts.chart('main', {

        chart: {
            type: 'column'
        },
        credits: {
            enabled: false
        },
        title: {
            text: null
        },

        xAxis: {
            categories: [<%= group_status_info.group_name %>]
        },
        yAxis: {
            allowDecimals: false,
            min: 0,
            title: {
                text: 'Number of fruits'
            }
        },

        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                        this.series.name + ': ' + this.y + '<br/>' +
                        'Total: ' + this.point.stackTotal;
            }
        },

        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },

        series: [{
            name: '故障',
            color: "#dd4b39",
            data: [<%= group_status_info.host_issue_count %>],
            stack: 'male'
        }, {
            name: '正常',
            color: "#00a65a",
            data: [<%= group_status_info.host_normal_count %>],
            stack: 'male'
        }]
    });
</script>