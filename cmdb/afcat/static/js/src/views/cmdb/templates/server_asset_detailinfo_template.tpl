<div class="box box-info">
    <div class="box-header">
        <h4>基础信息</h4>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table class="table table-bordered table-hover dataTable server-table">
                    <tr>
                        <th>序列号：</th><td><%= sn %></td><th>服务器用途：</th><td><%= usetype %></td><th>服务器分类：</th><td><%= assettype %></td>
                    </tr>
                     <tr><th>厂商：</th><td><%= factory %></td><th>集成商：</th><td><%= integrator %></td><th>型号：</th><td><%= model %></td></tr>
                     <tr><th>所属机房：</th><td><%= room %></td><th>所属机柜：</th><td><%= cabinet %></td><th>单元信息：</th><td><%= unitinfo %></td></tr>
                     <tr><th>集群信息：</th><td><%= clusterinfo %></td><th>CPU：</th><td><%= cpu %></td><th>内存：</th><td><%= memory %></td></tr>
                     <tr><th>所属环境：</th><td><%= netarea %></td><th>服务器状态：</th><td><%= assetstatus %></td><th>硬件联系人：</th><td><%= contact %></td></tr>
                    <tr>
                        <th>购买日期：</th>
                        <td><%= tradedate %></td>
                        <th>过保期：</th>
                        <td><%= expiredate %></td>
                        <th>开始保修期：</th>
                        <td><%= startdate %></td>
                    </tr>

                     <tr><th>管理IP：</th><td><%= manageip %></td><th>主机数量：</th><td><%= hostcount %></td></tr>
                    <tr><th>备注:</th><td colspan="5"><%= remark %></td></tr>
                </table>
            </div>
        </div>
    </div>
</div>

    


