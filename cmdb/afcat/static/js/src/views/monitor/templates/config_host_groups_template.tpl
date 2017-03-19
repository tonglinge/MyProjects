<td>
    <a class="link group_name" style="cursor: pointer" data-group-id="<%= group_id %>"><%= group_name %></a>
</td>
<td>
    <% _.each(hosts, function(host){ %>
        <a href="/monitor/host/<%= host.host_id %>/detail_info/" data-host-id="<%= host.host_id %>" class="green"><%= host.host_name %></a><i>,</i>
    <% }) %>
</td>