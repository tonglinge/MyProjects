<% if (search_key == "sys") { %>
    <td>
        <% _.each(projects, function(project){ %>
            <%= project %><br/>
        <% }) %>
    </td>
    <td>
        <% _.each(probusiness, function(business){ %>
            <%= business %><br/>
        <% }) %>
    </td>
    <td><a href="/cmdb/server_host_detail/list?sid=<%= id %>"><%= hostname %></a></td>
    <td><%= type %></td>

<% }else{ %>
    <td><a href="/cmdb/server_host_detail/list?sid=<%= id %>"><%= hostname %></a></td>
    <td><%= type %></td>
    <td><%= business %></td>
<% } %>

<td><%= cabinet %></td>
<td><%= unitinfo %></td>
<td><%= staffs %></td>
<td><%= model %></td>
<td><%= partition %></td>
<td><%= netarea %></td>
<td><%= remark %></td>
<td>
    <% if(changeperm){ %>
        <a href="/cmdb/modify_server_host/list?action=edit&sid=<%= id %>"><i class="fa fa-edit"></i></a>&nbsp;
    <% } %>
    <a href="/cmdb/modify_server_host/list?action=clone&sid=<%= id %>" class="clone-server-host"><i class="fa fa-copy"></i></a>&nbsp;
    <% if(delperm){ %>
        <a href="#" id="delete-server-asset"><i class="fa fa-remove"></i></a>
    <% } %>
    <a href="/cmdb/server_host_detail/list?sid=<%= id %>"><i class="fa fa-th"></i></a>
</td>
