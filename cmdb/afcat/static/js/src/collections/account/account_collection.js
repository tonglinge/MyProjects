/**
 * Created by super on 2016/10/21.
 */

define(function (require, exports, module) {
    var Backbone = require('backbone');

    var AccountCollection = Backbone.Collection.extend({
        initialize: function (options) {
            this.page = 1;
            this.canFetch = true;
            this.group_id = 0;
            this.model = options.model;
            //this.parseData = options.parseData;
        },

        parse: function (response) {
            if(response.status == true){
                this.canFetch = response.has_next;
                this.addPage();
                if(response.info && response.info != "") {
                    swal({ title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                }

            }else {
                swal({ title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
            }
            $("#loading").fadeOut("slow");
            if(typeof response.data != "undefined"){
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
        fetchData: function (reset, form_data, self,method) {
             if(reset){
                this.resetCollection();
            }else {
                reset = false
            }
            if(this.canFetch || reset){
                if(self){
                    var args = "";
                    var func = function () {};
                    if(typeof self == "function"){
                        func = self;
                        args = method;
                    }else if(typeof self == "object"){
                        for(var attr in self){
                            if(self[attr] == method){
                                func = typeof self[attr] == "function" ? self[attr]: func;
                                args = self;
                                break;
                            }
                        }
                    }
                    this.fetch({data: {page: this.page, data: form_data, type: this.monitor_type}, reset: true,
                        success: function (collection, response, options) {
                            func(args, collection, response, options)
                        },
                        error:function (xhr, textStatus, errorThrown) {
                            $("#loading").fadeOut("slow");
                            swal({   title: "内部请求错误！", type: 'error',   timer: 5500,   showConfirmButton: true });
                        },
                        beforeSend:function (callbackContext, jqXHR) {
                            $("#loading").show();
                        }
                    });
                }else {
                    this.fetch({data: {page: this.page, data: form_data, type: this.monitor_type},
                                reset: true,
                        success: function (collection, response, options) {

                        },
                        error: function (xhr, textStatus, errorThrown) {
                            $("#loading").fadeOut("slow");
                            swal({   title: "内部请求错误！", type: 'error',   timer: 5500,   showConfirmButton: true });
                        },
                        beforeSend:function (callbackContext, jqXHR) {
                            $("#loading").show();
                        }});
                }
            }else {
                // alert('到底了')
            }
        }
    });

    return AccountCollection;

});