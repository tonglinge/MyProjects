<div class="row">
    <script>
        $("#addSoftModal").modal({
            show: true
        })
        $("#addSoftModal").on("hidden.bs.modal", function() {
            $("#staffForm")[0].reset();
        });
    </script>
</div>
<div class="modal fade cmdbModal" id="addSoftModal" tabindex="-1" role="dialog"
aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               安装软件
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="staffForm">
                 <div class="form-group">
                     <div class="col-sm-3">
                         <label for="soft_type" class="control-label">软件分类：</label>
                     </div>
                     <div class="col-sm-8">
                         <select class="form-control" id="soft_type">
                             <% _.each(basesofttype, function(softtype){ %>
                                <option value="<%= softtype.id %>"><%= softtype.name %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="softname">软件名称：</label>
                     </div>
                     <div class="col-sm-8">
                         <select class="form-control" id="softname">
                             <% _.each(basesoft, function(soft){ %>
                                <option name="<%= soft.type_id %>" value="<%= soft.id %>"><%= soft.name %><%= soft.version %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="license">License：</label>
                     </div>
                     <div class="col-sm-8">
                         <select class="form-control" id="license">
                             <% _.each(softlisence, function(license){ %>
                                <option name="<%= license.soft_id %>" value="<%= license.id %>"><%= license.lisence %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="port">服务端口：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="port" class="form-control" id="port" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                         <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="remark" class="form-control" id="remark"  value=""/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-3">
                         <label for="soft_id">soft_id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="soft_id" class="form-control" id="soft_id"  value=""/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-3">
                         <label for="basesoft">id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="basesoft" class="form-control" id="basesoft"  value=""/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
            <button type="button" class="btn btn-default"
               data-dismiss="modal">关闭
            </button>
            <button type="button" class="btn btn-primary" id="submitSoft">
               提交
            </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->