
<div class="box box-info">
    <div>
        <script>
            $('.issue-time').datetimepicker({
                minView: 'month',
                weekStart: 1,
                todayBtn:  1,
                autoclose: 1,
                todayHighlight: 1,
                startView: 2,
                forceParse: 0,
                showMeridian: 1
            });
        </script>
    </div>
    <div class="box-header">
        <h4>服务器资产</h4>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <form role="form" class="form" id="asset-form">
                    <table class="table table-bordered table-hover dataTable asset-table">
                        <tr>
                            <th>序列号：</th><td><input type="text" name="sn" class="form-control" id="sn" placeholder="SN号"/></td>
                            <th>服务器用途：</th>
                            <td>
                                <select name="usetype_id" class="form-control" id="usetype_id">
                                    <option value="">--选择--</option>
                                    <% _.each(baseassettype, function(assettype){ %>
                                     <option value=<%= assettype.id %> flag=<%=assettype.flag%> ><%= assettype.name %></option>
                                     <% }) %>
                                </select>
                            </td>
                            <th>服务器分类：</th>
                            <td>
                                <select class="form-control" name="assettype_id" id="assettype_id">
                                    <option value="">--选择--</option>
                                    <% _.each(baseassetsubtype, function(subtype){ %>
                                     <option value=<%= subtype.id %>><%= subtype.name %></option>
                                     <% }) %>
                                </select>
                            </td>
                        </tr>
                         <tr>
                             <th>生产厂商：</th>
                             <td>
                                 <select class="form-control" name="factory_id" id="factory_id">
                                     <option value="">--选择--</option>
                                     <% _.each(basefactory, function(factory){ %>
                                     <option value=<%= factory.id %>><%= factory.name %></option>
                                     <% }) %>
                                 </select>
                             </td>
                             <th>集成商：</th>
                             <td>
                                 <select class="form-control" name="integrator_id" id="integrator_id">
                                     <option value="">--选择--</option>
                                     <% _.each(basefactory, function(factory){ %>
                                     <option value=<%= factory.id %>><%= factory.name %></option>
                                     <% }) %>
                                 </select>
                             </td>
                             <th><span style="color:red">*</span>型号：</th>
                             <td><input type="text" class="form-control" name="model" id="model"/></td>
                         </tr>
                         <tr>
                             <th><span style="color:red">*</span>数据中心：</th>
                             <td>
                                 <select class="form-control" id="datacenter">
                                     <option value="">--选择--</option>
                                     <% _.each(basedatacenter, function(datacenter){ %>
                                     <option value=<%= datacenter.id %>><%= datacenter.name %></option>
                                     <% }) %>
                                 </select>
                             </td>
                             <th><span style="color:red">*</span>所属机房：</th>
                             <td>
                                 <select class="form-control" name="room_id" id="room_id">
                                     <option value="">--选择--</option>
                                     <% _.each(basemachineroom, function(machineroom){ %>
                                     <option value=<%= machineroom.id %>><%= machineroom.name %></option>
                                     <% }) %>
                                 </select>
                             </td>
                             <th>所属机柜：</th>
                             <td><input type="text" class="form-control" name="cabinet" id="cabinet" /></td>
                         </tr>
                         <tr>
                             <th>管理IP：</th>
                             <td><input type="text" class="form-control" name="manageip" id="manageip" /></td>
                             <th>集群信息：</th>
                             <td><input type="text" class="form-control" name="clusterinfo" id="clusterinfo" /></td>
                             <th>单元信息：</th>
                             <td><input type="text" class="form-control" name="unitinfo" id="unitinfo" /> </td>
                         </tr>
                         <tr>

                             <th>CPU(数量)：</th>
                             <td><input type="number" class="form-control" name="cpu" id="cpu" /></td>
                             <th>内存(GB)：</th>
                             <td><input type="number" class="form-control"  name="memory" id="memory"  /></td>
                             <th>硬件负责人：</th>
                             <td><input type="text" class="form-control"  name="contact" id="contact" /></td>
                         </tr>

                         <tr>
                             <th>购买日期：</th>
                             <td>
                                 <div class="input-group date issue-time" data-date="2016-08-31" data-date-format="yyyy-mm-dd" data-link-field="event-start-time">
                                    <input class="form-control" size="16" type="text" value="" name="tradedate" id="tradedate" readonly>
                                    <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                                </div>
                             </td>
                             <th>开始保修期：</th>
                             <td>
                                 <div class="input-group date issue-time" data-date="2016-08-31" data-date-format="yyyy-mm-dd" data-link-field="event-start-time">
                                    <input class="form-control" size="16" type="text" value="" name="startdate" id="startdate" readonly>
                                    <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                                </div>
                             </td>
                             <th>过保日期：</th>
                             <td>
                                 <div class="input-group date issue-time" data-date="2016-08-31" data-date-format="yyyy-mm-dd" data-link-field="event-start-time">
                                    <input class="form-control" size="16" type="text" value="" name="expiredate" id="expiredate" readonly>
                                    <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                                </div>
                             </td>
                         </tr>
                         <tr>
                             <th>服务器状态：</th>
                             <td>
                                 <select class="form-control" name="assetstatus_id" id="status">
                                     <% _.each(baseassetstatus, function(status){ %>
                                     <option value=<%= status.id %> flag=<%= status.flag %> ><%= status.status %></option>
                                     <% }) %>
                                 </select>
                             </td>
                             <th>所属环境：</th>
                             <td>
                                 <select class="form-control" name="netarea_id" id="netarea_id">
                                     <% _.each(basenetarea, function(netarea){ %>
                                     <option value=<%= netarea.id %>><%= netarea.name %></option>
                                     <% }) %>
                                 </select>
                             </td>
                             <th>主机数(台)：</th>
                             <td style="vertical-align:middle;"><span id="asset_host_count" style="font-size: 14px;">0</span></td>
                         </tr>
                         <tr>
                             <th>备注:</th>
                             <td colspan="5">
                                 <div class="row">
                                     <div class="col-sm-4" style="width:285px">
                                         <input type="text" class="form-control" name="remark" id="remark"/>
                                     </div>
                                 </div>
                             </td>
                         </tr>
                         <tr>
                             <td colspan="6">
                                 <div class="col-sm-5"></div>
                                 <div class="col-sm-1">
                                     <input type="button" class="btn btn-primary" value="提交" id="submit-btn"/>
                                 </div>
                                 <div class="col-sm-4">
                                     <h5 id="error-message"></h5>
                                 </div>
                             </td>
                         </tr>
                    </table>
                </form>
            </div>
        </div>
    </div>

</div>
