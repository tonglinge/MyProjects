<option value="0">所有</option>
<% _.each(get_groups, function(group){ %>
    <option value="<%= group.group_id %>"><%= group.group_name %></option>
<% }) %>