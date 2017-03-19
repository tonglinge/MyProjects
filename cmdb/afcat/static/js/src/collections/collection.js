/**
 * Created by zengchunyun on 16/8/12.
 */

define(function (require, exports, module) {
    var Backbone = require('backbone');
    var $ = require("jquery");

    $.getCookie = function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookie = document.cookie.split(';');
            for (var i = 0; i < cookie.length; i++) {
                var cookie = $.trim(cookie[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    $.safeMethod = function (method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    return Backbone.Collection.extend({
        initialize: function (options) {
            //默认分页数据从第一页开始
            this.page = 1;
            //默认重置状态为true
            this.reseted = true;
            //是否有下一页
            this.has_next = true;
            //是否有上一页
            this.has_previous = false;
            //设置每页默认返回数据条数
            this.per_records = 20;
            this.model = options.model;
            this.update_page = true;
        },
        parse: function (response) {
            if (response.status == true) {
                //判断是否还有数据可以取回
                if(this.update_page){
                    this.has_next = response.has_next;
                    this.has_previous = response.has_previous;
                    if (this.has_next) {
                        this.addPage();
                    }
                }
            }
            if (response.info && response.info != "") {
                setTimeout(function () {
                    swal({title: response.info, type: response.category, timer: 1500, showConfirmButton: false});
                }, 500)
            }
            $("#loading").fadeOut("slow");
            return typeof response.data != "undefined" ? response.data : response;
        },
        resetCollection: function () {
            this.page = 1;
            this.reseted = true;
            this.has_next = true;
            this.has_previous = false;
        },
        addPage: function () {
            this.page += 1;
        },
        currentPage: function () {
            // 发送请求前执行， 重新获取当前数据时调用
            if(this.has_next){
                this.page -= 1;
            }
        },
        previousPage: function () {
            // 发送请求前执行，返回上一页
            if(this.has_previous){
                this.page -= 1;
                if(this.has_next){
                    this.page -= 1;
                }
            }
        },
        fetchData: function (reset, form_data, options) {
            if (reset) {
                this.resetCollection();
            } else {
                this.reseted = false;
            }
            /*
             * @reset: true or false  可选参数，
             * @form_data: {username: 'zengchunyun', password: 'password'}  可选参数
             * @options: {success: function, args: ['2016', '11', '21'], type: 'POST'} 可选参数
             */
            var type = 'GET';  //请求方法
            var url = this.url;
            var async = true;  //是否异步请求
            var callback = function () {};  //请求成功后执行的方法
            var errorCallback = function () {return true};  //请求失败后执行的方法
            var args = "";  //无论请求成功失败，该参数作为第一个值传人到callback或errorCallback方法
            var processData = true;
            var contentType = "application/x-www-form-urlencoded; charset=UTF-8";
            var dataType = "json";
            var requestData = {page: this.page, per_records: this.per_records};  //额外的请求参数，通过append选项false取消添加该请求参数
            if (typeof options == "object") {
                type = typeof options.type == 'undefined' ? type : options.type.toUpperCase();
                url = typeof options.url == 'undefined' ? url : options.url;
                async = typeof options.async == 'undefined' ? async : options.async;
                callback = typeof options.success == "function" ? options.success : callback;
                errorCallback = typeof options.error == "function" ? options.error : errorCallback;
                args = typeof options.args == 'undefined' ? args : options.args;
                processData = typeof options.processData == 'undefined' ? processData : options.processData;
                contentType = typeof options.contentType == 'undefined' ? contentType : options.contentType;
                dataType = typeof options.dataType == 'undefined' ? dataType : options.dataType;
                this.update_page = typeof options.update_page == 'undefined' ? true : options.update_page;
                requestData = typeof options.append != 'undefined' && options.append == false ? {} : requestData;
            }
            for (var key in form_data) {
                requestData[key] = form_data[key];
            }
            console.log("request-data:", requestData);
            if (this.has_next || reset || !this.reseted) {
                this.fetch({
                    async: async,
                    url: url,
                    contentType: contentType,
                    dataType: dataType,
                    data: requestData,
                    reset: this.reseted,
                    type: type,
                    processData: processData,
                    success: function (collection, response, options) {
                        callback(args, collection, response, options);
                    },
                    error: function (xhr, textStatus, errorThrown) {
                        $("#loading").fadeOut("slow");
                        var status = errorCallback(args, xhr, textStatus, errorThrown); //返回结果如果为真，将会弹出错误提示信息，默认弹出提示
                        if(textStatus.status != 200 || status == true){
                            swal({title: "内部请求错误！", type: 'error', timer: 5500, showConfirmButton: true});
                        }
                    },
                    beforeSend: function (callbackContext, jqXHR) {
                        $("#loading").show();
                        var token = $.getCookie('csrftoken');
                        if (!$.safeMethod(jqXHR.type) && !this.crossDomain) {
                            callbackContext.setRequestHeader("X-CSRFToken", token);
                        }
                    }
                });
            } else {
                $("#loading").fadeOut("slow");
            }
        }
    });
});