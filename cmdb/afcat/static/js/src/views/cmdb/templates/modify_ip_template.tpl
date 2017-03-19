<div class="row">
    <script>
        $("#IPModal").modal({
            show: true
        })
        $("#IPModal").on("hidden.bs.modal", function() {
            $("#IPForm")[0].reset();
            $("#IPForm").val(null);
            $(this).data('bs.modal', null);
        });
    </script>
</div>
<div class="modal fade cmdbModal " id="IPModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content" style="width: 490px;margin-left: 50px;margin-top: 50px;">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               编辑IP
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="IPForm">
                 <div class="form-group">
                     <div class="col-sm-4">
                         <label for="ipaddr" class="control-label">IP地址：</label>
                     </div>
                     <div class="col-sm-7">
                        <input class="form-control" value="<%= ipaddr %>" id="ipaddr" disabled="disabled"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="ipmask">IP地址段：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text"  class="form-control" value="<%= ipmask %>" disabled="disabled"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="status">分配状态：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" class="form-control" value="<%= status %>" disabled="disabled"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="">分配人：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" class="form-control" value="<%= allocateuser %>" disabled="disabled"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="allocateto">分配系统/设备：</label>
                     </div>
                     <div class="col-sm-7">
                         <input class="form-control" name="allocateto" value="<%= allocateto %>" />
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="vlan">VLAN：</label>
                     </div>
                     <div class="col-sm-7">
                         <input class="form-control" name="vlan" value="<%= vlan %>" />
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="remark" class="form-control" id="remark" value="<%= remark %>"/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-4">
                        <label for="id">id：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="id" class="form-control" id="id" value="<%= id %>"/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
             <span id="error-message"></span>
            <button type="button" class="btn btn-default" data-dismiss="modal">关闭 </button>
            <button type="button" class="btn btn-primary" id="btn-modify-ip"> 提交 </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->