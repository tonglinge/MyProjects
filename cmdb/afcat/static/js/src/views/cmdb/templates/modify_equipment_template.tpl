

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
        <h5>网络设备</h5>
    </div>
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table class="table table-bordered table-hover dataTable server-table">
                     <tr>
                         <th><span style="color:red">*</span>设备名称：</th>
                         <td><input type="text" class="form-control must-input" id="assetname"/></td>
                         <th>应用用途:</th>
                         <td><input type="text" class="form-control" id="usetype" placeholder=""></td>
                         <th><span style="color:red">*</span>类型：</th>
                         <td>
                             <select class="form-control" id="equipmenttype">
                                 <% _.each(baseequipmenttype, function(equipmenttype){ %>
                                 <option value=<%= equipmenttype.id %>><%= equipmenttype.name %></option>
                                 <% }) %>
                             </select>
                         </td>

                     </tr>
                     <tr>
                         <th>数据中心：</th>
                         <td>
                             <select class="form-control" id="datacenter">
                                 <% _.each(basedatacenter, function(datacenter){ %>
                                 <option value=<%= datacenter.id %>><%= datacenter.name %></option>
                                 <% }) %>
                             </select>
                         </td>
                         <th><span style="color:red">*</span>所属机房：</th>
                         <td>
                             <select class="form-control" id="machineroom">
                                 <% _.each(basemachineroom, function(room){ %>
                                 <option value=<%= room.id %>><%= room.name %></option>
                                 <% }) %>
                             </select>
                         </td>
                         <th><span style="color:red">*</span>机柜：</th>
                         <td>
                             <input type="text" class="form-control" id="cabinet">
                         </td>
                     </tr>
                     <tr>
                         <th>设备管理IP:</th>
                         <td>
                              <div class="input-group">
                              <div class="input-group-addon">
                                <i class="fa fa-laptop"></i>
                              </div>
                              <input type="text" class="form-control" id="manageip" data-inputmask="'alias': 'ip'" data-mask>
                            </div>
                         </td>
                         <th><span style="color:red">*</span>柜内位置：</th>
                         <td>
                             <input type="text" class="form-control must-input" id="slotindex"/>
                         </td>
                         <th><span style="color:red">*</span>设备型号：</th>
                         <td><input type="text" class="form-control must-input" id="model"/></td>
                     </tr>

                     <tr>
                         <th>序列号：</th>
                         <td><input type="text" class="form-control" id="sn" placeholder="SN"/></td>
                         <th>电源数量:</th>
                         <td>
                              <input type="text" class="form-control" id="powertype" placeholder="单电、双电">
                         </td>

                         <th>设备状态:</th>
                         <td colspan="5">
                             <select class="form-control" id="asset_status">
                                 <% _.each(baseassetstatus, function(status){ %>
                                 <option flag="<%= status.flag %>" value=<%= status.id %>><%= status.status %></option>
                                 <% }) %>
                             </select>
                         </td>


                     </tr>
                     <tr>
                         <th><span style="color:red">*</span>网络区域：</th>
                         <td>
                             <select class="form-control" id="netarea">
                                 <% _.each(basenetarea, function(netarea){ %>
                                 <option value=<%= netarea.id %>><%= netarea.name %></option>
                                 <% }) %>
                             </select>
                         </td>
                         <th>服务开始日期：</th>
                         <td><div class="input-group date issue-time" data-date="2016-08-31" data-date-format="yyyy-mm-dd" data-link-field="event-start-time">
                                <input class="form-control" size="16" type="text" value="" name="issue-time" id="tradedate" readonly>
                                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                            </div>
                         </td>
                         <th>过保日期：</th>
                         <td>
                             <div class="input-group date issue-time" data-date="2016-08-31" data-date-format="yyyy-mm-dd" data-link-field="event-start-time">
                                <input class="form-control" size="16" type="text" value="" name="issue-time" id="expiredate" readonly>
                                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                            </div>
                         </td>
                     </tr>

                     <tr>
                        <th>厂商：</th>
                        <td>
                            <select class="form-control" id="factory">
                                 <option value="">--选择--</option>
                                 <% _.each(basefactory, function(factory){ %>
                                 <option value=<%= factory.id %>><%= factory.name %></option>
                                 <% }) %>
                            </select>
                        </td>

                        <th>供应商：</th>
                        <td>
                            <select class="form-control" id="provider">
                                 <option value="">--选择--</option>
                                 <% _.each(basefactory, function(factory){ %>
                                 <option value=<%= factory.id %>><%= factory.name %></option>
                                 <% }) %>
                            </select>
                        </td>

                        <th>服务提供商：</th>
                        <td>
                            <select class="form-control" id="serviceprovider">
                                 <option value="">--选择--</option>
                                 <% _.each(basefactory, function(factory){ %>
                                 <option value=<%= factory.id %>><%= factory.name %></option>
                                 <% }) %>
                            </select>
                        </td>
                     </tr>
                    <% remain = extend.length%3 %>
                    <% rows = Math.ceil(extend.length/3) %>
                    <% for(var i=0;i<(rows);i++){ %>
                        <tr>
                            <% if(i<(rows-1)){ %>
                                <% for(var j=0;j<3;j++){ %>
                                    <th><%= extend[i*3+j].label %>：</th>
                                    <td><input class="form-control customer" size="16" type="input" name="<%= extend[i*3+j].to_field %>" value="<%= extend[i*3+j].value %>" /> </td>
                                <% } %>
                            <% }else{ %>
                                <% for(var j=0;j<(remain);j++){ %>
                                    <th><%= extend[i*3+j].label %>：</th>
                                    <td><input class="form-control customer" size="16" type="input" name="<%= extend[i*3+j].to_field %>" value="<%= extend[i*3+j].value %>" /></td>
                                <% } %>
                            <% } %>
                        </tr>
                    <% } %>


                    <tr>
                         <th>备注:</th>
                         <td colspan="5">
                             <input type="text" class="form-control" id="remark" style="width:340px"/>
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
                                 <span id="error-message"></span>
                             </div>
                         </td>
                     </tr>
                </table>
            </div>
        </div>
    </div>

</div>
