<% _.each(menu, function(menus){ %>
<tr>
<td><%= menus.name %></td>
<td><input type="checkbox" value="<%= menus.id %>" perm="view" class="perm-menu" <%= menus.view ? 'checked' :"" %> ></td>
</tr>
<% }) %>