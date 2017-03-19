<div class="row">
    <script>
        $("#allocateIPModal").modal({
            show: true
        })
        $("#allocateIPModal").on("hidden.bs.modal", function() {
            $("#allocateIPForm")[0].reset();
            $("#allocateIPForm").val(null);
            $(this).data('bs.modal', null);
        });
    </script>
</div>
<div class="modal fade cmdbModal " id="allocateIPModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content" style="width: 490px;margin-left: 50px;margin-top: 50px;">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
                分配IP
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="allocateIPForm">
                 <div class="form-group">
                     <div class="col-sm-4">
                         <label for="ipaddr" class="control-label">IP地址段：</label>
                     </div>
                     <div class="col-sm-7">
                        <input class="form-control"  id="ipaddr" value="<%= ipaddr %>" disabled="disabled"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="startip">起始IP：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="startip" id="startip" class="form-control" />
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="endip">结束IP：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="endip" id="endip" class="form-control"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="allocateto">分配系统/设备：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="allocateto" class="form-control"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="status">状态：</label>
                     </div>
                     <div class="col-sm-7">
                         <select class="form-control" name="status">
                             <% _.each(status, function(status, index){ %>
                                <option value="<%= index %>"><%= status %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="vlan">VLAN：</label>
                     </div>
                     <div class="col-sm-7">
                         <input class="form-control" name="vlan" />
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="remark" class="form-control"/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-4">
                        <label for="ipmask_id"></label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="ipmask_id" class="form-control" value="<%= id %>"/>
                     </div>
                 </div>

             </form>
         </div>
         <div class="modal-footer">
             <span id="error-message"></span>
            <button type="button" class="btn btn-default" data-dismiss="modal">关闭 </button>
            <button type="button" class="btn btn-primary" id="btn-allocate-ip"> 提交 </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->