/**
 * Created by super on 2016/6/11.
 */

//页面临时聊天记录保存列表
var MESSAGE_DB = [];

//ajax 跨站请求伪造CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

// end ajax CSRF



//保存选中用户或群组时，聊天框上面保存选中的对象，或保存上一个聊天对象的记录
function saveSelectedInfo(select_type,select_id, select_img,select_name) {
    var choose_user_id = select_id;
    var choose_user_name = select_name;
    var choose_user_img = select_img;
    //获取当前聊天的状态
    var chat_stat = $("#talkwith").attr("is_select");

    if (chat_stat == "false"){
        //如果当前没有和任何人聊天,则开始一个新的聊天,保存当前聊天人的信息
        $("#talkwith").attr({select_user:select_type +'_' + choose_user_id,
                            is_select:'true',
                            user_img:choose_user_img,
                            fname:choose_user_name
        });
        //清空当前聊天框记录
        $("#chat-content").html("")
    }else{
        //保存上次聊天对象用户名
        var last_chat_user = $("#talkwith").attr("select_user");

        //当前已经有正在聊天的朋友,点击了一个新的，要切换聊天对象，设置当前的对象信息
        $("#talkwith").attr({select_user:select_type + '_' + choose_user_id,
                            is_select:'true',
                            user_img:choose_user_img,
                            fname:choose_user_name
        });
        // 开始保存上一个聊天对象的聊天记录

        // 1 保存下来获取聊天内容
        var curr_chat_content = $("#chat-content").html();
        if (curr_chat_content.length > 0){
            // 将当前聊天的临时记录保存下来
            MESSAGE_DB.push({'user':last_chat_user,'content':curr_chat_content});
            //console.log(MESSAGE_DB)
        }

        //2 清空当前聊天框记录
        $("#chat-content").html("");
    } //结束切换聊天对象

    //打印聊天的标题
    $("#talkwith").html("<h2>正在与好友 [ "+ choose_user_name +" ] 聊天</h2>");

    // 获取当前切换过来的对象聊天记录，填充到聊天窗口
    $(MESSAGE_DB).each(function () {
        var selected_user = $("#talkwith").attr("select_user");
        console.log('db_user：'+$(this).attr('user')+'  select_user:'+selected_user);
        console.log(MESSAGE_DB);
        if (selected_user == $(this).attr('user')){
            //将保存的信息显示到聊天框
            $("#chat-content").html($(this).attr('content'));

            //将好友分组和群组列表的tab框上面的消息提示数减法点击的标签的消息数
            var selecte_msg_count = $("#"+select_type+"_msg_"+choose_user_id).text();
            var curr_tab_totalmsgcount = $("#"+select_type+"_totalmsg").text();
            var left_count = parseInt(curr_tab_totalmsgcount) - parseInt(selecte_msg_count);
            $("#"+select_type+"_totalmsg").text(left_count);
            if (left_count == 0){
                //如果没有了就隐藏消息提示框
                $("#"+select_type+"_totalmsg").css({'display':'none'});
            }
            //如果右侧头像处有显示消息提示的,清空并隐藏消息提示
            $("#div_"+select_type+"_msg_"+choose_user_id).hide();
            $("#"+select_type+"_msg_"+choose_user_id).text(0);

            //滚动消息框
            $(".conversation-inner").animate({scrollTop:$(".conversation-inner")[0].scrollHeight},500);
        }
    });

}

// 点击分组中的好友名字，在聊天框上面保存获取聊天对象信息
$(".user_name").click(function () {
    var choose_user_id = $(this).attr('id');
    var choose_user_name = $(this).text();
    var choose_user_img = $(this).parent().parent().prevAll().first().children().attr("src");
    saveSelectedInfo('user',choose_user_id,choose_user_img,choose_user_name);

 });

//点击群组时的事件
$(".groupname").click(function () {
    var choose_group_id = $(this).attr('id');
    var choose_group_name = $(this).text();
    saveSelectedInfo('group',choose_group_id,'',choose_group_name);

});

