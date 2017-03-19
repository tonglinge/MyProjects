<div class="col-sm-4">

</div>
<div class="col-sm-8">

    <div class="dataTables_paginate pull-right">
        <ul class="pagination" style="padding-top:0;margin:0">
            <% if(curr_page > 1){ %>
                <li class="paginate_button previous" id="<%= parseInt(curr_page)-1 %>"><a href="#" aria-controls="example1" data-dt-idx="0" tabindex="0"><i class="fa fa-chevron-left"></i></a></li>
            <% }else{ %>
                <li class="paginate_button previous disabled" id="<%= parseInt(curr_page)-1 %>"><a href="#" aria-controls="example1" data-dt-idx="0" tabindex="0"><i class="fa fa-chevron-left"></i></a></li>
            <% } %>
            <% page_edge = parseInt(curr_page/10) %>
            <% if(page_edge == 0){ %>
                <% for(var i=page_edge*10+1;i<=(page_edge+1)*10;i++){ %>
                    <% if(i <= num_pages){ %>
                        <% if (i == curr_page){ %>
                            <li class="paginate_button active"  id="<%= curr_page %>"><a href="#" aria-controls="example1" data-dt-idx="1" tabindex="0"><%= curr_page %></a></li>
                        <% }else{ %>
                            <li class="paginate_button"  id="<%= i %>"><a href="#" aria-controls="example1" data-dt-idx="2" tabindex="0"><%= i %></a></li>
                        <% } %>
                    <% } %>
                <% } %>
            <% }else{ %>
                <% for(var i=page_edge*10;i<(page_edge+1)*10+1;i++){ %>
                    <% if(i <= num_pages){ %>
                        <% if (i == curr_page){ %>
                            <li class="paginate_button active"  id="<%= curr_page %>"><a href="#" aria-controls="example1" data-dt-idx="1" tabindex="0"><%= curr_page %></a></li>
                        <% }else{ %>
                            <li class="paginate_button"  id="<%= i %>"><a href="#" aria-controls="example1" data-dt-idx="2" tabindex="0"><%= i %></a></li>
                        <% } %>
                    <% } %>
                <% } %>
            <% } %>

            <% if(curr_page < num_pages){ %>
                <li class="paginate_button next"   id="<%= parseInt(curr_page)+1 %>"><a href="#" aria-controls="example1" data-dt-idx="0" tabindex="0"><i class="fa fa-chevron-right"></i></a></li>
            <% }else{ %>
                <li class="paginate_button next disabled"   id="<%= parseInt(curr_page)+1 %>"><a href="#" aria-controls="example1" data-dt-idx="0" tabindex="0"><i class="fa fa-chevron-right"></i></a></li>
            <% } %>
        </ul>

    </div>
    <div class="dataTables_info pull-right">
        <p>共
        <% if(total_count){ %>
            <%= total_count %>
        <% }else{ %>
            0
        <% } %>

        条数据&nbsp;</p>
    </div>
</div>