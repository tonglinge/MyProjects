<div class="box box-info" id="server">
    <div class="box-header">
        <div class="col-sm-6"><h4>网络设备</h4></div>
    </div>
    <div class="box-body">
        <ul class="nav nav-tabs" id="equipment-tab">
            <li class="active"><a href="#tab_0" data-toggle="tab" aria-expanded="true">基础信息</a></li>
            <li class=""><a href="#tab_1" data-toggle="tab" aria-expanded="false">板卡</a></li>
            <li class=""><a href="#tab_2" data-toggle="tab" aria-expanded="false">责任人</a></li>
        </ul>

        <div class="tab-content">
            <div class="tab-pane active" id="tab_0">

                <table class="table table-bordered">
                    <tr><th>资产编号：</th><td><%= server.assetno %></td><th>设备序列号：</th><td><%= server.sn %></td><th>类型：</th><td><%= server.assettype %></td></tr>
                     <tr><th>所属机房：</th><td><%= server.room %></td><th>所属机柜：</th><td><%= server.cabinet %></td><th>柜内位置：</th><td><%= server.slotindex %></td></tr>
                    <tr><th>服务开始日期：</th><td><%= server.tradedate %></td><th>过保日期：</th><td><%= server.expiredate %></td><th>厂商：</th><td><%= server.factory %></td></tr>
                    <tr><th>设备型号：</th><td><%= server.model %></td><th>所属环境：</th><td><%= server.netarea %></td><th>设备管理IP：</th><td><%= server.manageip %></td></tr>
                     <tr><th>状态：</th><td><%= server.status %></td><th>设备名称：</th><td><%= server.assetname %></td><th>电源数量：</th><td><%= server.powertype %></td></tr>
                     <tr><th>用途:</th><td><%= server.usetype %></td><th>备注:</th><td colspan="5"><%= server.remark %></td></tr>
                    <% remain = extend.length%3 %>
                    <% rows = Math.ceil(extend.length/3) %>
                    <% for(var i=0;i<(rows);i++){ %>
                        <tr>
                            <% if(i<(rows-1)){ %>
                                <% for(var j=0;j<3;j++){ %>
                                    <th><%= extend[i*3+j].label %>：</th>
                                    <td><%= extend[i*3+j].value %></td>
                                <% } %>
                            <% }else{ %>
                                <% for(var j=0;j<(remain);j++){ %>
                                    <th><%= extend[i*3+j].label %>：</th>
                                    <td><%= extend[i*3+j].value %></td>
                                <% } %>
                            <% } %>
                        </tr>
                    <% } %>
                </table>

            </div>
            <div class="tab-pane" id="tab_1">
                <table class="table table-bordered table-hover dataTable card-table text-center">
                    <thead>
                        <tr><th>板卡名称</th><th>SN</th><th>型号</th><th>槽位</th><th>端口数</th><th>备注</th><th>操作</th></tr>
                    </thead>
                    <tbody id="card-tbody">
                    <% _.each(card, function(card){ %>
                        <tr>
                            <td><input class="form-control" value="<%= card.cardname %>" /></td>
                            <td><input class="form-control" value="<%= card.sn %>" /></td>
                            <td><input class="form-control" value="<%= card.model %>" /></td>
                            <td><input class="form-control" value="<%= card.slot %>" /></td>
                            <td><input class="form-control" value="<%= card.ports.length %>" disabled="disabled" style="width:60px;"/></td>
                            <td><input class="form-control" value="<%= card.remark %>" /></td>
                            <td style="display:none"><%= card.id %></td>
                            <td id="opration" style="display:none"></td>
                            <td id="<%= card.id %>" style="width:250px;">
                                <button type="button" href="#" class="btn btn-box-tool" id="editCard"><span class="fa fa-check"></span></button>
                                <button type="button" href="#" class="btn btn-box-tool" id="delCard"><span class="fa fa-remove"></span></button>
                                <button type="button" href="#" class="btn btn-box-tool" id="portDetail"><i class="fa fa-th"></i></button>
                            </td>
                        </tr>

                    <% }) %>
                    </tbody>

                </table>
                <div class="col-sm-5">
                    <div class="box-tools">
                        <a type="button" href="#" class="addRelateInfo"  id="addCard"><i class="fa fa-plus"></i>
                        </a>
                    </div>
                </div>
            </div>
            <!-- /.tab-pane -->
            <div class="tab-pane" id="tab_2">
                <table class="table table-bordered table-hover dataTable staff-table text-center">
                    <thead>
                        <tr><th>责任人</th><th>手机</th><th>座机</th><th>角色类型</th><th>邮箱</th><th>备注</th><th>操作</th></tr>
                    </thead>
                    <tbody id="staff-tbody">
                    <% _.each(staffs, function(staff){ %>
                        <tr>
                            <td><%= staff.name %></td>
                            <td><%= staff.mobile %></td>
                            <td><%= staff.tel %></td>
                            <td><%= staff.role %></td>
                            <td><%= staff.email %></td>
                            <td><%= staff.remark %></td>
                            <td style="display:none"><%= staff.id %></td>
                            <td style="display:none"><%= staff.staff_id %></td>
                            <td id="opration" style="display:none"></td>
                            <td id="<%= staff.id %>">
                                <a type="button" href="#" class="box-tool" id="editStaff"><span class="fa fa-edit"></span></a>
                                <a type="button" href="#" class="box-tool" id="delStaff"><span class="fa fa-remove"></span></a>
                            </td>
                        </tr>
                      <% }) %>
                    </tbody>

                </table>
                <div class="col-sm-5">
                    <div class="box-tools">
                        <a type="button" href="#" class="addRelateInfo"  id="addStaff"><i class="fa fa-plus"></i>
                        </a>
                    </div>
                </div>
            </div>
            <!-- /.tab-pane -->

        </div>
    </div>
</div>

<div id="cardDetail" style="display:none"></div>
<div class="col-sm-6" id="cardModal"> </div>
<div class="col-sm-6" id="staffModal"> </div>

