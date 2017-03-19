/**
 * Created by zengchunyun on 2016/9/30.
 */

//配置主机组页面
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var ConfigHostGroupsItemView = require("./monitor_config_host_groups_item_view").ConfigHostGroupsItemView;


    var ConfigHostGroupsView = Backbone.View.extend({
        events: {
            "click #move-left": "moveLeft",
            "click #move-right": "moveRight",
            "click #create_group": "createGroup",
            "click #modify_group": "modifyGroup",
            "click #del_group":"delGroup",
            "click .btn-create-group": "showCreatePage",
            "click #quit_create_group": "quitCreatePage",
            "click a.group_name": "showModifyPage"
        },
        initialize: function (options) {
            this.addToMenu = false;
            this.collection.url = options.url;
            this.model = options.options.model;
            this.action = null;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, {get_hosts_groups: true})
        },
        addAll: function () {
            this.collection.each(this.addOne, this);
            this.action = null;
        },
        addOne: function (model) {
            var view = new ConfigHostGroupsItemView({model: model});
            var group_id = model.get("group_id");
            var group_name = model.get("group_name");
            var update_group = this.$el.find("a[data-group-id=" + group_id + "]");
            var del_group = model.get("del_group");
            if(this.action == 'create' || this.action == 'modify'){
                if(model.get('hosts') && model.get('hosts').length){
                    if(!$('[data-group-menu-id="'+ group_id +'"]').length){
                        var new_group_menu = '<li><a href="/monitor/config/host_groups/'+ group_id +'" data-group-menu-id="'+ group_id +'"><i class="fa fa-circle-o"></i> '+ group_name +'</a></li>';
                        $("#monitor_groups_menu").append(new_group_menu);
                    }
                }
            } else if(this.action == 'delete'){
                $('[data-group-menu-id="'+ group_id +'"]').parent().remove()
            }
            if(del_group){
                update_group.parents("tr").remove();
            }else {
                var del_hosts = model.get("del_hosts");
                if(update_group.length != 0){
                    var update_html = $(view.render().el).find("td:last").html();
                    update_group.html(group_name);
                    update_group.parents("td").next().append(update_html);
                }else {
                    this.$el.find(".management_groups").append(view.render().el);
                    if(this.addToMenu){
                        this.$el.find("#group_id").append("<option value='"+ group_id +"'>"+ group_name +"</option>");
                        this.addToMenu = false;
                    }
                }
                if(del_hosts){
                    for(var i=0; i<del_hosts.length;i++){
                        update_group.parents("td").next().find("[data-host-id="+del_hosts[i]+"]").next().remove();
                        update_group.parents("td").next().find("[data-host-id="+del_hosts[i]+"]").remove();
                    }
                }
            }
        },
        moveLeft: function (e) {
            //此方法针对配置主机组页面，用于将其他组的主机移到新建组
            this.addOneSelected('host_id','host_set');
        },
        moveRight: function (e) {
            //此方法针对配置主机组页面，用于将新建组的主机移走
            this.addOneSelected('host_set','host_id');
        },
        addOneSelected: function (srcid,destid) {
            var src = document.getElementById(srcid);
            var dest = document.getElementById(destid);

            for (var i = src.length - 1; i >= 0; i--) {
                if(src.options[i].selected == true && src.options[i].value == 0){
                    this.addAllSelected(srcid,destid);
                    break;
                }else if (src.options[i].selected == true) {
                    dest.options.add(new Option(src.options[i].text,src.options[i].value));
                    src.options.remove(i);
                }
            }
        },
        addAllSelected: function (srcid,destid) {
            var src = document.getElementById(srcid);
            var dest = document.getElementById(destid);
            for (var i = 0; i < src.length; i++) {
                if(src.options[i].value == 0){
                    continue;
                }
                dest.options.add(new Option(src.options[i].text,src.options[i].value));
            }
            src.length = 0;
        },
        createGroup: function (e) {
            this.action = 'create';
            //创建主机群组按钮时触发
            var new_group = this.$el.find("[name=group_name]").val();
            var hosts_list = this.$el.find("[name=host_set]");
            var hosts_id = [];
            for(var i=0;i<hosts_list[0].length;i++){hosts_id.push(hosts_list[0][i].value)}
            this.collection.fetchData(true, {"hosts_id": JSON.stringify(hosts_id), "group_name": new_group});
            this.addToMenu = true;
            this.initFormPage(e);
            this.showCreatePage();
        },
        modifyGroup: function (e) {
            this.action = 'modify';
            //修改主机群组时触发
            var new_group = this.$el.find("[name=group_name]").val();
            var group_id = this.$el.find("#host_set").attr("data-group-id");
            var hosts_list = this.$el.find("[name=host_set]");
            var hosts_id = [];
            for(var i=0;i<hosts_list[0].length;i++){hosts_id.push(hosts_list[0][i].value)}
            this.collection.fetchData(true, {"hosts_id": JSON.stringify(hosts_id), "group_name": new_group, "group_id": group_id, "modify": true});
            this.initFormPage(e);
            this.quitCreatePage(e);
        },
        delGroup: function (e) {
            this.action = 'delete';
            var self = this;
            swal(
                {
                    title: "确定删除该主机组？",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: false
                },
                function(){
                    var del_group = self.$el.find("[name=group_name]").val();
                    var group_id = self.$el.find("#host_set").attr("data-group-id");
                    self.collection.fetchData(true, {"group_id": group_id, "group_name": del_group, "delete": true});
                    self.initFormPage(e);
                    self.quitCreatePage(e);
                }
                );
        },
        showCreatePage: function (e) {
            this.$el.find(".div_create_group").toggleClass("hide");
            this.$el.find(".div_show_group").toggleClass("hide");
        },
        initFormPage: function (e) {
            //初始化表单控件
            this.$el.find("[name=group_name]").val("");
            document.getElementById('host_set').length = 0;
        },
        quitCreatePage: function (e) {
            this.$el.find("#group_id").trigger("mychange");
            this.$el.find("#del_group").addClass("hide");
            this.showCreatePage(e);
            this.$el.find("#modify_group").html("创建主机群组").attr("id", "create_group");
            this.initFormPage(e)
        },
        showModifyPage: function (e) {
            var group_target = e.currentTarget;
            var group_name = group_target.innerText;
            var group_id = group_target.attributes['data-group-id'].value;
            this.$el.find("[name=group_name]").val(group_name);
            var hosts = $(group_target).parents("td").siblings().find("a");
            //重置多选框
            document.getElementById('host_set').length = 0;
            this.$el.find("#host_set").attr("data-group-id", group_id);
            this.$el.find("#del_group").removeClass("hide");
            for(var h=0; h<hosts.length; h++){
                var host_id = hosts[h].attributes['data-host-id'].value;
                var host_name = hosts[h].innerText;
                $("#host_set").append("<option value='"+ host_id +"'>"+ host_name +"</option>")
            }
            var dest = document.getElementById("host_set");
            if(dest){
                var src = document.getElementById("host_id");
                for(var j=0; j < dest.length; j++){
                    for(var i=0;i < src.length; i++){
                        if(src.options[i].value == dest.options[j].value){
                            src.options.remove(i);
                        }
                    }
                }
            }
            this.$el.find("#create_group").html("修改主机群组").attr("id", "modify_group");
            this.showCreatePage()
        }
    });
    return ConfigHostGroupsView;

});