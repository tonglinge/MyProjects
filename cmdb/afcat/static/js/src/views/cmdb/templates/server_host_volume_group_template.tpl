<div class="row">
    <script>
        $("#addVGModal").modal({
            show: true
        })
        $("#addVGModal").on("hidden.bs.modal", function() {
            $("#volume-group-form")[0].reset();
        });
    </script>
</div>
<div class="modal fade cardModal" id="addVGModal" tabindex="-1" role="dialog"
aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               VG
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="volume-group-form">
                 <div class="form-group">
                     <div class="col-sm-3">
                         <label for="vgname" class="control-label">VG/Pool名称：</label>
                     </div>
                     <div class="col-sm-7">
                        <input class="form-control" name="vgname" id="vgname"/>
                     </div>
                     <span style="color:red" id="err-vgname">*</span>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="vgsize">大小(GB)：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="vgsize" class="form-control" id="vgsize"/>
                     </div>
                     <span style="color:red" id="err-vgsize">*</span>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="raidtype_id">RAID类型：</label>
                     </div>
                     <div class="col-sm-7">
                         <select class="form-control" name="raidtype_id" id="raidtype_id">
                            <% _.each(baseraidtype, function(raidtype){ %>
                                <option value="<%= raidtype.id %>"><%= raidtype.typename %></option>
                            <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="remark" class="form-control" id="remark" value=""/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-3">
                        <label for="id">id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="id" class="form-control" id="id"/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
            <button type="button" class="btn btn-default"
               data-dismiss="modal">关闭
            </button>
            <button type="button" class="btn btn-primary" id="submit-volume-group">
               提交
            </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->