//组合输入框textarea的消息到页面消息显示框
function PutMsgToFront(content) {
    var send_msg = "";
    var currDate = new Date();
    var show_date = currDate.getHours() +":"+currDate.getMinutes()+":"+currDate.getSeconds();
    //获取当前用户的头像图片,保存在master模板的id=login_user_head_img标签中
    var head_img = $("#login_user_head_img").attr("src");
    var curr_name = $("#login_user_head_img").siblings().first().text();
    //组合消息
    send_msg += "<div class=\"conversation-item item-right clearfix\">";
    send_msg += "<div class=\"conversation-user\">" ;
    send_msg += "<img src=\"" +head_img+"\"></div>";
    send_msg += "<div class=\"conversation-body\">";
    send_msg += "<div class=\"name\">"+curr_name+"</div>";
    send_msg += "<div class=\"time hidden-xs\">" + show_date +"</div>";
    send_msg += "<div class=\"text\">" + replace_em(content) + "</div></div></div>";
    //提交到前端
    $("#chat-content").append(send_msg);
    $(".conversation-inner").animate({scrollTop:$(".conversation-inner")[0].scrollHeight},500);
    $("#msg_area").val('');
}


// ajax 提交消息到后台保存到消息队列
function CommitMsgToQueue(send_message) {
    var to_user = $("#talkwith").attr("select_user");
    var post_data = {'to_user':to_user, 
                    'message':send_message,
                    'from_user_img':$("#login_user_head_img").attr('src'),
                    'msg_type':'txt',
                    'send_user_name':$("#login_user_head_img").siblings().first().text()};
    
    //console.log(to_user, post_data);
    $.post("/chat/sendmsg/",{'data':JSON.stringify(post_data)},function (data) {
        console.log("commit success")
    })
}


//检查当前是否有选中用户，没有选中的用户则无法发送消息
function isSelectUser() {
    var is_select = $("#talkwith").attr("is_select");
    if (is_select == "true"){
        return true
    }else{
        $("#talkwith").html("<h2>请选择一个聊天对象</h2>");
        return false
    }
}


//点击发送消息按钮触发事件
$("#btn_sendmsg").click(function () {
    //是否选中用户
    if (isSelectUser()){
        var input_content = $("#msg_area").val().trim();
        if (input_content.length > 0){
            PutMsgToFront(input_content); //发送到显示消息框
            CommitMsgToQueue(input_content); //发送到后台保存到Q
    }}
});


//输入框输入消息后获取按键事件，如果是回车就将消息输出到消息框
$("#msg_area").keydown(function (e) {
    if (e.which == 13){
        //按下Enter键
        if (isSelectUser()){
            var input_content = $(this).val().trim();
            if (input_content.length > 0){
                //空消息不做任何操作,有内容才发送
                PutMsgToFront(input_content);
                CommitMsgToQueue(input_content);
        }}
        console.log('later'+$(this).val()+"aa");
    }
});


//定时获取用户消息
function GetMsgFromQueue() {
    //var curr_user_id = $("#login_user_head_img").attr("uid");    
    $.getJSON("/chat/getmsg/", function(msg_data){
        console.log("Get msg ......");
        console.log("MSG IS :",msg_data);
        if (msg_data == 'error'){
            console.log('errors');
            
        }else{
            AnalysisMesssage(msg_data);
            GetMsgFromQueue();
        }
        
    });
}

// 组合从后台获取的一条消息为html格式
function buildFirendMsg(head_img,show_date,content,from_user_name,msg_type) {
    var send_msg = "";
    send_msg += "<div class=\"conversation-item item-left clearfix\">";
    send_msg += "<div class=\"conversation-user\">" ;
    send_msg += "<img src=\"" +head_img+"\"></div>";
    send_msg += "<div class=\"conversation-body\">";
    send_msg += "<div class=\"name\">"+from_user_name+"</div>";
    send_msg += "<div class=\"time hidden-xs\">" + show_date +"</div>";
    if (msg_type == "img"){
        send_msg += "<div class=\"text\"><a href='"+content+"' target='_blank' ><img height='50' width='50' src='" + content + "'></a></div></div></div>";
    }else {
        if (msg_type == "file") {
            var filename = content.split("/")[content.split("/").length - 1];
            send_msg += "<div class=\"text\"> "+filename+"<a href='" + content + "' target='_blank'> 下载 </a></div></div></div>";
        } else {
            send_msg += "<div class=\"text\">" + content + "</div></div></div>";
        }
    }
    
    return send_msg
    
}

