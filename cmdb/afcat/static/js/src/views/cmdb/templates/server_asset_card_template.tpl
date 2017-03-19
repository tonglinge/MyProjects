<div class="row">
    <script>
        $("#addCardModal").modal({
            show: true
        })
        $("#addCardModal").on("hidden.bs.modal", function() {
            $("#cardForm")[0].reset();
        });
    </script>
</div>
<div class="modal fade cardModal" id="addCardModal" tabindex="-1" role="dialog"
aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               板卡
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="cardForm">
                 <div class="form-group">
                     <div class="col-sm-3">
                         <label for="cardname" class="control-label">板卡名称：</label>
                     </div>
                     <div class="col-sm-8">
                        <input class="form-control" id="cardname"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="sn">设备编号：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="sn" class="form-control" id="sn" value="" placeholder="SN"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="slot">槽位：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="slot" class="form-control" id="slot" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="model">型号：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="model" class="form-control" id="model" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="ports">端口号：</label>
                     </div>
                     <div class="col-sm-8">
                         <textarea class="form-control" id="ports" rows="3" placeholder="每一行一个端口号"></textarea>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="remark">备注：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="remark" class="form-control" id="remark" value=""/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-3">
                        <label for="card_id">id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="card_id" class="form-control" id="card_id" value=""/>
                     </div>
                 </div>
                 <div class="form-group" style="display:none">
                     <div class="col-sm-3">
                        <label for="opration">opration：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="opration" class="form-control" id="opration"/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" id="submitCard">提交</button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->