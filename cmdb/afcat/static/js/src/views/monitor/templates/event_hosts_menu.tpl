<option value="0">所有</option>
<% _.each(get_hosts, function(host){ %>
    <option value="<%= host.host_id %>"><%= host.host_name %></option>
<% }) %>