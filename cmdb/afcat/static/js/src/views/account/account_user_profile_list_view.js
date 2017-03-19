/**
 * Created by zengchunyun on 2016/12/5.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    //var UserProfileItemView = require("./account_user_profile_item_view").UserProfileItemView;


    var UserProfileView = Backbone.View.extend({
        events: {
            "click #summit-modifypass": "modifypass"
        },
        initialize: function (options) {
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
        },
        addAll: function () {
            var models = this.collection.models;
            //针对每次reload数据时需要清空整个app页面数据，指定判断关键属性，用来决定是否对app内容清空
            if(this.collection.reseted && models.length > 0 && models[0].has("hosts_status")){
                this.$el.find('.hosts_tbody').html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new UserProfileItemView({model: model});
            this.$el.find(".hosts_tbody").append(view.render().el);
        },
        modifypass: function () {
            var form = {};
            var formdata = $("#frm-modifypass").serializeArray();
            if(formdata[0].value.length < 5){
                $("#err-passwd").text("密码长度需大于5位");
                $("#password").focus();
                return false;
            }else{
                $("#err-passwd").text("");
            }
            if(formdata[0].value != formdata[1].value){
                $("#err-confirmpasswd").text("两次输入的密码不一致");
                $("#confirmpassword").focus();
                return false;
            }else{
                $("#err-confirmpasswd").text("");
            }
            for(var index in formdata){
                var field_data = formdata[index];
                form[field_data.name] = field_data.value;
            }
            form["method"] = "account.change.password";
            this.collection.fetchData(false,form,{type:"POST"})
        }
    });
    return UserProfileView;

});