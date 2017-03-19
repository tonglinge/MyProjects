<td width="15%"><%=vsname %></td>
<td width="10%"><%=vsaddr%>:<%=port%></td>
<td width="10%"><%=equipment %></td>
<td width="10%"><%=dnsdomain %></td>
<td width="10%"><%=snataddr.replace(RegExp(',','g'),'</br>') %></td>
<td width="10%"><%=pooladdr.replace(RegExp(',','g'),'</br>') %></td>
<td width="10%"><%=netarea %></td>
<td width="10%"><%=ploy %></td>
<td width="10%" rid="<%=id %>">
    <a type="button" href="#" class="btn-info-edit"><i class="fa fa-edit" title="编辑"></i></a>&nbsp;
    <a type="button" href="#" class="clone-equipment btn-info-clone"><i class="fa fa-clone" title="克隆"></i></a>
    <a type="button" href="#" class="btn-info-delete"><i class="fa fa-remove" title="删除"></i></a>
    <a href="#" class="btn-info-detail"><i class="fa fa-th" title="详情"></i></a>
</td>