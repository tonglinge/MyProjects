/**
 * Created by super on 2017/2/9.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require("backbone");
    var BalanceMappingItemView = require("./cmdb_lbmapping_item_view").BalanceMappingItemView;
    var BalanceMappingDetailView = require("./cmdb_lbmapping_item_view").BalanceMappingDetailItemView;
    var BalanceMappingEditView = require("./cmdb_lbmapping_item_view").BalanceMappingEditItemView;
    var CMDBPaginationView = require("./cmdb_pagination_view").PaginationView;

    var BalanceMappingView = Backbone.View.extend({
        events: {
            "click #search_submit": "search_info",
            "click .paginate_button": "changePage",
            "click .btn-info-delete": "delete",
            "click .btn-info-detail": "detail",
            "click .btn-info-edit": "edit",
            "click .btn-info-clone": "clone",
            "click #btn-new": "add",
            "click #save-and-add": "save_and_new",
            "click #save-and-back": "save_and_back",
            "click #export_file": "exportExcel"

        },
        initialize: function (options) {
            this.collection.url = options.url;
            this.record_data = "undefined";
            // this.collection.url = "/cmdb/basedata";
            this.model = options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'reset', this.paginator);
            this.collection.fetchData(true, {method: 'cmdb.balancemapping.info'});
        },
        addAll: function () {
            var models = this.collection.models;
            //针对每次reload数据时需要清空整个app页面数据，指定判断关键属性，用来决定是否对app内容清空
            this.$el.find(".lbmapping-body").html("");
            this.collection.each(this.addOne, this);

        },
        addOne: function (model) {
            var data = model.toJSON();
            var record = data.record;
            var self = this;
            this.record_data = record;
            $.each(record, function (index, obj) {
                var view = new BalanceMappingItemView({model: obj});
                self.$el.find(".lbmapping-body").append(view.render().el);
            });
        },
        //页面分页
        paginator: function (model) {
            var view = new CMDBPaginationView({model: model});
            $("#pagination").html(view.render().el);
        },
        changePage: function (e) {
            //切换分页
            this.$el.find(".lbmapping-body").html('');
            var curr_page = e.currentTarget.id;
            var _condition = $("#search_value").val();
            var formData = {"page": curr_page, "method": 'cmdb.balancemapping.info'};
            if (_condition) {
                formData["condition"] = _condition;
            }
            this.collection.fetchData(true, formData);
        },

        //按条件过滤
        search_info: function () {
            var _condition = $("#search_value").val();
            this.collection.fetchData(true, {method: 'cmdb.balancemapping.info', condition: _condition})
        },

        //删除记录
        delete: function (e) {
            var record_id = $(e.currentTarget).parent().attr("rid");
            var _collection = this.collection;
            var self = this;
            swal({
                    title: "删除确认",
                    text: "删除后将无法恢复,确认删除吗?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonText: "确认",
                    cancelButtonText: "取消",
                    closeOnConfirm: true,
                    closeOnCancel: true
                },
                function (isConfirm) {
                    if (isConfirm) {
                        _collection.fetchData(false, {
                                data: JSON.stringify({value: {"id": record_id}, action: "delete"}),
                                method: "cmdb.balancemapping.operate"
                            },
                            {
                                success: self.afterdelete(e),
                                type: "post"
                            }
                        )
                    }
                });
        },
        afterdelete: function (e) {
            $(e.currentTarget).parent().parent().remove();
        },

        // 查看详情
        detail: function (e) {
            //var data = this.collection.models[0].toJSON();
            //var record = data.record;
            var record = this.record_data;
            var self = this;
            var curr_id = $(e.currentTarget).parent().attr("rid");
            self.$el.find(".modal-body").find(".table").html("");
            $.each(record, function (index, obj) {
                if (obj.id == curr_id) {
                    var view = new BalanceMappingDetailView({model: obj});
                    $("#myModalLabel").html("配置详情");
                    self.$el.find(".modal-body").find(".table").append(view.render().el);
                    return false;
                }
            });
            $("#Modal").modal();
        },
        add: function (e) {
            $(e).attr("action", "new");
            this.showform(e);
        },
        //打开新添加记录页面e
        showform: function (e, record) {
            console.log("add function", e, record);
            //载入combox插件
            require("bootstrap_combox");
            // 获取基表数据
            this.reseted = true;
            var origization_url = this.collection.url;   // 保存之前的url
            this.collection.url = "/cmdb/basedata";  // 新请求数据的url
            var self = this;
            this.collection.fetchData(false,
                {data: JSON.stringify({"tables": ["BaseDataCenter", "BaseNetArea", "BaseBalanceType", "Projects", "Business"]})},
                {
                    success: function (collection, response, options) {
                        var models = response.toJSON();
                        var editview = new BalanceMappingEditView({model: models[0]});
                        // 将内容清空
                        $("#edit-info").find(".lb-edit-table").html("");
                        $("#edit-info").find(".lb-edit-table").html(editview.render().el);
                        //显示编辑模板
                        $("#list-info").hide();
                        $("#edit-info").fadeIn("slow");
                        $("#edit-info").delegate("#nosave-back", "click", function () {
                            self.hideform();
                        });
                        //给网络区域绑定change事件,填充设备
                        $("#edit-info").delegate("#netarea", "change", function (e) {
                            self.loadequipment();
                        });
                        //加载系统下拉框
                        self.initcombox(models[0].projects, models[0].business);

                        // 是否加载数据，编辑的时候填充数据
                        if (record != undefined) {
                            self.edit_fill(record, models[0])
                        }
                        // 设置当前操作属性
                        $("#action").attr("action", $(e).attr("action"));
                    }
                });

            this.collection.url = origization_url;
        },
        edit: function (e) {
            $(e).attr("action", "edit");
            this.load_data(e);
        },
        clone: function (e) {
            $(e).attr("action", "new");
            this.load_data(e);
        },
        // 获取当前行的编辑数据
        load_data: function (e) {
            var self = this;
            var record_id = $(e.currentTarget).parent().attr("rid");
            var record_objs = this.record_data;
            $(record_objs).each(function (index, obj) {
                if (obj.id == record_id) {
                    self.showform(e, obj);
                    return false;
                }
            });
        },
        //返回主页面
        hideform: function () {
            $("#edit-info").find(".lb-edit-table").html("");
            $("#edit-info").hide();
            $("#list-info").fadeIn("slow");
            // this.collection.fetchData(true, {method: 'cmdb.balancemapping.info'});
        },

        //加载所属区域的设备信息
        loadequipment: function (selected_id) {
            var netarea_id = $("#netarea option:selected").val();
            if (parseInt(netarea_id) > 0) {
                this.collection.fetchData(false, {
                    data: JSON.stringify({value: {"netarea_id": netarea_id}, action: "loadequipment"}),
                    method: "cmdb.balancemapping.operate"
                }, {
                    success: function (collection, response, options) {
                        var models = response.toJSON();
                        //渲染页面的option
                        $("#equipment").html("");
                        _.each(models, function (obj) {
                            if (obj.id == selected_id) {
                                option = "<option value='" + obj.id + "' selected>" + obj.name + "</option>";
                            } else {
                                option = "<option value='" + obj.id + "'>" + obj.name + "</option>";
                            }
                            $("#equipment").append(option);
                        })

                    }
                })
            }
        },

        // 初始化系统选择框
        initcombox: function (project_data, business_data) {
            var self = this;
            var show_data = Array();
            $(project_data).each(function (index, obj) {
                show_data[index] = {'id': obj.id, 'name': obj.sysname};
            });
            var testdataBsSuggest = $("#combox-project").bsSuggest({
                indexId: 0,  //data.value 的第几个数据，作为input输入框的内容
                indexKey: 1, //data.value 的第几个数据，作为input输入框的内容
                showBtn: true,
                data: {'value': show_data}
            }).on('onSetSelectValue', function (e, keyword, data) {
                self.loadbusiness(data, business_data);
            })
        },

        //加载所选系统下的所有业务模块
        loadbusiness: function (chooseobj, business_data) {
            $("#business").html("");
            $(business_data).each(function (index, obj) {
                if (obj.project_id == chooseobj.id) {
                    $("#business").append("<option value='" + obj.id + "'>" + obj.bussname + "</option>");
                }
            })

        },

        // 保存并新增
        save_and_new: function () {
            var action = $("#action").attr("action");
            this.save_data(action, "new");
        },
        // 保存并返回
        save_and_back: function () {
            var action = $("#action").attr("action");
            this.save_data(action, "back");
        },
        // 保存数据
        save_data: function (action, success_action) {
            var vsname = $("#vsname").val().trim();
            var vsaddr = $("#vsaddr").val().trim();
            var port = $("#port").val().trim();
            var dnsdomain = $("#dnsdomain").val().trim();
            var datacenter_id = $("#datacenter").val();
            var netarea_id = $("#netarea option:selected").val();
            var project_id = $("#combox-project").attr("data-id");
            var business_id = $("#business").val();
            var snataddr = $("#snataddr").val().trim().replace(RegExp('\n', 'g'), ',');
            var pooladdr = $("#pooladdr").val().trim().replace(RegExp('\n', 'g'), ',');
            var equipment_id = $("#equipment option:selected").val();
            var hosttype = $("#hosttype").val().trim();
            var hostname = $("#hostname").val().trim();
            var vlan = $("#vlan").val().trim();
            var ploy = $("#ploy").val();
            var remark = $("#remark").val().trim();
            var self = this;
            // 验证合法性
            if (vsname.length == 0) {
                return this.err_message("vsname", "请填写vs名称!");
            } else {
                $("#vsname").css("border", "1px solid #ccc")
            }
            if (vsaddr.length == 0) {
                return this.err_message("vsaddr", "请填写vs地址!");
            } else {
                if (!this.ipcheck(vsaddr)) {
                    return this.err_message("vsaddr", "vs地址不合法!");
                } else {
                    $("#vsaddr").css("border", "1px solid #ccc");
                }
            }
            if (port.length == 0) {
                return this.err_message("port", "请填写端口!");
            } else {
                $("#port").css("border", "1px solid #ccc")
            }
            if (parseInt(netarea_id) == 0) {
                return this.err_message("netarea", "请选择网络区域!")
            } else {
                $("#netarea").css("border", "1px solid #ccc")
            }
            if (snataddr.length == 0) {
                return this.err_message("snataddr", "请填写SNAT地址池!")
            } else {
                $(snataddr.split(',')).each(function (index, ip) {
                    if(!self.ipcheck(ip)){
                        return self.err_message("snataddr","SNAT地址池包含非法IP")
                    }
                });
                $("#snataddr").css("border", "1px solid #ccc")
            }
            if (pooladdr.length == 0) {
                return this.err_message("pooladdr", "请填写服务器地址池!")
            } else {
                $(pooladdr.split(',')).each(function (index, ip) {
                    if(!self.ipcheck(ip)){
                        return self.err_message("pooladdr","服务器地址池包含非法IP")
                    }
                });
                $("#pooladdr").css("border", "1px solid #ccc")
            }
            if (business_id == null){
                return this.err_message("business", "请选择业务模块!")
            }else{
                $("#business").css("border", "1px solid #ccc")
            }
            // console.log(vsname, vsaddr, port, dnsdomain, datacenter_id, 'netareaid', netarea_id, project_id, equipment_id);
            // console.log(business_id, snataddr, pooladdr, hosttype, hostname, vlan, remark);
            //提交后台
            var post_data = {
                "vsname": vsname,
                "vsaddr": vsaddr,
                "port": port,
                "dnsdomain": dnsdomain,
                "datacenter_id": datacenter_id,
                "netarea_id": netarea_id,
                "project_id": project_id,
                "business": business_id.join(","),
                "snataddr": snataddr,
                "pooladdr": pooladdr,
                "equipment_id": equipment_id,
                "hosttype": hosttype,
                "hostname": hostname,
                "vlan": vlan,
                "ploy_id": ploy,
                "remark": remark
            };

            if (action == "edit") {
                post_data["id"] = $("#action").attr("data-id");
            }
            // console.log("post_data:", post_data);
            this.collection.fetchData(false, {
                data: JSON.stringify({value: post_data, action: action}),
                method: "cmdb.balancemapping.operate",
            }, {
                success: function (collection, response, options) {
                    if (success_action == "new") {
                        // console.log("response back", response, options);
                        if (options.status) {
                            self.new_after_save();
                        }
                    }
                    if (success_action == "back") {
                        self.hideform();
                        self.collection.fetchData(true, {method: 'cmdb.balancemapping.info'});
                    }
                }, type: "post"
            })
        },
        err_message: function (dom_id, err_msg) {
            $("#" + dom_id).css("border", "1px solid red");
            $("#error-message").html("<b>" + err_msg + "</b>");
            $("#error-message").css("color", "red");
            setTimeout(function () {
                $("#error-message").text("");
            }, 3000);
            return false;
        },

        // 保存完后新增时清空数据
        new_after_save: function () {
            $("#vsname").val("");
            $("#vsaddr").val("");
            $("#port").val("");
            $("#dnsdomain").val("");
            $("#datacenter").val("0");
            $("#snataddr").val("");
            $("#pooladdr").val("");
            $("#hosttype").val("");
            $("#hostname").val("");
            $("#vlan").val("");
            $("#remark").val("");
        },
        // 编辑时填充页面
        edit_fill: function (obj, base_data) {
            $("#vsname").val(obj.vsname);
            $("#vsaddr").val(obj.vsaddr);
            $("#port").val(obj.port);
            $("#dnsdomain").val(obj.dnsdomain);
            $("#datacenter").val(obj.datacenter_id);
            $("#netarea").val(obj.netarea_id);
            $("#snataddr").val(obj.snataddr.replace(RegExp(',', 'g'), '\n'));
            $("#pooladdr").val(obj.pooladdr.replace(RegExp(',', 'g'), '\n'));
            $("#hosttype").val(obj.hosttype);
            $("#hostname").val(obj.hostname);
            $("#vlan").val(obj.vlan);
            $("#remark").val(obj.remark);

            $("#combox-project").attr("data-id", obj.project_id);
            $("#combox-project").val(obj.project);
            this.loadequipment(obj.equipment_id);
            // 加载指定系统的业务模块
            this.loadbusiness({id: obj.project_id}, base_data.business);
            // 选中业务模块
            var bussid = obj.business_id.split(",");
            $("#business").val(bussid);

            $("#action").attr("data-id", obj.id);
        },
        exportExcel: function () {
            $("#search-form").submit();
        },
        ipcheck: function (value) {
            var ip = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
            var re = RegExp(ip);
            return re.test(value)
        }

    });

    return BalanceMappingView;
});