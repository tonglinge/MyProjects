<div class="box box-info" id="host-manager">
    <div class="box-header">
        <div class="col-sm-6"><h4>主机管理</h4></div>
    </div>
    <div class="box-body">
        <ul class="nav nav-tabs" id="host-tabs">
            <li class="active"><a href="#tab_0" data-toggle="tab" aria-expanded="true">基础信息</a></li>
            <li class=""><a href="#tab_1" data-toggle="tab" aria-expanded="false">CPU 内存信息</a></li>
            <li class=""><a href="#tab_2" data-toggle="tab" aria-expanded="false">IP地址信息</a></li>
            <li class=""><a href="#tab_3" data-toggle="tab" aria-expanded="false">板卡</a></li>
            <li class=""><a href="#tab_4" data-toggle="tab" aria-expanded="false">存储信息</a></li>
            <li class=""><a href="#tab_5" data-toggle="tab" aria-expanded="false">安装软件</a></li>
            <li class=""><a href="#tab_6" data-toggle="tab" aria-expanded="false">联系人</a></li>
        </ul>

        <div class="tab-content">
            <div class="tab-pane active" id="tab_0">
                <table class="table table-bordered table-hover dataTable server-table">
                    <tr>
                        <th>主机名：</th><td><%= server.hostname %></td><th>主机类型：</th><td><%= server.type %></td><th>宿主机：</th><td><%= server.ownserver %></td>
                    </tr>
                    <tr><th>型号：</th><td><%= server.model %></td><th>分区：</th><td><%= server.partition %></td><th>网络域：</th><td><%= server.netarea %></td></tr>
                    <tr><th>F5策略：</th><td><%= server.balancetype %></td><th>购买日期：</th><td><%= server.tradedate %></td><th>过保日期：</th><td><%= server.expiredate %></td></tr>
                    <tr><th>运行状态：</th><td colspan="5"><%= server.runningstatus %></td></tr>
                    <tr><th>所属业务线：</th><td colspan="5"><%= server.business %></td></tr>
                    <tr><th>备注:</th><td colspan="5"><%= server.remark %></td></tr>
                </table>
            </div>
            <div class="tab-pane" id="tab_1">
                <table class="table table-bordered table-hover dataTable server-table">
                    <tr><th>CPU型号</th><th>CPU数量</th><th>CPU核数(GHZ)</th><th>CPU主频</th><th>内存容量(G)</th><th>备注</th><th>操作</th></tr>
                    <% _.each(cpu, function(cpu){ %>
                    <tr>
                        <td><%= cpu.model %></td>
                        <td><%= cpu.cpucount %></td>
                        <td><%= cpu.corecount %></td>
                        <td><%= cpu.frequenct %></td>
                        <td><%= cpu.memory %></td>
                        <td><%= cpu.remark %></td>
                        <td style="display:none"><%= cpu.id %></td>
                        <td id="<%= cpu.id %>">
                            <a href="#" id="editCPU"><i class="fa fa-edit"></i></a>&nbsp;
                            <a href="#" id="delCPU"><i class="fa fa-remove"></i></a>
                        </td>
                    </tr>
                    <% }) %>
                </table>
                <div class="col-sm-5">
                    <div class="box-tools">
                        <a href="#" title="添加" class="addRelateInfo" id="addCPU"><i class="fa fa-plus"></i></a>
                    </div>
                </div>
            </div>
            <div class="tab-pane" id="tab_2">
                <table class="table table-bordered table-hover dataTable server-table">
                    <tr><th>IP地址</th><th>网关地址</th><th>IP类型</th><th>域名</th><th>vlan编号</th><th>备注</th><th>操作</th></tr>
                    <% _.each(ip, function(ip){ %>
                     <tr>
                         <td><%= ip.ipaddress %></td>
                         <td><%= ip.gatway %></td>
                         <td><%= ip.iptype %></td>
                         <td><%= ip.domain %></td>
                         <td><%= ip.vlan %></td>
                         <td><%= ip.remark %></td>
                         <td style="display:none"><%= ip.id %></td>
                         <td id="<%= ip.id %>">
                            <a href="#" id="editIP"><i class="fa fa-edit"></i></a>&nbsp;
                            <a href="#" id="delIP"><i class="fa fa-remove"></i></a>
                         </td>
                     </tr>
                    <% }) %>
                </table>
                <div class="col-sm-5">
                    <div class="box-tools">
                        <a href="#" title="添加" class="addRelateInfo" id="addIP"><i class="fa fa-plus"></i></a>
                    </div>
                </div>
            </div>
            <div class="tab-pane" id="tab_3">
                <table class="table table-bordered table-hover dataTable server-table">
                      <tr><th>SN</th><th>类型</th><th>型号</th><th>厂商</th><th>MAC/WWN</th><th>槽位</th><th>端口数</th><th>备注</th><th>操作</th></tr>

                         <% _.each(card, function(card){ %>
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
                                 <td id="<%= card.id %>">
                                     <a href="#" id="editServerHostCard"><i class="fa fa-edit"></i></a>&nbsp;
                                     <a href="#" id="delServerHostCard"><i class="fa fa-remove"></i></a>
                                     <a type="button" class="btn btn-box-tool" id="server-host-card-detail"><i class="fa fa-th"></i></a>
                                 </td>
                             </tr>
                         <% }) %>
                </table>
                <div class="col-sm-5">
                    <div class="box-tools">
                        <a href="#" title="添加" class="addRelateInfo" id="addServerHostCard"><i class="fa fa-plus"></i></a>
                    </div>
                </div>

            </div>
            <div class="tab-pane" id="tab_4">
                <table class="table table-bordered table-hover dataTable server-table">
                     <tr><th>VG名</th><th>VG大小</th><th>Raid类型</th><th>备注</th><th>操作</th></tr>
                      <% _.each(vg, function(vg){ %>
                     <tr>
                         <td><%= vg.vgname %></td>
                         <td><%= vg.vgsize %></td>
                         <td><%= vg.raidtype %></td>
                         <td><%= vg.remark %></td>
                         <td style="display:none"><%= vg.id %></td>
                         <td id="<%= vg.id %>">
                             <a href="#" id="edit-vg" ><i class="fa fa-edit"></i></a>&nbsp;
                             <a href="#" id="del-vg"><i class="fa fa-remove"></i></a>
                             <button type="button" class="btn btn-box-tool" id="vg-detail"><i class="fa fa-th"></i></button>
                         </td>
                     </tr>
                      <% }) %>
                </table>
                <div class="col-sm-5">
                    <div class="box-tools">
                        <a href="#" title="添加" class="addRelateInfo" id="add-vg"><i class="fa fa-plus"></i></a>
                    </div>
                </div>
            </div>

            <div class="tab-pane" id="tab_5">
                <table class="table table-bordered table-hover dataTable server-table">
                      <tr><th>软件名称</th><th>软件类型</th><th>版本</th><th>lisence</th><th>服务端口</th><th>备注</th><th>操作</th></tr>
                       <% _.each(software, function(sw){ %>
                         <tr>
                             <td><%= sw.softname %></td>
                             <td><%= sw.softtype %></td>
                             <td><%= sw.version %></td>
                             <td><%= sw.lisence %></td>
                             <td><%= sw.port %></td>
                             <td><%= sw.remark %></td>
                             <td style="display:none"><%= sw.id %></td>
                             <td style="display:none"><%= sw.soft_id %></td>
                             <td id="<%= sw.id %>">
                                 <a href="#" id="editSoft"><i class="fa fa-edit"></i></a>&nbsp;
                                 <a href="#" id="delSoft"><i class="fa fa-remove"></i></a>
                             </td>
                         </tr>
                       <% }) %>
                </table>
                <div class="col-sm-6">
                    <div class="box-tools">
                        <a href="#" title="添加" class="addRelateInfo" id="addSoft"><i class="fa fa-plus"></i></a>
                    </div>
                </div>
            </div>
            <div class="tab-pane" id="tab_6">
                <table class="table table-bordered table-hover dataTable server-table">
                     <tr><th>联系人</th><th>手机</th><th>座机</th><th>角色类型</th><th>邮箱</th><th>备注</th><th>操作</th></tr>
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
                                <a href="#" id="editStaff"><i class="fa fa-edit"></i></a>&nbsp;
                                <a href="#" id="delStaff"><i class="fa fa-remove"></i></a>
                            </td>
                        </tr>
                      <% }) %>
                </table>
                <div class="col-sm-5">
                    <div class="box-tools">
                        <a href="#" title="添加" class="addRelateInfo" id="addStaff"><i class="fa fa-plus"></i></a>
                    </div>
                </div>

            </div>
        </div>
    </div>
</div>

<div class="col-sm-6" id="CPUModal">
</div>
<div class="col-sm-6" id="IPModal">
</div>
<div class="col-sm-6" id="CardModal"> </div>
<div class="col-sm-6" id="VGModal"> </div>
<div class="col-sm-6" id="softwareModal"> </div>
<div class="col-sm-6" id="staffModal"> </div>











