<!-- 设备增长趋势图 -->
<div class="c-host-wapper" style="height:320px;">
    <div class="page-header">
        <h4 id="page-header-title">设备增长趋势图</h4>
    </div>
    <div class="c-host-area" id="index-main-echar">
        <div id="repot_chart"></div>
        <script>
            require(['echarts'], function (echarts) {
                var myChart5 = echarts.init(document.getElementById('repot_chart'));
                option5 = {
                    title: {
                        show: true,
                        text: 'CMBD设备统计',
                        textStyle: {
                            fontWeight: 'normal',
                            fontSize: 12,
                            color: '#333'
                        }
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['服务器', '网络设备', '主机设备']
                    },
                    grid: {
                        top: '20%',
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    }
                    ,
                    toolbox: {
                        feature: {
                            saveAsImage: {
                                shwo: true,
                                title: '保存图片',
                                pixelRatio: 2
                            }

                        }
                    }
                    ,
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: ['2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12', '2017-01', '2017-02', '2017-03']
                    }
                    ,
                    yAxis: {
                        type: 'value'
                    }
                    ,
                    series: [
                        {
                            name: '服务器',
                            type: 'line',
                            stack: '总量',
                            data: [0,0,0,0,0,1,2,3,4,5,6]
                        },
                            {
                            name: '网络设备',
                            type: 'line',
                            stack: '总量',
                            data: [0,1,3,4,6,7,12,32,34,45,61]
                        },
                            {
                            name: '主机设备',
                            type: 'line',
                            stack: '总量',
                            data: [0,0,0,0,0,11,21,32,34,45,36]
                        }

                    ]
                }
                ;
                myChart5.setOption(option5);
            })
        </script>
    </div>
</div>
<!-- /事件列表 -->
<div class="c-host-wapper" style="height:220px;">
    <div class="page-header">
        <h4 id="page-header-title">事件列表</h4>
    </div>
    <div class="c-host-area" id="index-main-event">
        <table class="table table-hover">
            <thead>
            <tr>
                <th style="width:50px">序号</th>
                <th class="text-center">事件</th>
                <th style="width:100px">事件日期</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>1</td>
                <td>服务器 AAA 维保日期 (2017-03-10) 即将过期</td>
                <td>2017-03-05</td>
            </tr>
            <tr>
                <td>1</td>
                <td>IP地址 40.1.2.32 已无设备使用,待回收</td>
                <td>2017-03-05</td>
            </tr>
            <tr>
                <td>1</td>
                <td>服务器 AAA 维保日期 (2017-03-10) 即将过期</td>
                <td>2017-03-05</td>
            </tr>
            <tr>
                <td>1</td>
                <td>服务器 AAA 维保日期 (2017-03-10) 即将过期</td>
                <td>2017-03-05</td>
            </tr>
            <tr>
                <td>1</td>
                <td>服务器 AAA 维保日期 (2017-03-10) 即将过期</td>
                <td>2017-03-05</td>
            </tr>
            </tbody>
        </table>
    </div>
</div>