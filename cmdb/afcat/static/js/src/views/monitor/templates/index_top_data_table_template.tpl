<div class="box box-info">
    <div class="box-header with-border">
        <h3 class="box-title"><%= name %>(<%= unit %>)</h3>
        <div class="box-tools pull-right">
            <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i>
            </button>
            <button type="button" class="btn btn-box-tool" data-widget="remove"><i class="fa fa-times"></i></button>
        </div>
    </div>
    <div class="box-body">
        <div class="col-md-12">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>主机名</th>
                        <th>描述</th>
                        <th>时间</th>
                        <th>值</th>
                    </tr>
                </thead>
                <tbody>
                    <% _.each(item_value, function(data){ %>
                    <tr>
                        <td><a href="/monitor/host/<%= data.host_id %>/detail_info/" target="_blank"><%= data.host_name %></a></td>
                        <td><%= data.description %></td>
                        <td><%= data.datetime %></td>
                        <td class="issue"><%= data.value %></td>
                    </tr>
                    <% }) %>
                </tbody>
            </table>
        </div>
    </div>

</div>