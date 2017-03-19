<td class="user-name"><%= user.username %></td>
<td ><img class="user-headimg" style="width:30px; height: 30px;" src="/static/img/account/<%= user.avatar %>"></td>
<td class="user-nickname"><%= user.nickname %></td>
<td class="user-email"><%= user.email %></td>
<td class="user-superuser"><%= user.is_superuser ? "管理员用户" : "普通用户" %></td>
<td class="user-groups"><%= user.groupname %></td>
<td class="user-cust"><%= user.usercust %></td>
<td class="user-active"><%= user.is_active ? "活动" : "锁定" %></td>
<td><%= user.date_joined %></td>
<td><%= user.last_login %></td>
<td class="cust-id" style="display:none"><%= user.cust_id %></td>
<td>
    <span class="pull-right">
        <a href="#"><i class="fa fa-lock btn-change-passwd" title="重置密码" uid="<%= user.id %>"></i></a>&nbsp;&nbsp;&nbsp;
        <a href="#"><i class="fa fa-edit btn-change-user"  title="编辑" uid="<%= user.id %>"></i></a>&nbsp;&nbsp;&nbsp;
        <a href="#"><i class="fa fa-times margin-r-10 btn-delete-user" title="删除" uid="<%= user.id %>"></i></a>
    </span>
</td>