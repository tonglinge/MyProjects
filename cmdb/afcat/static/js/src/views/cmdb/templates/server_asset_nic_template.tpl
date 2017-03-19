<div class="row">
    <script>
        $("#addNICModal").modal({
            show: true
        })
        $("#addNICModal").on("hidden.bs.modal", function() {
            $("#nicForm")[0].reset();
        });
    </script>
</div>
<div class="modal fade cmdbModal" id="addNICModal" tabindex="-1" role="dialog"
aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               网卡信息
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="nicForm">
                 <div class="form-group">
                     <div class="col-sm-2">
                         <label for="factory" class="control-label">厂商：</label>
                     </div>
                     <div class="col-sm-8">
                        <select class="form-control" id="factory">
                            <% _.each(basefactory, function(factory){ %>
                                <option value="<%= factory.id %>"><%= factory.name %></option>
                            <% }) %>
                        </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="model">型号：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="model" class="form-control" id="model" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="sn">设备编号：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="sn" class="form-control" id="sn" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="mac">MAC地址：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="mac" class="form-control" id="mac" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="slotindex">插槽：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="slotindex" class="form-control" id="slotindex" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="remark" class="form-control" id="remark" value=""/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-2">
                        <label for="nic_id">nic_id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="nic_id" class="form-control" id="nic_id" value=""/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
            <button type="button" class="btn btn-default"
               data-dismiss="modal">关闭
            </button>
            <button type="button" class="btn btn-primary" id="submitNic">
               提交
            </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->