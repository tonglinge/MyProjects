<% _.each(data, function(audit, index){ %>
<li class="info">
    <div class="timeline-simple-wrap">
        <p class="info-title"><%= audit.operater %></p><span class="timeline-simple-date"><%= audit.operate_time %>   </span>
        <span style="width:200px;text-overflow:ellipsis;white-space:nowrap;display: inline-block;overflow: hidden;"
              title="<%= audit.operate_data %>"><%= audit.action %>&nbsp;&nbsp;<%= audit.model_name %>：&nbsp; <%= audit.operate_data %> </span>

    </div>
</li>
<% }) %>