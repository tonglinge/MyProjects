<h6><%= title %></h6>
<div id="<%= name %>" class="my_chart"></div>

<script>
    require(['echarts'], function (echarts) {
        var myChart1 = echarts.init(document.getElementById('<%= name %>'));
        var option1 = {
            title: {
                text: null,
            },
            color:['#666a99', '#60f83c','#fc5c76','#f9ff4d'],
            resize: {
                height: "auto",
                width: "auto"
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            grid: {
                top: 20,
                left: '3%',
                right: '4%',
                bottom: 20,
                containLabel: true
            },
            legend: {
                x: 'center',
                y: 'bottom',
                data: [<% _.each(legend,function(v,index){ %>'<%= v %>',<% }) %>],
                itemWidth: 10,
                itemHeight: 10,
                textStyle: {
                    fontSize: 12
                }
            },
            toolbox: {
                show: false,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {
                        show: true,
                        type: ['pie', 'funnel']
                    },
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            calculable: true,
            series: [
                {
                    name: "",
                    type: 'pie',
                    radius: [20, 110],
                    center: ['50%', '50%'],
                    roseType: 'radius',
                    label: {
                        normal: {
                            show: false
                        },
                        emphasis: {
                            show: false
                        }
                    },
                    data: [
                        <% _.each(series,function(edata){ %>
                        {value: '<%= edata.value %>', name: '<%= edata.name %>'},
                        <% }) %>
                    ]
                }
            ]
        };

        myChart1.setOption(option1);

    })

</script>
