<td><a href="/cmdb/server_asset_detail/list?sid=<%= id %>"><%= assettype %></a></td>
<td><%= cabinet %></td>
<td><%= unitinfo %></td>
<td><%= model %></td>
<td><%= sn %></td>
<td><%= cpu %></td>
<td><%= memory %></td>
<td class="hostcount"><%= hostcount %></td>
<td><%= expiredate %></td>
<td>
    <% if(changeperm){ %>
        <a type="button" href="/cmdb/modify_server_asset/list?action=edit&sid=<%= id %>"><i class="fa fa-edit"></i></a>&nbsp;
    <% } %>
    <a type="button" href="/cmdb/modify_server_asset/list?action=clone&sid=<%= id %>" class="clone-server-asset"><i class="fa fa-copy"></i></a>
    <% if(delperm){ %>
        <a href="#" type="button" id="delete-server-asset"><i class="fa fa-remove"></i></a>
    <% } %>
    <a type="button" href="/cmdb/server_asset_detail/list?sid=<%= id %>"><i class="fa fa-th"></i></a>
</td>
