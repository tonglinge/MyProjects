/**
 * Created by super on 2016/4/26.
 */

$(function () {
    //点击接收许可复选框
    $("#terms-cond").change(function () {
        if ($(this).prop('checked')){
            $(".btn-success").removeAttr('disabled');
        }else{
            console.log('0');
            $(".btn-success").attr('disabled',true);
        }
    });

    // input框输入时取消错误提示信息
    $(":input").keydown(function () {
        $(this).removeClass('input-error');
        $(".input-err-tip").hide();
    });

    //用户名有效验证
    $("#uname").blur(function () {
        var uname = $(this).val();
        console.log(uname);
        if (uname.length > 0){
            //ajax验证有效性
            $.ajax({
                url:'/regist/checkuser/',
                type:"GET",
                data:{username:uname},
                success:function (data) {
                    var returnvalue = data;
                    console.log(returnvalue);
                    if (returnvalue == "1"){
                        $("#err-uname").text('* 此用户名已经存在!');
                        error_tip_show("uname","username-tip");
                         return false;
                    }
                },
				error:function(errmsg){
                    $("#error-box").text('验证失败!');
					console.log('errmsg:',errmsg);	
				},


            })
        }
    });

    //点击注册验证
    $(".btn-success").click(function () {
        //check user
        if ($("#uname").val().trim().length == 0){
            $("#err-uname").text('* 请输入用户名');
            error_tip_show("uname","username-tip");
            return false
        }/*else{
            //验证用户名是否应注册,此处应该用ajax，没有做服务端就暂时写死了
            if ($("#uname").val() == 'oldboy'){
                $("#err-uname").text('* 此用户名已经存在!');
                error_tip_show("uname","username-tip");
                return false;
            }
        }*/
        //姓名框
        if ($("#fullname").val().trim().length == 0){
            $("#err-fullname").text('* 请输入姓名');
            error_tip_show("fullname","fullname-tip");
            return false
        }
        //email验证
        if ($("#email").val().trim().length == 0){
            $("#reg-email-tip").text('* 请输入邮箱');
            error_tip_show("email","email-tip");
            return false;
        }else{
            var reg=/^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/;
            var v=$("#email").val().trim();
            if (!reg.test(v)){
                $("#reg-email-tip").text('* 邮箱格式不正确!');
                error_tip_show("email","email-tip");
                return false;
            }
        }
        //密码
        if ($("#pwd").val().trim().length == 0){
            $("#err-pwd").text('* 请输入密码');
            error_tip_show("pwd","pwd-tip");
            return false;
        }
        //再次密码
        if ($("#confirm-pwd").val().trim().length == 0){
            $("#err-confirmpwd").text('* 请输入密码');
            error_tip_show("confirm-pwd","confirm-pwd-tip");
            return false;
        }
        //两次密码一致么
        if ($("#pwd").val().trim() != $("#confirm-pwd").val().trim()){
            $("#err-confirmpwd").text('两次密码不一致!');
            error_tip_show("confirm-pwd","confirm-pwd-tip");
            return false;
        }
		//都没有问题那就ajax注册
		console.log('begin reg');
        var postdata={username:$('#uname').val(),
				  fullname:$('#fullname').val(),
				  password:$('#pwd').val(),
				  email:$('#email').val()
             };
        console.log(postdata);
		$.ajax({
			 url:'/regist/',
             type:'POST',
             dataType:'json',
			 data:JSON.stringify(postdata),
             success:function(data) {
                 if (data=="1"){
                     console.log('succ:',data);
                     $("#error-box").text('注册成功,返回登录!');
                     window.location.href = '/login/';
                 }
             },
             error:function(err_msg){
                 console.log('error:',err_msg);
             }

		});
		return false
    });

});

function error_tip_show(inputid,errtid) {
    $('#'+inputid).addClass('input-error');
    $('.'+errtid).show();
}