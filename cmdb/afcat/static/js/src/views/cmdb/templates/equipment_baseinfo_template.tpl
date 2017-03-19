<td><a href="/cmdb/equipment_detail/list?sid=<%= id %>"><%= assetname %></a></td>
<td><%= assettype %></td>
<td><%= netarea %></td>
<td><%= room %></td>
<td><%= cabinet %></td>
<td><%= unitinfo %></td>
<td><%= model %></td>
<td><%= manageip %></td>
<td><%= staffs %></td>
<td id="<%= id %>">
    <% if(changeperm){ %>
        <a  type="button" href="/cmdb/modify_equipment/list?action=edit&sid=<%= id %>" id="btn_edit_equipment"><i class="fa fa-edit"></i></a>&nbsp;
    <% } %>
    <a  type="button" href="/cmdb/modify_equipment/list?action=clone&sid=<%= id %>" class="clone-equipment" id="btn-clone-equipment"><i class="fa fa-copy"></i></a>
    <% if(delperm){ %>
        <a type="button" href="#" id="btn_delete_equipment"><i class="fa fa-remove"></i></a>
    <% } %>

    <a href="/cmdb/equipment_detail/list?sid=<%= id %>"><i class="fa fa-th"></i></a>
</td>
