<div class="col-md-12">
    <div class="box box-info">
        <div class="box-header with-border">
            <h5><%= name %></h5>
            <div class="box-tools pull-right">
                <input name="switch_status" type="checkbox" checked/>
                <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i>
                </button>
            </div>
            <div class="col-md-6">
                <div class="input-group">
                    <div class="input-group-addon">
                        <i class="fa fa-clock-o"></i>
                    </div>
                    <input type="text" name="history" class="form-control pull-right" id="history<%= graph_id %>">
                </div>
            </div>
        </div>
        <div class="box-body">
            <div id="<%= graph_id %>" style="height:300px;" class="col-md-12 col-sm-12"></div>
        </div>
    </div>
</div>

<script type="text/javascript">
    require(['jquery'], function ($) {
        $("[name='switch_status']").bootstrapSwitch();
        $('#history' + "<%= graph_id %>").daterangepicker(
                {
                    timePicker: true,
                    autoUpdateInput: true,
                    timePickerIncrement: 15,
                    timePicker24Hour: true,
                    locale: {format: 'YYYY-MM-DD HH:mm:ss', separator: ' / '}
                }
        );
        Highcharts.chart("<%= graph_id %>", {
            title: {
                text: null
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: [<%= date %>]
            },
            yAxis: {
                title: {
                    text: null
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: ''
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [
                    <% _.each(data, function(item_data){ %>
                        {
                            name: '<%= item_data.item_name %>',
                            data: [<%= item_data.values %>]
                        },
                    <% }) %>
                ]
        });
    })
</script>