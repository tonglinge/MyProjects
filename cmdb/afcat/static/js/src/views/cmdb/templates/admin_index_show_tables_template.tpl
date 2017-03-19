<% _.each(models_list, function(model, index){ %>
<li><a href="#tables_data" data-model-name="<%= model.object_name %>" data-table-alias="<%= model.verbose_name %>"><i class="fa fa-inbox"></i> <%= model.verbose_name %></a></li>
<% }) %>

