/**
 * Created by super on 2016/10/27.
 */
define(function (require, exports, module){
    var $ = require("jquery");
    var Backbone = require('backbone');

    var PermUserlistItemView=require("./account_user_item_view").PermUserslistItemView;

    var PermUserlistView = Backbone.View.extend({

        events:{
            "click #btn_show_add": "showAddPage",
            "click #cancel-user-add": "hideAddPage",
            "click #summit-user-add": "createUser",
            "change #upfile": "upFile",
            "blur #user-email": "checkEmail",
            "click .btn-change-passwd": "showResetPassModal",
            "click .btn-change-user": "changeUserInfo",
            "click .btn-delete-user": "deleteUser",
            "click #btn-resetPassword": "resetPassword"
        },

        initialize : function (options) {
            this.model = options.model;
            this.collection.url = options.url;
            this.canFetch = false;
            this.listenTo(this.collection, "reset", this.addAll);
            this.collection.fetchData(true);

        },
        addAll: function () {
            this.$el.find("#perm-user-list-body").children().remove();
            //this.$el.find("#belong-cust").children().remove();
            // 遍历collection的数据,开始逐条渲染
            this.collection.each(this.addOne, this);

        },
        addOne: function (model) {
            // 渲染单条 tr,追加到 tbody
            var usermodel = model.toJSON();
            if (typeof usermodel.username != "undefined" && typeof usermodel.is_superuser != "undefined") {
                var userlistItemView = new PermUserlistItemView({model: usermodel});
                // 先清理掉所有 tbody 的数据,
                this.$el.find("#perm-user-list-body").append(userlistItemView.render().el);
            }else if (typeof usermodel.custalias != "undefined" && typeof  usermodel.idcode != "undefined"){
                // 添加用户权限组的select
                this.fillPermCusts(usermodel);
            }else{
                this.fillPermGroups(usermodel)
            }

        },
        initCreatePage: function () {
            //添加或编辑时都用一个页面,初始化输入框
            $("#user-username").val("");
            $("#user-username").attr("readonly",false);
            $("#user-nickname").val("");
            $("#user-email").val("");
            $("#user-password").val("");
            $("#confirmpassword").val("");
            $("#img-show-head").removeAttr("src");
            $("#create-page-title").text("添加用户");
            $("#summit-user-add").attr("action","add");
            $("#belong-cust").val("");
        },
        showAddPage: function () {
            //添加用户显示添加页面
            this.$el.find("#user-list").hide();
            this.$el.find("#user-add").show("slow");
            //获取所有的权限组信息
            this.loadGroups({"action":"add"});
            this.loadCust({"action":"add"});
        },
        loadGroups: function (options) {
            // 从后台获取所有的权限组数据
            this.$el.find("#user-groups option").first().siblings().remove();
            var original_url = this.collection.url; // 保存原始url
            this.collection.url = "/account/load_groups";
            this.collection.fetchData(true,"", this.checkGroups,options);
            this.collection.url = original_url;
        },
        loadCust: function (options) {
            $("#belong-cust").first().siblings().remove();
            var original_url = this.collection.url;
            this.collection.url = "/account/load_custs";
            this.collection.fetchData(true, "",this.checkCust, options);
            this.collection.url = original_url;
        },
        fillPermGroups: function (model) {
            // 渲染权限组下拉框
            this.$el.find("#user-groups").append("<option value="+model.id+">"+model.name+"</option>");
        },
        fillPermCusts: function (model) {
            console.log(model);
            $("#belong-cust").append("<option value="+model.idcode+">"+model.custalias+"</option>");
            $('#belong-cust').selectpicker('refresh');
	        $('#belong-cust').selectpicker('render');
        },
        hideAddPage: function () {
            this.$el.find("#user-add").hide();
            this.$el.find("#user-list").show();
            this.initCreatePage();
            //重新加载一下用户信息
            this.$el.find("#belong-cust").remove();
            this.$el.find(".bootstrap-select").append("<select class='form-control bootstrap-select' id='belong-cust' multiple></select>")
            this.collection.fetchData(true);
        },
        checkEmail: function () {
            var email = this.$el.find("#user-email").val();
            if (this.mailCheck(email) == false){
                this.$el.find("#user-email").css("border-color", "red");
            }else{
                this.$el.find("#user-email").css("border-color", "#d2d6de");
            }
            // console.log("email invalid");
        },
        upFile: function () {
            // console.log("upfile....");
            var file_data =  new FormData($("#form_sendfile")[0]);
            file_data.append('file', $("#upfile")[0].files[0]);
            var element = this.$el;
            //异步发送文件到后端
            $.ajax({
                url:"/account/upfile/",
                type:'POST',
                data:file_data,
                contentType:false,
                processData:false,
                success:function (filename) {
                    console.log("calback....",filename);
                    element.find("#head-img").attr("img-name", filename);
                    element.find("#img-show-head").attr("src","/static/img/account/"+filename.substr(1,filename.length-2))

                }
            });
        },
        mailCheck: function (string) {
            var check = /^\w+([-.]\w+)*@\w+([-.]\w+)*\.[a-zA-Z]{2,10}$/;
            return check.test(string) ? true : false;
        },
        showErrMsg: function (msg) {
            swal({title: msg,alertType:"error",type:"error", showConfirmButton: false, timer:2000});
        },
        createUser: function (e) {
            var action = $(e.currentTarget).attr("action");
            //添加用户确认按钮事件
            var username = this.$el.find("#user-username").val();
            var nickname = this.$el.find("#user-nickname").val();
            var password = this.$el.find("#user-password").val();
            var confirmpass = this.$el.find("#confirmpassword").val();
            var is_superuser = this.$el.find("#is-superuser").val();
            var user_group = this.$el.find("#user-groups").val();
            // var is_active = this.$el.find(".is-active[checked]").val();
            var is_active = this.$el.find("input[name='inlineRadioOptions']:checked").val();
            var head_img = this.$el.find("#head-img").attr("img-name");
            var email = this.$el.find("#user-email").val();
            var cust_id = $("#belong-cust").val().join(",");
            // 开始验证
            if (username.length == 0){
                this.showErrMsg("请输入用户名!");
                this.$el.find("#user-username").focus();
                return false
            }
            if (nickname.length == 0){
                this.showErrMsg("请输入昵称/姓名!");
                this.$el.find("#user-nickname").focus();
                return false
            }
            if ((password.length < 5 || confirmpass.length < 5) && action =="add"){
                this.showErrMsg("密码长度必须大于5位!");
                return false
            }
            if (password != confirmpass){
                this.showErrMsg("两次输入密码不一致!");
                return false
            }
            if (!this.mailCheck(email)){
                this.showErrMsg("请输入正确的邮箱地址!");
                return false
            }
            if (cust_id == "0" | cust_id == ""){
                this.showErrMsg("请选择至少一个管理客户!");
                return false
            }
            if (user_group == 0){
                this.showErrMsg("选择用户权限组!");
                return false
            }


            // 开始提交数据
            var new_user = new this.model();
            new_user.url = this.collection.url;
            var post_data = {
                "username": username,
                "nickname": nickname,
                "password": password,
                "is_superuser": is_superuser,
                "is_active": is_active,
                "groups": user_group,
                "navatar": head_img ? head_img : "",
                "email" : email,
                "cust_id": cust_id,
                "action": action
            };
            new_user.set("data", post_data);
            new_user.self = this;
            // console.log(post_data);
            new_user.save(new_user.attributes,{success:function () {
                //添加成功后回到主页面，
                new_user.self.hideAddPage();
            }});


        },
        showResetPassModal: function (e) {
            var uid = $(e.currentTarget).attr("uid");
            this.$el.find("#text-resetPassword").val("");
            this.$el.find("#user-password-reset").modal("show");
            this.$el.find("#btn-resetPassword").attr("uid", uid);

        },
        resetPassword: function (e) {
            var new_pass_obj = this.$el.find("#text-resetPassword");
            var new_pass = new_pass_obj.val().trim();
            var change_uid = $(e.currentTarget).attr("uid");
            if (new_pass.length < 5){
                console.log("dss");
                new_pass_obj.css({"border-color":"red"});
                new_pass_obj.attr("placeholder", "密码必须大于5位");
                return false;
            }
            var user_model = new this.model();
            user_model.url = this.collection.url;
            post_data = {"action":"resetpass","id":change_uid,"new_pass": new_pass};
            this.$el.find("#user-password-reset").modal("hide");
            user_model.save({"data": post_data});
            return false;
        },
        changeUserInfo: function (e) {
            // 获取选中的用户的值
            var username = $(e.currentTarget).parent().parent().parent().siblings(".user-name").text().trim();
            var headimg = $(e.currentTarget).parent().parent().parent().siblings().find(".user-headimg").attr("src");
            var nickname = $(e.currentTarget).parent().parent().parent().siblings(".user-nickname").text().trim();
            var email = $(e.currentTarget).parent().parent().parent().siblings(".user-email").text().trim();
            var usertype = $(e.currentTarget).parent().parent().parent().siblings(".user-superuser").text().trim();
            var usergroup = $(e.currentTarget).parent().parent().parent().siblings(".user-groups").text().trim();
            var usercust = $(e.currentTarget).parent().parent().parent().siblings(".user-cust").text().trim();
            var isactive = $(e.currentTarget).parent().parent().parent().siblings(".user-active").text().trim();
            var cust_id = $(e.currentTarget).parent().parent().parent().siblings(".cust-id").text().trim();

            // 将密码框隐藏掉不修改
            this.$el.find("input[type='password']").parent().parent().hide();
            // 调用添加的页面进行编辑
            //添加用户显示添加页面
            this.$el.find("#user-list").hide();
            this.$el.find("#user-add").show("slow");
            this.loadGroups({"action":"change","usergroup":usergroup});
            this.loadCust({"action":"change","cust_id":cust_id});
            // 选中用户类型下拉框
            this.$el.find("#is-superuser").children().each(function (e) {
                // console.log("111", this.text, e);
                if (this.text.trim() == usertype){
                    $(this).attr("selected", true)
                }else{
                    $(this).attr("selected", false)
                }
            });
            //填充编辑框
            $("#user-username").val(username);
            $("#user-nickname").val(nickname);
            $("#user-email").val(email);
            $("input[name='inlineRadioOptions'][data-txt='"+isactive+"']").attr("checked",true);

            var cust_id = cust_id.split(",");
            $("#img-show-head").attr("src",headimg);
            //修改显示页面
            $("#user-username").attr("readonly",true);
            $("#create-page-title").text("编辑用户");
            $("#summit-user-add").attr("action","change");
        },
        checkGroups: function (options) {
            if (options.action == "change") {
                //编辑用户时，当load权限组完成之后再collections中调用此方法来选中用户所属组
                $("#user-groups").children().each(function () {
                    if (this.text.trim() == options.usergroup) {
                        $(this).attr("selected", true)
                    } else {
                        $(this).attr("selected", false)
                    }
                })
            }
        },
        checkCust: function (options) {
            if (options.action == "change") {
                //编辑用户时，当load权限组完成之后再collections中调用此方法来选中用户所属组
                var cust_id = options.cust_id.split(",");
                $("#belong-cust").selectpicker("val", cust_id);
            }

        },
        deleteUser: function (e) {
            var uid = $(e.currentTarget).attr("uid");
            console.log(uid);
            var post_data = {"id":uid, "action":"delete"};
            var new_model = new this.model();
            new_model.url = this.collection.url;

            swal({title:"确定要删除该用户吗?",
                type:"warning",
                showCancelButton:true,
                confirmButtonText: "确认",
                cancelButtonText: "取消",
                closeOnConfirm: false,
                closeOnCancel: true},
            function(isConfirm){
                if (isConfirm) {
                    new_model.save({"data":post_data});
                    $(e.currentTarget).parent().parent().parent().parent().remove();
                }
            });
        }

    });

    return PermUserlistView

});