<div class="box box-info">
    <div class="box-header">
        <div class="col-sm-6"><h3 class="box-title">VG</h3></div>
        <div class="col-sm-5">
            <div class="box-tools pull-right">
                <button type="button" class="btn btn-success" id="history-back"><<返回</button>
            </div>
        </div>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table class="table table-bordered table-hover dataTable vg-table">
                    <thead>
                        <tr><th>VG名</th><th>VG大小</th><th>RAID类型</th><th>备注</th></tr>                </thead>
                    <tbody>
                        <tr>
                            <td><%= vg.vgname %></td>
                            <td><%= vg.vgsize %></td>
                            <td><%= vg.raidtype %></td>
                            <td><%= vg.remark %></td>
                            <td style="display:none"><input type="hidden" id="vg-id" value="<%= vg.id %>" /></td>
                        </tr>
                    </tbody>

                </table>
            </div>
        </div>

    </div>
</div>

<div class="row">
    <div class="col-sm-6">
        <div class="box box-info">
            <div class="box-header">
                <div class="col-sm-2"><h3 class="box-title">LV</h3></div>
                <div class="col-sm-3">

                </div>
            </div>
            <div class="box-body">
                <table class="table table-bordered table-hover dataTable card-table">
                    <thead>
                        <tr>
                            <th class="text-center" width="25%">LV名</th>
                            <th class="text-center" width="15%">LV大小</th>
                            <th class="text-center" width="20%">文件系统</th>
                            <th class="text-center" width="25%">备注</th>
                            <th class="text-center" width="15%">操作</th>
                        </tr>
                    </thead>
                    <tbody id="lv-tbody" vg-id="<%= vg.id %>">
                        <% _.each(vg.lv, function(lv){ %>
                         <tr>
                             <td><input type="text" class="form-control input-sm" value="<%= lv.lvname %>" /><span style="color: red;"></span></td>
                             <td><input type="number" class="form-control input-sm" value="<%= lv.lvsize %>" /><span style="color: red;"></span></td>
                             <td><input type="text" class="form-control input-sm" value="<%= lv.filesystem %>" /></td>
                             <td><input type="text" class="form-control input-sm" value="<%= lv.remark %>" /></td>
                             <td style="display:none"><%= lv.id %></td>
                             <td style="width:100px">
                                 <button href="#" class="btn btn-box-tool" id="edit-lv"><i class="fa fa-check"></i></button>&nbsp;
                                 <button href="#" class="btn btn-box-tool" id="del-lv"><i class="fa fa-remove"></i></button>
                             </td>
                         </tr>
                          <% }) %>
                    </tbody>

                </table>
                <div class="row">
                    <div class="col-sm-1">
                        <div class="box-tools">
                            <button type="button" href="#" class="btn btn-box-tool" id="add-lv" title="添加LV"><i class="fa fa-plus"></i> </button>
                        </div>
                    </div>
                    <div class="col-sm-3"></div>
                </div>
            </div>

        </div>
    </div>
    <div class="col-sm-6">
        <div class="box box-info">
            <div class="box-header">
                <div class="col-sm-2"><h3 class="box-title">PV</h3></div>
                <div class="col-sm-3">

                </div>
            </div>
            <div class="box-body">
                <table class="table table-bordered table-hover dataTable pv-table">
                    <thead>
                        <tr>
                            <th class="text-center" width="30%">PV/LUN</th>
                            <th class="text-center" width="20%">PV/LUN 大小</th>
                            <th class="text-center" width="35%">备注</th>
                            <th class="text-center" width="15%">操作</th>
                        </tr>
                    </thead>
                    <tbody id="pv-tbody" vg-id="<%= vg.id %>">
                        <% _.each(vg.pv, function(pv){ %>
                         <tr>
                             <td><input type="text" class="form-control input-sm" value="<%= pv.pvname %>" /><span style="color: red;"></span></td>
                             <td><input type="number" class="form-control input-sm" value="<%= pv.pvsize %>" /><span style="color: red;"></span></td>
                             <td><input type="text" class="form-control input-sm" value="<%= pv.remark %>" /></td>
                             <td style="display:none"><%= pv.id %></td>
                             <td style="width:100px">
                                 <button href="#" class="btn btn-box-tool" title="编辑" id="edit-pv" title="编辑"><i class="fa fa-check"></i></button>&nbsp;
                                 <button href="#" class="btn btn-box-tool" title="删除"  id="del-pv" titile="删除"><i class="fa fa-remove"></i></button>
                             </td>
                         </tr>
                          <% }) %>
                    </tbody>

                </table>
                <div class="row">
                    <div class="col-sm-1">
                        <div class="box-tools">
                            <button type="button" href="#" class="btn btn-box-tool pull-left" id="add-pv" title="添加PV"><i class="fa fa-plus"></i> </button>
                        </div>
                    </div>

                    <div class="col-sm-3"></div>
                </div>
            </div>
        </div>

    </div>
</div>