<div class="row">
    <script>
        $("#IPConfigModal").modal({
            show: true
        })
        $("#IPConfigModal").on("hidden.bs.modal", function() {
            $("#modify-subnet-form")[0].reset();
            $("#modify-subnet-form").val(null);
            $(this).data('bs.modal', null);
        });
    </script>
</div>
<div class="modal fade cmdbModal " id="IPConfigModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content" style="width: 490px;margin-left: 50px;margin-top: 50px;">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               编辑子网
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="modify-subnet-form">
                 <div class="form-group">
                     <div class="col-sm-4">
                         <label for="ipaddr" class="control-label">IP地址：</label>
                     </div>
                     <div class="col-sm-7">
                        <input class="form-control" name="ipaddr" id="ipaddr" value="<%= ipaddr %>"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="counts">子网总数：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="counts" class="form-control" id="counts" value="<%= counts %>"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-4">
                        <label for="allocated-count">已分配子网：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" class="form-control" id="allocated-count" value="<%= allocatecount %>" disabled="disabled"/>
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
                         <input class="form-control" name="usefor" value="<%= usefor %>" />
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
                         <input type="button" name="restore" value="Restore Defaults">
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
             <span id="error-message"></span>
            <button type="button" class="btn btn-default" data-dismiss="modal">关闭 </button>
            <button type="button" class="btn btn-primary" id="btn-modify-subnet"> 提交 </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->