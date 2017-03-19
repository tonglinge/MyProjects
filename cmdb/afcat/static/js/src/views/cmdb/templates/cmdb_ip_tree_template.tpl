<ul class="iptree" style="list-style-type: none;padding-left:15px">
    <li>
        <% if(typeof(datacenter) != "undefined"){ %>
            <i class="fa fa-plus"></i>
            <span ip-id=""><%= datacenter %></span>
        <% }else{ %>
            <% if(ip.allocate > 0){ %>
                <i class="fa fa-plus"></i>
            <% } %>
            <span ip-id="<%= ip.id %>" ><%= ip %></span>
        <% } %>

        <ul class="iptree" style="display:none;list-style-type: none;padding-left:15px">
            <% if(ip){ %>
                <% _.each(ip, function(ip){ %>
                <li>
                    <% if(ip.allocate > 0){ %>
                        <i class="fa fa-plus"></i>
                    <% } %>
                    <span ip-id="<%= ip.id %>"><%= ip.ip %></span>
                </li>
                <% }) %>
            <% } %>
        </ul>

    </li>
</ul>