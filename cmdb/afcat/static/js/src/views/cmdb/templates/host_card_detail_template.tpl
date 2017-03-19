<div class="box box-info">
    <div class="box-header">
        <div class="col-sm-6"><h3 class="box-title">板卡</h3></div>
        <div class="col-sm-5">
            <div class="box-tools pull-right">
                <button type="button" href="#" class="btn btn-success" id="history-back"><<返回</button>
            </div>
        </div>
    </div>
    <div class="box-body">
    <div class="row">
        <div class="col-sm-12">
            <table class="table table-bordered table-hover dataTable">
                <thead>
                      <tr><th>SN</th><th>类型</th><th>型号</th><th>厂商</th><th>MAC/WWN</th><th>槽位</th><th>端口数</th><th>备注</th></tr>
                </thead>
                <tbody>
                    <tr>
                         <td><%= card.sn %></td>
                         <td><%= card.typename %></td>
                         <td><%= card.model %></td>
                         <td><%= card.factory %></td>
                         <td><%= card.mac %></td>
                         <td><%= card.slot %></td>
                         <td><%= card.portcount %></td>
                         <td><%= card.remark %></td>
                         <td style="display:none"><%= card.id %></td>
                     </tr>
                </tbody>
            </table>
        </div>
    </div>

</div>
</div>

<div class="box box-info">
    <div class="box-header">
        <div class="col-sm-6"><h3 class="box-title">板卡端口</h3></div>
        <div class="col-sm-5">

        </div>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table class="table table-bordered table-hover dataTable">
                    <thead>
                        <tr >
                            <th colspan="3" class="text-center">本端端口</th>
                            <th colspan="3" class="text-center">对端端口</th><th colspan="2"></th>
                        </tr>
                        <tr>
                            <th class="text-center">本端端口</th>
                            <th class="text-center">本端类型</th>
                            <th class="text-center">VLAN</th>
                            <th class="text-center">对端端口</th>
                            <th class="text-center">对端设备</th>
                            <th class="text-center">对端类型</th>
                            <th class="text-center">备注</th>
                            <th class="text-center">操作</th>
                        </tr>
                    </thead>
                    <tbody id="portmap">
                        <% _.each(ports, function(port){ %>
                            <tr>
                                <td style="width:100px"><input class="form-control input-sm"  value="<%= port.portname %>"  /></td>
                                <td style="width:150px"><input class="form-control input-sm"  value="<%= port.porttype %>" /></td>
                                <td style="width:80px" > <input class="form-control input-sm" value="<%= port.vlan %>" /></td>

                                <td style="width:100px">
                                      <input class="form-control input-sm"  type="text"  value="<%= port.targetport %>" id="targetport-<%= port.id %>" class="form-control" disabled="disabled">
                                </td>

                                <td style="width:200px"><input class="form-control input-sm"  value="<%= port.targetasset%>" id="targetasset-<%= port.id %>" disabled="disabled"/></td>
                                <td style="width:100px"><input class="form-control input-sm"  value="<%= port.targettype %>" id="targettype-<%= port.id %>" disabled="disabled"/></td>
                                <td style="width:200px"><input class="form-control input-sm"  value="<%= port.remark %>" /></td>
                                <td style="display:none"><input type="text" value="<%= port.id %>" /></td>
                                <td style="width:100px">
                                    <button type="button" href="#" class="btn btn-box-tool" id="edit-port"><span class="fa fa-check"></span></button>
                                    <button type="button" href="#" class="btn btn-box-tool" id="del-port"><span class="fa fa-remove"></span></button>
                                </td>
                            </tr>
                        <% }) %>

                    </tbody>

                </table>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-5">
                <div class="box-tools">
                    <button type="button" href="#" class="btn btn-box-tool" id="add-port" title="添加端口"><i class="fa fa-plus"></i> </button>
                </div>
            </div>
        </div>
    </div>


</div>
