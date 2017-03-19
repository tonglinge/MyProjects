<div class="box box-info">
    <div class="box-header">
        <div class="col-sm-6"><h3 class="box-title">板卡【<%= card.cardname %>】-端口</h3></div>
        <div class="col-sm-5">
            <div class="box-tools pull-right">
                <button type="button" href="#" class="btn btn-success" id="portDetail"><<返回</button>
            </div>
        </div>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table class="table table-bordered table-striped dataTable localport-table">
                    <thead>
                        <tr>
                            <th class="text-center">本端端口</th>
                            <th class="text-center">本端类型</th>
                            <th class="text-center">VLAN</th>
                            <th class="text-center">备注</th>
                            <th class="text-center">操作</th>
                        </tr>
                    </thead>
                    <tbody id="portlist">
                        <% _.each(card.ports, function(port){ %>
                            <tr>
                                <td><input class="form-control" style="width:100px" value="<%= port.portname %>"  /></td>
                                <td><input class="form-control" style="width:100px" value="<%= port.porttype %>" /></td>
                                <td><input class="form-control" style="width:100px" value="<%= port.vlan %>" /></td>
                                <td><input class="form-control" style="width:300px" value="<%= port.remark %>" /></td>
                                <td style="display:none"><input type="text" value="<%= port.id %>" /></td>
                                <td>
                                    <button type="button" href="#" class="btn btn-box-tool" id="editPort"><span class="fa fa-check"></span></button>
                                    <button type="button" href="#" class="btn btn-box-tool" id="delPort"><span class="fa fa-remove"></span></button>
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
                    <button type="button" href="#" class="btn btn-box-tool" id="addPort" title="添加端口"><i class="fa fa-plus"></i> </button>
                </div>
            </div>
        </div>
    </div>

    <div class="box-header">
        <div class="col-sm-6"><h3 class="box-title">板卡【<%= card.cardname %>】-端口映射</h3></div>
        <div class="col-sm-5">

        </div>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table class="table table-bordered table-striped dataTable portmap-table">
                    <thead>
                        <tr>
                            <th class="text-center">本端端口</th>
                            <th class="text-center">对端端口</th>
                            <th class="text-center">对端设备</th>
                            <th class="text-center">对端类型</th>
                            <th class="text-center">备注</th>
                            <th class="text-center">操作</th>
                        </tr>
                    </thead>
                    <tbody id="portmap">
                        <% _.each(card.maps, function(map){ %>
                            <tr>
                                <td><input class="form-control" id="localport"  style="width:100px" value="<%= map.localportname %>"  disabled="disabled"/></td>
                                <td>
                                    <div class="input-group input-group-sm" style="width: 80px;">
                                      <div class="input-group-btn">
                                        <button type="button" class="btn btn-primary" id="choose-port"><i class="fa fa-list"></i></button>
                                      </div>
                                      <input style="width:70px" type="text" name="table_search" value="<%= map.targetportname %>" id="targetport-<%= map.mapid %>" class="form-control pull-right" disabled="disabled">
                                    </div>
                                </td>

                                <td><input class="form-control" style="width:300px" value="<%= map.targetasset%>" id="targetasset-<%= map.mapid %>" disabled="disabled"/></td>
                                <td><input class="form-control" style="width:80px" value="<%= map.targetporttype %>" id="targettype-<%= map.mapid %>" disabled="disabled"/></td>
                                <td><input class="form-control" style="width:300px" value="<%= map.remark %>" /></td>
                                <td style="display:none"><input type="text" value="<%= map.mapid %>" /></td>
                                <td style="display:none"><input type="text" id="targetid-<%= map.mapid %>" value="<%= map.targetportid %>"/></td>
                                <td>
                                    <button type="button" href="#" class="btn btn-box-tool" id="editMap"><span class="fa fa-check"></span></button>
                                    <button type="button" href="#" class="btn btn-box-tool" id="delMap"><span class="fa fa-remove"></span></button>
                                </td>
                            </tr>
                        <% }) %>
                    </tbody>

                </table>
                <div>
                    <input type="text" id="currChoose" chooseport="" targetportid=""  hidden>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-5">
                <div class="box-tools">
                    <button type="button" href="#" class="btn btn-box-tool" id="addMap" title="添加端口"><i class="fa fa-plus"></i> </button>
                </div>
            </div>
        </div>
    </div>
</div>

