/**
 * Created by super on 2016/6/14.
 */

//用户登录检测
$("#login_btn").click(function () {
    var username = $("#login-uname").val();
    var userpwd = $("#login-pwd").val();

    if (username.trim().length == 0){
        $("#login-uname").addClass('input-error');
        $(".username-tip").show();
        return false
    }
    if (userpwd.trim().length == 0){
        $("#login-pwd").addClass('input-error');
        $(".pwd-tip").show();
        return false
    }

});


//登录页面，输入框获取焦点后将错误的信息移除
$(":input").keydown(function () {
    $(this).removeClass('input-error');
    $(".input-err-tip").hide();
});

$(document).ready(function () {
    console.log('login ready');
});