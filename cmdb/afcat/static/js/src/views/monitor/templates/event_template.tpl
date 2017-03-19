<% if (data_parentid == 0) { %>
<td data-switcherid="<%= data_switcherid %>" data-parent="<%= parent %>"><span class="arrow-right mycaret"></span></td>
<td class="<%= issue_id == 0 ? 'normal-bg' : 'average-bg' %>"><%= priority %></td>
<td class="<%= issue_id == 0 ? 'normal' : 'issue' %>"><%= issue %></td>
<td><%= date_time %></td>
<td class="<%= ack_id == 0 ? 'no' : 'yes' %>"><%= ack %></td>
<td><a href="/monitor/host/<%= host_id %>/detail_info/" target="_blank"><%= host_name %></a></td>
<td><%= info %></td>
<% } else { %>
<td colspan="2" data-parentid="<%= data_parentid %>"></td>
<td class="<%= issue_id == 0 ? 'normal' : 'issue' %>"><%= issue %></td>
<td><%= date_time %></td>
<td class="<%= ack_id == 0 ? 'no' : 'yes' %>"><%= ack %></td>
<td colspan="2"></td>
<% } %>

