<div class="row">
    <script>
        $("#addIPModal").modal({
            show: true
        })
        $("#addIPModal").on("hidden.bs.modal", function() {
            $("#ipForm")[0].reset();
        });
    </script>
</div>
<div class="modal fade cmdbModal" id="addIPModal" tabindex="-1" role="dialog"
aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog">
      <div class="modal-content" style="width: 490px;margin-left: 50px;margin-top: 50px;">
         <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
               aria-hidden="true">×
            </button>
            <h4 class="modal-title" id="myModalLabel">
               IP信息
            </h4>
         </div>
         <div class="modal-body">
             <form role="form" class="form-horizontal" id="ipForm">
                 <div class="form-group">
                     <div class="col-sm-3">
                         <label for="ipaddress" class="control-label">IP地址：</label>
                     </div>
                     <div class="col-sm-7">
                        <input class="form-control pull-left" type="text" id="ipaddress"/>
                     </div>
                    <span id="err-ipaddr" style="color:red; float: left;">*</span>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="gateway">网关地址：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="input" name="gateway" class="form-control" id="gateway" value=""/>
                     </div>
                     <span id="err-gatway" style="color:red; float: left;">*</span>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="iptype">IP类型：</label>
                     </div>
                     <div class="col-sm-7">
                         <select class="form-control" id="iptype">
                             <option value="服务IP">服务IP</option>
                             <option value="物理IP">物理IP</option>
                         </select>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="domain">域名：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="text" name="domain" class="form-control" id="domain" value=""/>
                     </div>
                 </div>
                 <div class="form-group">
                     <div class="col-sm-3">
                        <label for="vlan">vlan编号：</label>
                     </div>
                     <div class="col-sm-7">
                         <input type="number" name="vlan" class="form-control" id="vlan" min="0" max="1000" value=""/>
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
                     <div class="col-sm-2">
                        <label for="ip_id">ip_id：</label>
                     </div>
                     <div class="col-sm-8">
                         <input type="text" name="ip_id" class="form-control" id="ip_id" value=""/>
                     </div>
                 </div>
             </form>
         </div>
         <div class="modal-footer">
            <button type="button" class="btn btn-default"
               data-dismiss="modal">关闭
            </button>
            <button type="button" class="btn btn-primary" id="submitIP">
               提交
            </button>
         </div>
      </div><!-- /.modal-content -->
   </div><!-- /.modal-dialog -->
</div><!-- /.modal -->