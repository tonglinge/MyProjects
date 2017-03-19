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
    var data = [ ];
     <%_.each(series, function(series){ %>
        data.push(["<%= series.name %>", <%= series.value %>])
        <% }) %>
    Highcharts.setOptions({
        colors: ['#001F48','#F8B123','#C53C50','#264363','#D6626F','#26415C','#BC123F','#425891','#FAAB2A','#DB5D73','#4B657E']
    });
    Highcharts.chart(tagname, {
        credits: {
            enabled: false, //不显示LOGO
        },
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            padding: '0'
        },
        title: {
            text: '<%= title %>',
            align: 'center',
            verticalAlign: 'middle',
            style:{ "color": "#333333", "fontSize": "8px", fontWeight:"bold" },
            y: 0
        },
        tooltip: {
            headerFormat: '{series.name}<br>',
            pointFormat: '{point.name}'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    distance:1,
                    style: {fontSize: "8px", fontWeight:"thin" ,padding: '4px'},
                    formatter: function () {
                        var last_index = this.point.name.lastIndexOf("-");
                        var point_name = this.point.name.slice(0,last_index);
                        var colon_index = this.point.name.lastIndexOf(":");
                        var point_name2 = this.point.name.slice(0,colon_index);
                        return '<span style="color:'+this.point.color+'">' + point_name +'</span>';
                    },
                    verticalAlign:"'top'"
                },
                startAngle: 0,
                endAngle: 360,
                center: ['50%', '50%']
            }
        },

        series: [{
            type: 'pie',
            name: '<%= title %>',
            size: '64%',
            innerSize:"75%",
            animation: false,
            data: data,
        }],
        responsive: {
            rules: [{
                condition: {
                    minWidth: 400
                },
                chartOptions: {
                    plotOptions: {
                        pie: {dataLabels:{distance:20}}
                    }
                }
            }]
        }
});


})
</script>