//将从服务端获取的数据进行分析展示到前端聊天框
function AnalysisMesssage(recv_data) {
    $(recv_data).each(function () {
        //获取数据信息
        var from_user_id = $(this).attr("from_user");
        var from_user_name = $(this).attr("send_user_name");
        var from_user_img = $(this).attr("from_user_img");
        var from_user_msg = $(this).attr("message");
        var from_user_time = $(this).attr("send_date");
        var msg_type = $(this).attr("msg_type");
        var to_user = $(this).attr("to_user");
        //获取这条消息是本来直接发给我的还是通过group转过来的
        var msg_to_type = to_user.split("_")[0];
        if (msg_to_type == "group"){
            //如果消息是发给群组的，这个时候判断的是否from_user_id就不能是发送者的id了，而是send_to的id,
            from_user_id = to_user.split("_")[1];
        }

        var curr_msg_count = $("#"+msg_to_type+"_msg_"+from_user_id).text(); //当前已有来消息数量

        //将当前消息记录组合成可显示的html
        var new_msg = buildFirendMsg(from_user_img,from_user_time,from_user_msg,from_user_name,msg_type);

        //如果当前的聊天对话框就是这个消息的发送者，直接放到聊天对话框中
        var curr_talk_with = $("#talkwith").attr("select_user");
        if (curr_talk_with == msg_to_type +"_"+from_user_id){
            $("#chat-content").append(new_msg);
            $(".conversation-inner").animate({scrollTop:$(".conversation-inner")[0].scrollHeight},500);
        }else{
            //否则保存消息到MESSAGE_DB中,待用户点击的时候显示出来
            //将发送消息的用户的头像上加上信息提醒标识
            //将对应的来消息数加1
            console.log('befor add', curr_msg_count);
            $("#"+msg_to_type+"_msg_"+from_user_id).text(parseInt(curr_msg_count)+1);
            $("#div_"+msg_to_type+"_msg_"+from_user_id).show();
            console.log("group count:", $("#"+msg_to_type+"_msg_"+from_user_id).text());

            //对用户和群组的tab框上面添加消息提示框
            var totalmsgcount = $("#"+msg_to_type+"_totalmsg").text();
            $("#"+msg_to_type+"_totalmsg").text(parseInt(totalmsgcount)+1);
            $("#"+msg_to_type+"_totalmsg").css({'display':"block"});

            //将消息追加到临时保存消息框中
            var exists_user_msg = false;
            $(MESSAGE_DB).each(function () {
                if ($(this).attr('user') == msg_to_type + '_' + from_user_id){
                    //如果在之前的列表中找到有该用户的记录了,追加记录
                    var curr_content = $(this).attr('content');
                    curr_content += new_msg;
                    $(this).attr({'content':curr_content});
                    exists_user_msg = true;
                }
            });
            if (exists_user_msg == false){
                //没有保存的消息记录
                MESSAGE_DB.push({'user':msg_to_type + '_' + from_user_id,'content':new_msg})
            }
        }

    })
}

//从后台去用户状态
function loadFriendsStatus() {
    var online_html = "<i class=\"fa fa-check-circle\"></i><span style=\"color:limegreen\"> Online</span>";
    var offline_html = "<i class=\"fa fa-minus-circle\"></i><span style=\"color:red\"> Offline</span>";

    $.getJSON("/chat/friendstat",function (callback) {
        $(".online").each(function () {
            if (callback.indexOf(parseInt($(this).attr('id').split("_")[1])) > -1){
                $(this).html(online_html);
            }else{
                $(this).html(offline_html);
            }        
        });
    })
}

//打开上传图片或文件模态框
function send_msg(msgtype) {
    //如果当前没有和任何人聊天，则无法发送文件
    var chat_stat = $("#talkwith").attr("is_select");
    if (chat_stat == "false"){
        $("#talkwith").html("<h2>请选择一个聊天对象</h2>");
    }else{
        var to_user = $("#talkwith").attr("select_user");
        var from_user_img = $("#login_user_head_img").attr('src');
        var send_user_name = $("#login_user_head_img").siblings().first().text();
        $("#send_type").val(msgtype + '|' + to_user + '|' + from_user_img + '|' + send_user_name);
        $('#myModal').modal('show');
    }
    
}

//发送图片或文件到后台
function sendfile() {
    $(".file-content").hide();
    //$.post("/chat/",$("#form_sendfile").);
    var formdata = new FormData($("#form_sendfile")[0]);
    console.log($("#upfile")[0].files[0]);
    formdata.append('file',$("#upfile")[0].files[0]);
    console.log(formdata);
    //异步发送文件到后端
    $.ajax({
        url:"/chat/",
        type:'POST',
        data:formdata,
        contentType:false,
        processData:false,
        success:function (callback) {
            console.log(callback);
        }

    });
    console.log('commit');
    //显示进度条
    $(".progress").show();
    //调用文件大小请求函数获取传输进度
    var file_total_size = $("#upfile")[0].files[0].size;
    var file_name = $("#login_user_head_img").attr('uid') + "_" + $("#upfile")[0].files[0].name;
    getFileProgress(file_total_size, file_name);

}

