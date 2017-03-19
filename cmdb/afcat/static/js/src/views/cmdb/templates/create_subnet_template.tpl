<div class="row">
    <script>
        $("#partitionSubnetModal").modal({
            show: true
        })
        $("#partitionSubnetModal").on("hidden.bs.modal", function() {
            $("#createSubnetForm")[0].reset();
            $("#createSubnetForm").val(null);
            $(this).data('bs.modal', null);
        });
    </script>
</div>
<div class="modal fade cmdbModal " id="partitionSubnetModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content" style="width: 490px;margin-left: 50px;margin-top: 50px;">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
                新建网络
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="createSubnetForm">
                 <div class="form-group">
                     <div class="col-sm-4">
                         <label for="ipaddr" class="control-label">网络地址：</label>
                     </div>
                     <div class="col-sm-7">
                        <input class="form-control" name="ipaddr" id="ipaddr" placeholder="192.168.0.0/16"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="counts">子网总数：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="counts" class="form-control" id="counts" min="0" max="256"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="datacenter">数据中心：</label>
                     </div>
                     <div class="col-sm-7">
                         <select class="form-control" name="datacenter_id" id="datacente">
                             <% _.each(basedatacenter, function(datacenter){ %>
                                <option value="<%= datacenter.id %>"><%= datacenter.name %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="netarea">网络区域：</label>
                     </div>
                     <div class="col-sm-7">
                         <select class="form-control" name="netarea_id" id="netarea">
                             <option value="">---请选择---</option>
                             <% _.each(basenetarea, function(netarea){ %>
                                <option value="<%= netarea.id %>"><%= netarea.name %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="usefor">用途：</label>
                     </div>
                     <div class="col-sm-7">
                         <input class="form-control" name="usefor" />
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="vlan">VLAN：</label>
                     </div>
                     <div class="col-sm-7">
                         <input class="form-control" name="vlan"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="remark" class="form-control" id="remark" />
                     </div>
                 </div>

             </form>
         </div>
         <div class="modal-footer">
             <span id="error-message"></span>
            <button type="button" class="btn btn-default" data-dismiss="modal">关闭 </button>
            <button type="button" class="btn btn-primary" id="create-subnet-submit"> 提交 </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->