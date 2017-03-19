/**
 * Created by super on 2016/10/21.
 */

define(function (require, exports, module){
    var $ = require("jquery");
    var Backbone = require('backbone');

    var GroupPermMenuItemView=require("./account_group_perm_item_view").GroupPermMenuItemView;
    var GroupPermAssetItemView=require("./account_group_perm_item_view").GroupPermAssetItemView;
    var GroupPermGroupItemView=require("./account_group_perm_item_view").GroupPermGroupsItemsView;

    var GroupPermView;
    GroupPermView = Backbone.View.extend({

        events: {
            "click #group-list-ul li span.group_name": "choose_group",
            "click #btn-add-group": "new_group",
            "click #btn_update_perm": "update_group_perms",
            "click #btn-change-group": "change_group",
            "click #btn-delete-group": "delete_group",
            "click #perm-menu-view-all": "select_view_menu_all",
            "click #perm-serv-view-all": "select_view_project_all",
            "click #perm-serv-add-all": "select_add_project_all",
            "click #perm-serv-change-all": "select_change_project_all",
            "click #perm-serv-delete-all": "select_delete_project_all",
            "click #perm-equi-view-all": "select_view_type_all",
            "click #perm-equi-add-all": "select_add_type_all",
            "click #perm-equi-change-all": "select_change_type_all",
            "click #perm-equi-delete-all": "select_delete_type_all"


        },

        initialize: function (options) {
            this.canFetch = false;
            this.perms = {};
            this.collection.url = options.url;
            this.model= options.model;
            this.listenTo(this.collection, "reset", this.showGroupPerms);

        },
        // 选中组名后触发的事件
        choose_group: function (e) {
            var gid = $(e.currentTarget).siblings("span.group_id").text();
            console.log("gid=", gid);
            // 在权限列表后面显示组名
            this.$el.find("#perm_show_group_name").text(" [" + $(e.currentTarget).text() + "]");
            //将组id追加到button的属性中
            this.$el.find("#btn_update_perm").attr("group_id", gid);
            this.$el.find("#btn_update_perm").removeAttr("disabled");
            // 点击后显示组的所有权限


            this.collection.fetchData(true, JSON.stringify({gid: gid}));

        },
        //渲染组的权限页面
        showGroupPerms: function () {
            // 将所有全选checkbox的checked属性置为空
            var all_checkbox_tag = this.$el.find("table th span input");
            $.each(all_checkbox_tag, function (idx, obj) {
               $(obj).prop("checked", false);
            });
            // 开始渲染权限列表页面
            this.collection.each(this.showItemPerms, this);
        },
        showItemPerms: function (model) {
            var perm_model = model.toJSON();
            // 渲染菜单 menu
            var menu_items_view = new GroupPermMenuItemView({model: perm_model.group_perm.menu});

            this.$el.find("#group-perm-menu-table tbody").remove();
            this.$el.find("#group-perm-menu-table").append(menu_items_view.render().el);

            // 渲染 project
            var project_items_view = new GroupPermAssetItemView({
                model: perm_model.group_perm.projects,
                classattrname: "perm-project"
            });
            this.$el.find("#group-perm-server-table tbody").remove();
            this.$el.find("#group-perm-server-table").append(project_items_view.render().el);

            // 渲染 assettype
            var type_items_view = new GroupPermAssetItemView({
                model: perm_model.group_perm.equipmenttype,
                classattrname: "perm-type"
            });
            this.$el.find("#group-perm-equipment-table tbody").remove();
            this.$el.find("#group-perm-equipment-table").append(type_items_view.render().el);

            this.loadGroupPerms(perm_model.group_perm, this);
            //console.log("All Perms", perm_model)
        },
        // 将当前组的权限按照规则加载到 this.perms 中，方便再次操作的时候修改权限
        loadGroupPerms: function (perms, view_obj) {
            var menu_perms = perms.menu;
            var projects_perms = perms.projects;
            var equipment_perms = perms.equipmenttype;
            view_obj.perms = {
                "account.view_menus": [],
                "cmdb.view_projects": [],
                "cmdb.add_projects": [],
                "cmdb.change_projects": [],
                "cmdb.delete_projects": [],
                "cmdb.view_baseequipmenttype": [],
                "cmdb.add_baseequipmenttype": [],
                "cmdb.change_baseequipmenttype": [],
                "cmdb.delete_baseequipmenttype": []
            };

            //加载菜单权限
            $.each(menu_perms, function (idx, obj) {
                if (obj.view == 1){
                    view_obj.perms["account.view_menus"].push(obj.id);
                }
            });
            //加载projects权限
            $.each(projects_perms, function (idx, obj) {
                if (obj.view == 1){view_obj.perms["cmdb.view_projects"].push(obj.id)}
                if (obj.add == 1){view_obj.perms["cmdb.add_projects"].push(obj.id)}
                if (obj.change == 1){view_obj.perms["cmdb.change_projects"].push(obj.id)}
                if (obj.deleted == 1){view_obj.perms["cmdb.delete_projects"].push(obj.id)}
            });
            //加载设备type权限
            $.each(equipment_perms, function (idx, obj) {
                if (obj.view == 1){view_obj.perms["cmdb.view_baseequipmenttype"].push(obj.id)}
                if (obj.add == 1){view_obj.perms["cmdb.add_baseequipmenttype"].push(obj.id)}
                if (obj.change == 1){view_obj.perms["cmdb.change_baseequipmenttype"].push(obj.id)}
                if (obj.deleted == 1){view_obj.perms["cmdb.delete_baseequipmenttype"].push(obj.id)}
            });
            //console.log("curr group's perm list", view_obj.perms)
        },

        //点击查看菜单权限的全选按钮触发事件
        select_view_menu_all:function (e) {
            // console.log($(e.currentTarget).prop("checked"));
            this.change_checkbox_checked_prop("perm-menu","view", $(e.currentTarget).prop("checked"));
        },
        //点击 主机权限 查看的全选 触发事件
        select_view_project_all:function (e) {
            this.change_checkbox_checked_prop("perm-project", "view", $(e.currentTarget).prop("checked"));
        },
        //点击 主机权限 添加的全选 触发事件
        select_add_project_all:function (e) {
            this.change_checkbox_checked_prop("perm-project", "add", $(e.currentTarget).prop("checked"));
        },
        //点击 主机权限 修改的全选 触发事件
        select_change_project_all:function (e) {
            this.change_checkbox_checked_prop("perm-project", "change", $(e.currentTarget).prop("checked"));
        },
        //点击 主机权限 删除的全选 触发事件
        select_delete_project_all:function (e) {
            this.change_checkbox_checked_prop("perm-project", "delete", $(e.currentTarget).prop("checked"));
        },
        //点击 设备权限 查看的全选 触发事件
        select_view_type_all:function (e) {
            this.change_checkbox_checked_prop("perm-type", "view", $(e.currentTarget).prop("checked"));
        },
        //点击 设备权限 添加的全选 触发事件
        select_add_type_all:function (e){
            this.change_checkbox_checked_prop("perm-type", "add", $(e.currentTarget).prop("checked"));
        },
        //点击 设备权限 修改的全选 触发事件
        select_change_type_all:function (e) {
            this.change_checkbox_checked_prop("perm-type", "change", $(e.currentTarget).prop("checked"));
        },
        //点击 设备权限 删除的全选 触发事件
        select_delete_type_all:function (e) {
            this.change_checkbox_checked_prop("perm-type", "delete", $(e.currentTarget).prop("checked"));
        },
        //选中checkbox的公共方法,根据classname和perm属性来选择
        change_checkbox_checked_prop: function (classname, permprop, check_status) {
            var choose_menu_checkbox_list = this.$el.find("input."+classname+"[perm='"+permprop+"']");
            $.each(choose_menu_checkbox_list, function (idx, obj) {
                // if ($(obj).prop("checked")){
                //     $(obj).prop("checked", false)
                // }else{
                //     $(obj).prop("checked", true)
                // }
                $(obj).prop("checked", check_status)
            })
        },

        // 获取所有选中的菜单权限
        get_menu_perms: function (checked_menu) {
            // console.log(checked_menu);
            for (var i=0;i<checked_menu.length;i++) {
                var choose_obj = $(checked_menu[i]);

                var menu_id = parseInt(choose_obj.val());
                var menu_perm = choose_obj.attr("perm");
                var menu_perm_value = 0;
                if (choose_obj.prop("checked")) {
                    menu_perm_value = 1;
                }
                // console.log("menu_perm_value:", menu_id, menu_perm_value);
                // 如果view_menu中有当前的id号，从列表中删除
                if (this.perms["account.view_menus"].indexOf(menu_id) >= 0){
                    this.perms["account.view_menus"].splice(this.perms["account.view_menus"].indexOf(menu_id), 1);
                }
                if (menu_perm_value == 1){
                    //如果选中，追加到perms中
                    this.perms["account.view_menus"].push(menu_id)
                }
            };


        },
        // 遍历所有项目权限checkbox的方法
        get_projects_perms: function (checked_projects) {
            for (var i=0;i<checked_projects.length;i++){
                this.asset_perm_get(checked_projects[i], "_projects");
            }

        },
        // 设备资产类型权限
        get_equipmenttype_perms: function (checked_types) {
            for (var i=0;i<checked_types.length;i++) {
                this.asset_perm_get(checked_types[i], "_baseequipmenttype");
            }
        },
        asset_perm_get: function (project, perm_name) {
            var choose_obj = $(project);
            var project_id = parseInt(choose_obj.val());
            var project_perm = "cmdb."+choose_obj.attr("perm") + perm_name;
            var project_perm_value = 0;
            if (choose_obj.prop("checked")) {
                project_perm_value = 1;
            }
            // console.log(project_perm);
            // 如果view_menu中有当前的id号，从列表中删除
            if (this.perms[project_perm].indexOf(project_id) >= 0){
                this.perms[project_perm].splice(this.perms[project_perm].indexOf(project_id), 1);
            }
            if (project_perm_value == 1){
                //如果选中，追加到perms中
                this.perms[project_perm].push(project_id)
            }
        },
        //点击更新权限按钮触发事件
        update_group_perms: function () {
            var btn_obj = this.$el.find("#btn_update_perm");
            var group_id = btn_obj.attr("group_id");
            var post_url = this.collection.url;

            // 获取所有选中的菜单权限 menus
            var menus = this.$el.find("input.perm-menu");
            this.get_menu_perms(menus);
            // 获取所有选中的项目权限 projects
            var projects = this.$el.find("input.perm-project");
            this.get_projects_perms(projects);
            // 获取所有选中的设备类型权限 types
            var equipmenttypes = this.$el.find("input.perm-type");
            this.get_equipmenttype_perms(equipmenttypes);
            // 总的所有权限
            var group_perms = this.perms;
            var post_data = {"group_id":group_id, "perms":group_perms};

            var new_model = new this.model();
            new_model.url = this.collection.url;
            new_model.save({"data":post_data});
            //修改编辑状态为不可用
            btn_obj.attr("disabled", true);
            // 提交
            // $.ajax({
            //     url:post_url,
            //     type:"POST",
            //     dataType:"json",
            //     data:{data:JSON.stringify(post_data)},
            //     success:function (callback) {
            //         console.log(callback.info);
            //         //修改编辑状态为不可用
            //         btn_obj.attr("disabled", true);
            //
            //     }
            // });

        },
        // 添加、修改、删除 一个组的公共方法
        new_group: function () {
            var group_name = this.$el.find("#groupname").val();
            var exists_group_name_tag = this.$el.find(".group_name");
            var exists_group_name_list = [];
            $.each(exists_group_name_tag, function (idx, obj) {
                exists_group_name_list.push($(obj).text())
            });
            //判断是否为空
            if (group_name.length == 0) {
                swal({title: "组名不能为空", type: "warning"});
                return false;
            }
            //判断组名是否存在
            console.log(exists_group_name_list);
            if (exists_group_name_list.indexOf(group_name) >= 0) {
                swal({title: "组名已经存在", type: "error"});
                return false
            }

            var action = this.$el.find("#btn-add-group").attr("action");
            console.log(action);
            if (action == "add") {
                //添加
                var request_data = {"group_name": group_name, "action": action};
            }else {
                // 编辑或删除
                var group_id = this.$el.find("#btn-add-group").attr("group_id");
                var request_data = {"group_name": group_name, "id":group_id,"action": action};
            }

            //提交数据到后台
            var group_model = new this.model();
            group_model.url = "/account/group_modify";
            group_model.set("data",request_data);
            group_model.self = this;
            // console.log("response.data:",request_data);
            // console.log("model.attributes:",group_model.attributes);
            group_model.save(group_model.attributes, {
                success: function (model, response, options) {
                    // console.log(model);
                    var self_collection = model.self; //获取当前model的collections

                    var group_items_view = new GroupPermGroupItemView({ model: model.toJSON()});
                    if(action=="add") {
                        //self_collection.$el.find("#group-list-ul").append(group_items_view.render().el);
                        self_collection.after_group_add(group_items_view);
                    }
                    if(action=="change"){
                        self_collection.after_group_change(group_name);
                    }
                    self_collection.$el.find("#groupname").val("");
                }
            });
            // group_model.save({"data":request_data})

        },
        // 添加组 提交后台成功后添加组到页面
        after_group_add: function (group_item_view) {
          this.$el.find("#group-list-ul").append(group_item_view.render().el)
        },
        // 更新组 提交后台成功后更新页面组名
        after_group_change: function (new_group_name) {
            //修改添加按钮的名字
            var button_obj =  this.$el.find("#btn-add-group");
            button_obj.text("添加");
            button_obj.removeAttr("group_id");
            button_obj.attr("action","add");
            this.$el.find("#add-group-title").text("添加组");
            //修改组名为新名字
            var old_group = this.$el.find(".group_name[choosed=true]");
            old_group.text(new_group_name);
            old_group.removeAttr("choosed");

        },
        // 编辑组
        change_group:function (e) {
            // 获取id
            var group_id = $(e.currentTarget).parent().siblings(".group_id").text();
            var group_name = $(e.currentTarget).parent().siblings(".group_name").text();
            // console.log("group_id", group_id);
            //修改添加按钮的名字
            this.$el.find("#add-group-title").text("编辑组");
            this.$el.find("#btn-add-group").text("修改");
            this.$el.find("#btn-add-group").attr("group_id",group_id);
            this.$el.find("#btn-add-group").attr("action","change");
            //将组名添加到输入框
            this.$el.find("#groupname").val(group_name);
            //标记当前选中组
            $(e.currentTarget).parent().siblings(".group_name").attr("choosed",true);
        },
        // 删除组
        delete_group: function (e) {
            //防止先点击查看权限在点击删除
            this.$el.find("#btn_update_perm").attr("disabled", true);
            var group_id = $(e.currentTarget).parent().siblings(".group_id").text();
            var new_model = new this.model();
            new_model.url =  "/account/group_modify";
            var post_data = {"id":group_id, "action":"delete"};

            swal({title:"确定要删除该组吗?",
                text:"删除该组后,该组下的所有用户权限都将删除!",
                type:"warning",
                showCancelButton:true,
                confirmButtonText: "确认",
                cancelButtonText: "取消",
                closeOnConfirm: false,
                closeOnCancel: true},
            function(isConfirm){
                if (isConfirm) {
                    new_model.save({"data":post_data}, {success:function (returndata, response) {
                        if (response.status){
                            $(e.currentTarget).parent().parent().parent().remove();
                        }
                    }});

                }
            }
            );
        }
    });

    return GroupPermView

});