//从服务端获取文件发送的状态
function getFileProgress(file_total_size, file_name){    
    var doprogress = setInterval(function () {
        $.getJSON('/chat/fileprocess/',{'file_name':file_name},function (recved_size) {            
            if (file_total_size == recved_size){
                $(".progress-bar").css('width','100%');
                $(".progress-bar").text("100%");
                clearInterval(doprogress);
                //关闭模态框
                $("#myModal").modal('hide');
                //恢复hide进度条，show文件上传标签
                $(".progress").hide();
                $(".file-content").show();
                //将精度条恢复初始值
                $(".progress-bar").css('width',"0%");
                $(".progress-bar").text("0%");
                //将发送成功的内容put到消息框
                var file_type = $("#send_type").val().split("|")[0];
                if (file_type == "img"){
                    var content = "<img src='/static/uploads/"+file_name+"' width='50' height='30'>"
                }else {
                    var content = '文件发送成功!';
                }
                PutMsgToFront(content)

            }else {
                var percent = parseInt((recved_size/file_total_size) * 100) + "%";
                console.log('recved:',recved_size, 'total:',file_total_size,'percent:',percent);
                $(".progress-bar").css('width',percent);
                $(".progress-bar").text(percent);
            }
            
        })
    
    }, 1000);
}

//将获取到的所有用户数据组合成html标签
function buildUserListHtml(userlist) {
    var html_list = "";
    $(userlist).each(function () {
       
        html_list += "<tr>";
        html_list += "<td><img src=\"/static/img/samples/" + $(this).attr('userimg') + " \">"+$(this).attr('username')+"</td>";
        html_list += "<td>"+$(this).attr('sex')+"</td>";
        html_list += "<td>" + $(this).attr('age') + "</td>";
        if ($(this).attr('status') == "online") {
            html_list += "<td class=\"text-center\"><span class=\"label label-success\"> 在线 </span></td>";
        }else {
            html_list += "<td class=\"text-center\"><span class=\"label label-default\"> 离线 </span></td>";
        }
        html_list += "<td style=\"width: 10%;\">";
        html_list += "<a href='#' class=\"table-link\" id='"+$(this).attr('id')+"' onclick='addMyFriend(this);'>";
        html_list += "<span class=\"fa-stack\">";
        html_list += "<i class=\"fa fa-square fa-stack-2x\"></i>";
        html_list += "<i class=\"fa fa-search-plus fa-stack-1x fa-inverse\"></i>";
        html_list += "</span></a></td></tr>";
    });
    
    return html_list;
}

GetMsgFromQueue();
//每2分钟获取一次好友状态
setInterval("loadFriendsStatus()",120000);


//添加好友search框键盘按下事件
$("#search-user").keydown(function (e) {
    if (e.which == 13){
        addFriends(1);
    }
});

//点击所有用户列表后面的添加按钮触发事件
function addMyFriend(ths) {
    var choose_user_id = $(ths).attr('id');
    //将当前选择用户id保存到插入数据库连接的a标签中
    $("#btn_insert_group").attr('choose_user',choose_user_id);

    //隐藏好友列表div，显示分组div
    $("#alluserlist").hide();
    $("#choose_groups").show();
    return false;
}


//返回
function back() {
    $("#choose_groups").hide();
    $("#alluserlist").show();
}

function replace_em(str){
    str = str.replace(/\</g,'<；');
    str = str.replace(/\>/g,'>；');
    str = str.replace(/\n/g,'<；br/>；');
    str = str.replace(/\[em_([0-9]*)\]/g,'<img src="/static/face/$1.gif" border="0" />');
    return str;
}

//查看成员列表
function viewMembers(group_id) {
    $("#show_groups").hide();
    $("#show_members").show();
    $.getJSON("/chat/loadmembers/",{groupid:group_id},function (member_list) {
        console.log(member_list);
        var mem_list_str="";
        $(member_list).each(function () {
            mem_list_str += "<li class=\"col-md-3\">";
            mem_list_str += "<div class=\"img\"><img src=\"/static/img/samples/"+$(this).attr('head_img')+"\"></div>";
            mem_list_str += "<div class=\"details\">"+$(this).attr('fullname')+"</div></li>";
        });
        $("#member-list").html(mem_list_str);
    });
    return false
}
//从查看成员列表返回组列表
function backmembers(){
    $("#show_groups").show();
    $("#show_members").hide();
    $("#member-list").html("");
}
//http://www.tuicool.com/articles/InuQfin