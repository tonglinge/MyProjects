<div class="row">
    <script>
        $("#addCardModal").modal({
            show: true
        })
        $("#addCardModal").on("hidden.bs.modal", function() {
            $("#card-form")[0].reset();
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
             <form role="form" class="form-horizontal" id="card-form">
                 <div class="form-group">
                     <div class="col-sm-2">
                         <label for="cardtype" class="control-label">类型：</label>
                     </div>
                     <div class="col-sm-8">
                        <select class="form-control" name="cardtype" id="cardtype">
                            <option value="1">网卡</option>
                            <option value="2">存储卡</option>
                        </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="sn">SN：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="sn" class="form-control" id="sn"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="model">型号：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="input" name="model" class="form-control" id="model"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="mac">MAC/WWN：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="mac" class="form-control" id="mac"/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="factory_id">厂商：</label>
                     </div>
                     <div class="col-sm-8">
                         <select class="form-control" name="factory_id" id="factory_id">
                             <option value="">--选择--</option>
                            <% _.each(basefactory, function(factory){ %>
                                <option value="<%= factory.id %>"><%= factory.name %></option>
                            <% }) %>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-2">
                        <label for="slot">插槽：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="slot" class="form-control" id="slot"/>
                     </div>
                 </div>
                 <div class="form-group" id="portlist">
                     <div class="col-sm-2">
                        <label for="ports">端口：</label>
                     </div>
                     <div class="col-sm-8">
                         <textarea class="form-control" name="ports" id="ports" rows="3" placeholder=""></textarea>
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
            <button type="button" class="btn btn-primary" id="submitServerHostCard">
               提交
            </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->