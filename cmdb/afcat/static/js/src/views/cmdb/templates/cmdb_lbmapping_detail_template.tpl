<tr>
    <th>vs名称：</th>
    <td><%=vsname %></td>
    <th>所属设备：</th>
    <td><%=equipment%></td>
</tr>
<tr>
    <th>vs地址：</th>
    <td><%=vsaddr %>:<%=port %></td>
    <th>DNS域名：</th>
    <td><%=dnsdomain%></td>
</tr>
<tr>
    <th>SNAT地址池：</th>
    <td><%=snataddr.replace(RegExp(',','g'),'</br>') %></td>
    <th>服务器地址池：</th>
    <td><%=pooladdr.replace(RegExp(',','g'),'</br>') %></td>>
</tr>
<tr>
    <th>数据中心：</th>
    <td><%=datacenter %></td>
    <th>所属区域：</th>
    <td><%=netarea %></td>
</tr>
<tr>
    <th>系统名称：</th>
    <td><%=project %></td>
    <th>所属业务：</th>
    <td><%=business %></td>
</tr>
<tr>
    <th>主机类型:</th>
    <td><%=hosttype %></td>
    <th>主机名:</th>
    <td><%=hostname %></td>
</tr>
<tr>
    <th>所属VLAN：</th>
    <td><%=vlan %></td>
    <th>负载策略：</th>
    <td><%=ploy %></td>
</tr>
<tr>
    <th>备注：</th>
    <td colspan="3"><%=remark %></td>
</tr>