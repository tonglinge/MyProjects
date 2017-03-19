<% _.each(get_event_triggers_status, function(info){ %>
    <tr>
        <td class="<%= info.issue_id == 0 ? 'normal-bg' : 'average-bg' %>"><%= info.priority %></td>
        <td><%= info.datetime %></td>
        <td class="<%= info.ack_id == 0 ? 'no' : 'yes' %>"><%= info.ack %></td>
        <td><a href="/monitor/host/<%= info.host_id %>/detail_info/" target="_blank"><%= info.host_name %></a></td>
        <td class="issue"><%= info.description %></td>
    </tr>
<% }) %>
<% if(get_event_triggers_status.length == 0){ %>
<tr><td colspan="5" style="color: #00a65a">当前没有任何告警信息</td></tr>
<% } %>