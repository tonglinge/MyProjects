
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
        <h4>主机管理</h4>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <form role="form" class="form" id="host-form">
                <table class="table table-bordered table-hover dataTable server-table">
                    <tr>
                        <th><span style="color:red">*</span>主机名： </th><td><input type="text" name="hostname" class="form-control" id="hostname"/></td>
                        <th>主机类型：</th>
                        <td>
                            <select class="form-control" name="type_id" id="type_id">
                                <option value="" flag="">--选择--</option>
                                <% _.each(baseassettype, function(assettype){ %>
                                 <option value=<%= assettype.id %> flag=<%=assettype.flag%> ><%= assettype.name %></option>
                                 <% }) %>
                            </select>
                        </td>
                        <th>宿主机：</th>
                        <td>
                            <select class="form-control" name="ownserver_id" id="ownserver_id">
                                <option value="">--选择--</option>
                                <% _.each(ownserver, function(server){ %>
                                 <option value=<%= server.id %>><%= server.server %></option>
                                 <% }) %>
                            </select>
                        </td>
                    </tr>
                     <tr>
                         <th>型号：</th>
                         <td><input type="text" name="model" class="form-control" id="model"/></td>
                         <th>分区：</th>
                         <td>
                            <input name="partition" class="form-control" id="partition" />
                         </td>
                         <th>网络域：</th>
                         <td>
                            <select name="netarea_id" class="form-control" id="netarea_id" >
                                <option value="">--选择--</option>
                                <% _.each(basenetarea, function(netarea){ %>
                                 <option value=<%= netarea.id %>><%= netarea.name %></option>
                                 <% }) %>
                            </select>
                         </td>

                     </tr>
                    <tr>
                         <th>F5策略：</th>
                         <td>
                             <select name="balancetype_id" class="form-control" id="balancetype_id">
                                <option value="">--选择--</option>
                                <% _.each(basebalancetype, function(balancetype){ %>
                                 <option value=<%= balancetype.id %>><%= balancetype.typename %></option>
                                 <% }) %>
                             </select>
                         </td>
                        <th>购买日期：</th>
                         <td>
                             <div class="input-group date issue-time" data-date="2016-08-31" data-date-format="yyyy-mm-dd" data-link-field="event-start-time">
                                <input class="form-control" size="16" type="text" value="" name="tradedate" id="tradedate" readonly>
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
                        <th>运行状态：</th>
                         <td>
                             <select name="runningstatus_id" class="form-control" id="runningstatus_id" >
                                <option value="">--选择--</option>
                                <% _.each(baserunningstatus, function(runningstatus){ %>
                                 <option value=<%= runningstatus.id %>><%= runningstatus.status %></option>
                                 <% }) %>
                             </select>
                         </td>
                     </tr>
                     <tr>
                         <th>所属业务线:</th>
                         <td colspan="5" style="margin-left:10px;">
                             <div class="row">
                                 <div class="col-sm-3" style="width:575px">
                                     <input class="form-control" id="project" placeholder="业务系统关键字..." style="width:230px"/>
                                     <input type="hidden" class="form-control" id="project-id" /><span class="form-control" style="display:none" id="reload-data">reload data</span>
                                 </div>
                                 <div class="col-sm-4">
                                     <button type="button" class="btn btn-primary input-sm" id="add-project"><i class="fa fa-plus"></i>添加业务系统</button>
                                 </div>
                             </div>
                             <div>&nbsp;</div>
                             <div class="row">
                                 <div class="col-sm-4" style="width:260px">
                                     <select multiple="multiple" class="form-control" id="business_set">
                                     </select>
                                 </div>
                                 <div class="col-sm-2" style="padding-top: 12px;width:55px">
                                     <button type="button" id="move-right">=></button>
                                     <button type="button" id="move-left"><=</button>
                                 </div>
                                 <div class="col-sm-4" style="width:260px">
                                     <select multiple="multiple" name="business" class="form-control" id="business_id">
                                     </select>
                                 </div>
                                 <div class="col-sm-4">
                                     <button type="button" class="btn btn-primary input-sm" id="add-business"><i class="fa fa-plus"></i>添加业务线</button>
                                 </div>
                             </div>
                         </td>
                     </tr>

                     <tr>
                         <th>备注:</th>
                         <td colspan="5">
                             <div class="row">
                                 <div class="col-sm-4" style="width:260px">
                                     <input type="text" name="remark" class="form-control" id="remark"/>
                                 </div>
                             </div>
                         </td>
                     </tr>
                     <tr>
                         <td colspan="6">
                             <div class="col-sm-4"></div>
                             <div class="col-sm-4">
                                 <button type="button" class="btn btn-primary submit-btn" id="save-and-add">保存并新增</button>
                                 <button type="button" class="btn btn-primary submit-btn" id="save-and-back">保存并返回</button>
                                 <button type="button" class="btn btn-primary submit-btn" id="save-and-detail">补充详情</button>
                             </div>
                             <div class="col-sm-4">
                                  <span id="error-message" style="color:red"></span>
                             </div>
                         </td>
                     </tr>
                </table>
                </form>
            </div>
        </div>
    </div>

</div>
