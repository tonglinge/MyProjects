<div class="row">
    <script>
        $("#addCPUModal").modal({
            show: true
        })
        $("#addCPUModal").on("hidden.bs.modal", function() {
            $("#cpuForm")[0].reset();
        });
    </script>
</div>
<div class="modal fade cmdbModal " id="addCPUModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content" style="width: 490px;margin-left: 50px;margin-top: 50px;">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               CPU、内存信息
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="cpuForm">
                 <div class="form-group">
                     <div class="col-sm-3">
                         <label for="model" class="control-label">CPU型号：</label>
                     </div>
                     <div class="col-sm-7">
                        <input class="form-control" id="model"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="cpucount">CPU数量(C)：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="cpucount" class="form-control" id="cpucount" value=""/>
                     </div>
                     <span id="err-cpucount" style="color: red;">*</span>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="corecount">CPU核数：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="corecount" class="form-control" id="corecount" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="frequency">主频(GHZ)：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="frequency" class="form-control" id="frequency" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="memory">内存容量(G)：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="memory" class="form-control" id="memory" value=""/>
                     </div>
                     <span id="err-memory" style="color: red;">*</span>
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
                     <div class="col-sm-2">
                        <label for="cpu_id">id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="cpu_id" class="form-control" id="cpu_id" value=""/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">关闭 </button>
            <button type="button" class="btn btn-primary" id="submitCPU"> 提交 </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->