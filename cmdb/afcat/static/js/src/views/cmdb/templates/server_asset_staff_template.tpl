<div class="row">
    <script>
        $(document).ready(function () {
            $("#addStaffModal").modal({
                show: true
            });
            $("#addStaffModal").on("hidden.bs.modal", function() {
                $("#staffForm")[0].reset();
            });
        })
    </script>
</div>
<div class="modal fade cmdbModal" id="addStaffModal" tabindex="-1" role="dialog"
aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               联系人
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="staffForm">
                 <div class="form-group">
                     <div class="col-sm-2">
                         <label for="name" class="control-label">联系人：</label>
                     </div>
                     <div class="col-sm-8">
                         <select class="form-control" id="staffSelect">
                             <% _.each(staffs, function(staff){ %>
                                <option value="<%= staff.id %>"><%= staff.name %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="mobile">手机：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="mobile" class="form-control" id="mobile" value="<%= staffs[0].mobile %>" readonly/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="telphone">座机：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="telphone" class="form-control" id="telphone" value="<%= staffs[0].tel %>" readonly/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="email">邮箱：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="email" name="telphone" class="form-control" id="email" value="<%= staffs[0].email %>" readonly/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="email">角色：</label>
                     </div>
                     <div class="col-sm-8">
                         <select class="form-control" id="role">
                             <% _.each(baserole, function(role){ %>
                                <option value=<%= role.id %>><%= role.role_name %></option>
                             <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                         <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="remark" class="form-control" id="remark"  value="<%= staffs[0].remark %>"/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-2">
                        <label for="R_server_staff">id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="R_server_staff" class="form-control" id="R_server_staff"/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-2">
                        <label for="staff_id">id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="staff_id" class="form-control" id="staff_id"/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-2">
                        <label for="opration">opration：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="opration" class="form-control" id="opration"/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
            <button type="button" class="btn btn-default"
               data-dismiss="modal">关闭
            </button>
            <button type="button" class="btn btn-primary" id="submitStaff">
               提交
            </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->