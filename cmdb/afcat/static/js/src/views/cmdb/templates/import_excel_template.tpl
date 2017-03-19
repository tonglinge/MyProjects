


<ul class="nav nav-tabs">
    <li class="active"><a href="#tab_0" data-toggle="tab" aria-expanded="true">导入</a></li>
    <li class=""><a href="#tab_1" data-toggle="tab" aria-expanded="false">模板下载</a></li>
    <li class=""><a href="#tab_2" data-toggle="tab" aria-expanded="false">样例下载</a></li>

</ul>
<div class="tab-content" id="import-excel-content">
    <div class="tab-pane active" id="tab_0">

        <form role="form" id="import-excel-form" enctype="multipart/form-data">
            <div class="form-group">
                <label for="template_type">选择导入分类:</label>
                <select name="template_type" class="form-control" id="template_type">
                    <option value="assets" module="assets">服务器设备</option>
                    <option value="equipment" module="equipment">网络设备</option>
                    <option value="server" module="server">主机设备</option>
                </select>
            </div>
            <div class="form-group">
                <label for="excel_file">选择文件:</label>
                <input type="file" name="excel_file" class="form-control"  id="excel_file" />
            </div>
            <div class="form-group">
                <input type="button" class="btn btn-primary" id="btn-import-excel"  value="导入"/>
            </div>
        </form>
        <div id="import-error" style="display:none;  overflow: auto;">
            <table class="table table-condensed table-hover" id="import-error-table">
                <thead>
                    <th>报错行号</th><th>报错信息</th>
                </thead>
                <tbody id="import-error-body" style="height:500px;width:650px;overflow: auto;display:block">

                </tbody>
            </table>
            <button class="btn btn-primary" id="btn-import-error">确定</button>
        </div>
    </div>
    <div class="tab-pane" id="tab_1">
        <form role="form" action="/cmdb/downtemplate/" id="download-template-form">
            <div class="form-group">
                <label for="template_type">选择设备分类:</label>
                <select name="template_type" class="form-control">
                    <option value="assets" module="assets">服务器设备</option>
                    <option value="equipment" module="equipment">网络设备</option>
                    <option value="server" module="server">主机设备</option>
                </select>
            </div>
            <div class="form-group">
                <input type="hidden" class="form-control" name="file_type" value="1" hidden/>
            </div>
            <div class="form-group">
                <label for="btn-download"></label>
                <input type="button" name="btn-download" class="btn btn-primary" id="btn-download-template" value="下载" />
            </div>
        </form>
    </div>
    <!-- /.tab-pane -->

    <div class="tab-pane" id="tab_2">
        <form role="form" action="/cmdb/downtemplate/" id="download-demo-form">
            <div class="form-group">
                <label for="template_type">选择设备分类:</label>
                <select name="template_type" class="form-control">
                    <option value="assets" module="assets">服务器设备</option>
                    <option value="equipment" module="equipment">网络设备</option>
                    <option value="server" module="server">主机设备</option>
                </select>
            </div>
            <div class="form-group">
                <input type="hidden" class="form-control" name="file_type" value="0" hidden/>
            </div>
            <div class="form-group">
                <label for="btn-download"></label>
                <input type="button" name="btn-download" class="btn btn-primary" id="btn-download-demo" value="下载"/>
            </div>
        </form>
    </div>
    <!-- /.tab-pane -->

</div>