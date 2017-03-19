/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var ImportExcelItemView = require("./cmdb_import_excel_item_view").ImportExcelItemView;
    var CMDBView = Backbone.View.extend({
        events: {
            "click #btn-import-excel": "importExcel",
            "click #btn-download-template": "download",
            "click #btn-download-demo": "download",
            "click #btn-import-error": "goBack"
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.model = options.options.model;
            this.collection.url = options.url;
            this.listenTo(this.collection, 'all', this.render);
            this.render();
        },
        render: function () {
            var view = new ImportExcelItemView();
            $("#import-excel-tabs").append(view.render().el);
        },
        goBack: function (e) {
            $("#import-excel-form").css("display", "");
            $("#import-error").css("display", "none");
        },
        importExcel: function (e) {
            //导入Excel
            var file_data = new FormData();
            var upload_form = $(e.currentTarget).closest("form");
            var template_type = $(upload_form).find("#template_type").val();
            var module = $(upload_form).find("#template_type option:selected").attr('module');
            var excel_file = $("#excel_file")[0].files.item(0);
            file_data.append("data", JSON.stringify({"template_type":template_type,"module":module,"action":"import"}));
            file_data.append("file", excel_file);
            var new_model = new this.model();
            new_model.url = this.collection.url;
            $("#loading").fadeIn();
            new_model.save(null, {data:file_data, contentType:false, processData:false, success:function (model, response) {
                $("#loading").fadeOut();
                swal({title: "",
                    text: response.info,
                    type: "warning",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    closeOnConfirm: true}
                );
                if(!response.status){
                    $("#import-error-body").empty();
                    if(response.data.length>0){
                        for(var index in response.data){
                            var innerhtml = "<tr>\
                                <td>"+ response.data[index].row + "</td>" +
                                "<td>" + response.data[index].errmsg + "</td></tr>";
                            $("#import-error-body").append(innerhtml)
                        }
                    }
                    $("#import-excel-form").css("display", "none");
                    $("#import-error").css("display", "");
                }
            }, error:function () {
               $("#loading").fadeOut();
            }, sync:false})
        },
        download: function (e) {
            //下载模板或样例文件
            var download_form = $(e.currentTarget).closest("form").get(0);
            $(download_form).submit();
        },
    });

    return CMDBView;
})
