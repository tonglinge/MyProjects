<table class="table table-hover table-striped ">
    <thead class="search-head">
        <tr>
            <% _.each(tables_data['fields_name'], function(fields, index){ %>
                <% for(var key in fields){ %>
                    <% if(index == 0){ %>
                        <th data-field="<%= key %>"><input type="checkbox" class="btn btn-default btn-sm all_checkbox" /></th>
                    <% } else { %>
                        <th data-field="<%= key %>"><%= fields[key] %></th>
                    <% } %>
                <% } %>
            <% }) %>
        </tr>
    </thead>
    <tbody>
        <% _.each(tables_data['records'], function(fields){ %>
            <tr>
                <% _.each(fields, function(field, index){ %>
                    <% for(var key in field){ %>
                        <% if(index == 0){ record_id=field[key] %>
                            <td>
                                <input type="checkbox" class="btn btn-default btn-sm record_checkbox" data-record-id="<%= record_id %>" />
                            </td>
                        <% } else { %>
                            <td data-field="<%= key %>" >
                            <% if(index == 1){ %>
                                <a href="?id=<%= record_id %>&target=<%= table_name %>"><%= field[key] %></a>
                            <% } else { %>
                                <%= field[key] %>
                            <% } %>
                            </td>
                        <% } %>
                    <% } %>
                <% }) %>
            </tr>
        <% }) %>

    </tbody>
</table>