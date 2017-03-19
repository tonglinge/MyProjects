/**
 * Created by zengchunyun on 16/8/12.
 */

define(function (require, exports, module) {
    var Backbone = require('backbone');

    var CMDBCollection = Backbone.Collection.extend({
        initialize: function (options) {
            this.page = 1;
            this.canFetch = true;
            this.model = options.model;
            this.parseData = options.parseData;
        },
        parse: function (response) {

            if(response.status == true){
                this.canFetch = response.has_next;
                this.addPage();
                if(response.info && response.info != "") {
                    swal({   title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                }

            }else {
                swal({ title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
            }
            if(typeof response.data != "undefined"){
                console.log("return_data_is:",response.data);
                return response.data;
            }else {
                return response;
            }
        },
        resetCollection: function () {
            this.page = 1;
            this.canFetch = true;
        },
        addPage: function () {
            this.page += 1;
        },
        fetchData: function (reset, form_data, options){
            var async = true;
            var method = "";
            var type = "GET";
            if(options){
                var async = typeof options.async == "undefined" ? async : options.async;
                var method = typeof options.method == "undefined" ? async : options.method;
                var type = typeof options.type == 'undefined' ? type : options.type.toUpperCase();
            }

            if(reset){
                this.resetCollection();
            }else {
                reset = false
            }

            if(this.canFetch || reset){
                this.fetch({
                    data:{data:form_data, method: method},
                    reset: reset,
                    async: async,
                    type: type,
                })
            }else {
                $("#loading").fadeOut("slow");
            }
        }
    });

    return CMDBCollection;

});