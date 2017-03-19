<% _.each(project, function(p){ %>
<tr>
<td><%= p.name %></td>
<td><input type="checkbox" value="<%= p.id %>" perm="view" class="<%= classattrname %>" <%= p.view ? 'checked' : "" %> ></td>
<td><input type="checkbox" value="<%= p.id %>" perm="add" class="<%= classattrname %>" <%= p.add ? 'checked' : "" %> ></td>
<td><input type="checkbox" value="<%= p.id %>" perm="change" class="<%= classattrname %>" <%= p.change ? 'checked' : "" %> ></td>
<td><input type="checkbox" value="<%= p.id %>" perm="delete" class="<%= classattrname %>" <%= p.deleted ? 'checked' : "" %> ></td>
</tr>
<%}) %>