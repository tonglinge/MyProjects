<tr>
    <th width="110px"><span style="color:red">*</span>VS名称：</th>
    <td><input type="text" class="form-control must-input" name="vsname" id="vsname" ></td>
    <th width="100px"><span style="color:red">*</span>VS地址:</th>
    <td><input type="text" class="form-control" name="vsaddr" id="vsaddr" placeholder=""></td>
    <th width="110px"><span style="color:red">*</span>端口:</th>
    <td><input type="number" style="width:200px;" class="form-control" name="port" id="port" placeholder="端口"></td>
</tr>
<tr>
    <th>DNS域名：</th>
    <td><input type="text" id="dnsdomain" class="form-control">
    <th>数据中心：</th>
    <td>
        <select class="form-control" id="datacenter">
            <option value="0">-请选择-</option>
            <%_.each(basedatacenter, function(datacenter){ %>
            <option value="<%=datacenter.id %>"><%=datacenter.name %></option>
            <%}) %>
        </select>
    </td>
    <th><span style="color:red">*</span>网络区域：</th>
    <td>
        <select class="form-control" id="netarea">
            <option value="0">-请选择-</option>
            <%_.each(basenetarea, function(area){ %>
            <option value="<%=area.id%>"><%=area.name %></option>
            <%}) %>
        </select>
    </td>
</tr>
<tr>
    <th>业务模块:</th>
    <td>
        <div class="row">
            <div class="col-sm-12">
                <div class="input-group">
                    <i class="clearable glyphicon glyphicon-remove"
                       style="position: absolute; top: 12px; right: 35px; z-index: 4; cursor: pointer; font-size: 12px; display: none;"></i>
                    <input type="text" class="form-control" id="combox-project" autocomplete="off" data-id="0">
                    <div class="input-group-btn">
                        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="">
                            <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-right" role="menu"
                            style="padding-top: 0px; max-height: 375px; max-width: 800px; overflow: auto; width: auto; transition: 0.3s; left: -132px; right: auto; min-width: 165px;"></ul>
                    </div>
                    <!-- /btn-group -->
                </div>
            </div>
        </div>

        <select multiple class="form-control" namd="business" id="business" style="margin-top: 6px;">

        </select>
    </td>
    <th><span style="color:red">*</span>SNAT地址池:</th>
    <td>
        <textarea class="form-control" name="snataddr" id="snataddr" style="height:110px;resize: none"
                  placeholder="每行一个IP"></textarea>
    </td>
    <th><span style="color:red">*</span>服务器地址池：</th>
    <td><textarea class="form-control" name="pooladdr" id="pooladdr" style="height:110px;resize: none"
                  placeholder="每行一个IP"></textarea></td>
</tr>
<tr>
    <th>所属设备：</th>
    <td>
        <select class="form-control" name="equipment" id="equipment">

        </select>
    </td>
    <th>主机类型:</th>
    <td>
        <input type="text" class="form-control" name="hosttype" id="hosttype" placeholder="P780">
    </td>
    <th>主机名：</th>
    <td>
        <input type="text" class="form-control" name="hostname" id="hostname" placeholder="多个用逗号(,)分隔">
    </td>
</tr>
<tr>
    <th>VLAN：</th>
    <td><input type="text" class="form-control" name="vlan" id="vlan" placeholder=""></td>
    <th>负载策略：</th>
    <td>
        <select class="form-control" name="ploy" id="ploy">
            <% _.each(basebalancetype, function(ploy){ %>
            <option value="<%=ploy.id %>"><%=ploy.typename%></option>
            <%}) %>
        </select>
    </td>
    <th></th>
    <td>
    </td>
</tr>
<tr>
    <th>备注:</th>
    <td colspan="5">
        <input type="text" class="form-control" name="remark" id="remark" placeholder="">
    </td>
</tr>
<tr>
    <td colspan="6">
        <div class="col-sm-4"></div>
        <div class="col-sm-4">
            <button type="button" class="btn btn-primary submit-btn" id="save-and-add">保存并新增</button>
            <button type="button" class="btn btn-primary submit-btn" id="save-and-back">保存并返回</button>
            <button type="button" class="btn btn-primary submit-btn" id="nosave-back">返回</button>
            <hidden id="action" action="new"></hidden>
        </div>
        <div class="col-sm-4">
            <span id="error-message"></span>
        </div>
    </td>
</tr>
