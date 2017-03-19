/**
 * Created by zhanghai on 2016/9/19.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var Backbone = require('backbone');
    var NetworkItemView = require("./cmdb_ip_management_item_view").NetworkItemView;
    var IPDetailItemView = require("./cmdb_ip_detail_item_view").IPDetailItemView;
    var CMDBPaginationView = require("./cmdb_pagination_view").PaginationView;
    var IPTreeItemView = require("./cmdb_ip_tree_item_view").IPTreeItemView;
    var CreateSubnetItemView = require("./cmdb_partition_subnet_item_view").CreateSubnetItemView;


    var CMDBView = Backbone.View.extend({
        events: {
            "click #search-ip": "searchIP",
            "click #search-subnet": "searchSubnet",
            "click .paginate_button": "changePage",
            "click #btn-modify-subnet": "modifySubnet",
            "click #btn-partition-subnet": "partitionSubnet",
            "click #btn-allocate-ip": "allocateIP",
            "click #btn-modify-ip": "modifyIP",
            "click #create-subnet": "initCreateSubnet",
            "click #create-subnet-submit": "createSubnet",
            "click #btn-export-ip": "exportIP",
            "keyup #counts": "checkSubnetCount",
            "blur #ipaddr": "checkIPAddress",
            "change .ip-status": "statusFilter"
        },
        initialize: function (options) {
            this.page = 1;
            this.canFetch = false;
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'all', this.render);
            this.listenTo(this.collection, 'reset', this.paginator);

            this.ip_id = "";
            var request_data = {
                page: this.page,
                ip_id: this.ip_id,
                method: "cmdb.ipmanagement.info",
            };
            this.collection.fetchData(true, request_data);
        },
        refreshData: function () {
            //数据刷新

            var ref = $("#ip-treeview").jstree(true),
                sel = $('#ip-treeview').jstree('get_selected');
            if(sel.length){
                var selected_node = ref.get_node(sel);
                var selected_node_id = selected_node.id;
                var node_ids = selected_node_id.split("-");
                var datacenter_id = node_ids[0];
                var has_ip_id = node_ids.length>1;
                var ip_id = has_ip_id?node_ids[1]:"";
            }else{
                var datacenter_id = "";
                var ip_id = "";
            }
            var request_data = {
                page: this.page,
                ip_id: ip_id,
                datacenter_id: datacenter_id,
                method: "cmdb.ipmanagement.info",
            };
            this.collection.fetchData(false, request_data, {async:false});
        },
        addAll: function () {
            //this.$el.find("#ip-treeview").html('');
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var ip_config_model = model.toJSON(),
                ip_tree = ip_config_model.ip_tree;
                ip_design = ip_config_model.ip_design;
                ip_allocate = ip_config_model.ip_allocate;
            this.appendIPTree(ip_tree);
            this.loadIPDesign(ip_design);
            this.loadIPDetail(ip_allocate);

        },
        loadIPDetail: function (ip_allocate) {
            //加载IP列表
            var self = this;
            $("#ip-detail").empty();
            if(ip_allocate){
                $.each(ip_allocate.record, function (index, record) {
                    record["number"] = index+1;
                    var view = new IPDetailItemView({model:self.model, record: record, collection: self.collection});
                    $("#ip-detail").append(view.render().el);
                })
            }
        },
        appendIPTree: function (ip_tree) {
            //加载ip树
            var self = this,
                initial_data = [];

            $.each(ip_tree, function (index, record) {
                root_data = {
                    "id": record.datacenter_id,
                    "datacenter": record.datacenter,
                    "text": record.datacenter,
                    "children": [],
                    'state': {
                        'opened': false,
                        'selected': false
                    },
                    "icon":false,
                };
                var children = [];
                $.each(record.ip, function (index, ip) {
                    children.push({
                        "id": ip.datacenter_id.toString()+"-"+ip.id.toString(),
                        "text": ip.ip,
                        "datacenter": ip.datacenter,
                        'state': {
                            'opened': false,
                            'selected': false
                        },
                        "icon": false,
                    });
                });
                root_data["children"] = children;
                initial_data.push(root_data);
            })

            $('#ip-treeview').on("select_node.jstree", function (event, data) {
                console.log("data:", data)
                if ("node" in data) {
                    if (data.node.parent == "#" && isNaN(data.node.id)) {
                        var ip_id = ""
                    } else {
                        var node_ids = data.node.id.split("-");
                        var datacenter_id = node_ids[0];
                        var has_ip_id = node_ids.length>1;
                        var ip_id = has_ip_id?node_ids[1]:"";
                    }

                    var request_data = {
                        page: 1,
                        datacenter_id: datacenter_id,
                        ip_id: ip_id,
                        method: "cmdb.ipmanagement.info",
                    };
                    self.collection.url = "/api/v1/afcat/";
                    self.collection.fetchData(false, request_data, {
                        async: false, success: function (model,  collection, response) {
                            var resdata = response.data;
                            // $.each(ip_config_model.ip_design.record, function (index, record) {
                            //     var view = new NetworkItemView({model:self.model, record: record, collection: self.collection});
                            //     $("#ip-config").append(view.render().el);
                            // });
                            self.loadIPDesign(resdata.ip_design)

                            // $.each(ip_config_model.ip_allocate.record, function (index, record) {
                            //     record["number"] = index+1;
                            //     var view = new IPDetailItemView({model:self.model, record: record, collection: self.collection});
                            //     $("#ip-detail").append(view.render().el);
                            // })
                            self.loadIPDetail(resdata.ip_allocate);

                            // $("#subnet-pagination").html("");
                            // if ("record" in ip_config_model.ip_design) {
                            //     var view = new CMDBPaginationView({model: ip_config_model.ip_design});
                            //     $("#subnet-pagination").append(view.render().el);
                            // }
                            //
                            // $("#ip-pagination").html("");
                            // if ("record" in ip_config_model.ip_allocate) {
                            //     var view = new CMDBPaginationView({model: ip_config_model.ip_allocate});
                            //     $("#ip-pagination").append(view.render().el);
                            // }
                            self.paginator(collection);

                            var ref = $("#ip-treeview").jstree(true),
                                sel = $('#ip-treeview').jstree('get_selected');
                            if(!sel.length){
                                return false;
                            }
                            //删除子节点,重新加载
                            var selected_node = ref.get_node(sel);
                            ref.delete_node(selected_node.children);
                            $("#datacenter-title").html("<h4>"+ selected_node.original.datacenter +"</h4>")
                            $.each(resdata.ip_tree, function (index, record) {
                                if(record.ip instanceof Array){
                                    if(selected_node.id == record.datacenter_id){
                                        $.each(record.ip, function (index, ip) {
                                            var newNode = { state: "open", id:(record.datacenter_id).toString()+"-"+(ip.id).toString(), datacenter:ip.datacenter, text:ip.ip, icon:false };
                                            $('#ip-treeview').jstree("create_node", sel, newNode, "last");
                                        });
                                    }
                                }else{
                                    var newNode = { state: "open", id:(record.datacenter_id).toString()+"-"+(record.id).toString(), datacenter:record.datacenter, text:record.ip, icon:false };
                                    $('#ip-treeview').jstree("create_node", sel, newNode, "last");
                                    //$('#ip-treeview').jstree().create_node(sel, newNode);
                                }

                            })

                        }
                    });

                }

            }).jstree({
                "plugins": [
                    "types", "dnd", "sort", "state"
                ],
                "core": {
                    "plugins": [
                        "wholerow"
                    ],
                    'check_callback': true,
                    'state': {
                        'opened': false,
                        'selected': false
                    },
                    "data": initial_data,
                    "types": {
                        "default" : {
                            "icon" : false  // 关闭默认图标
                        },
                    }
                }
            });
        },
        loadIPDesign: function (ip_design) {
            //加载IP/子网列表
            var self = this;
            $("#ip-config").html("");
            if (ip_design) {
                $.each(ip_design.record, function (index, record) {
                    var view = new NetworkItemView({model:self.model, record: record, collection: self.collection});
                    $("#ip-config").append(view.render().el);
                })
            }
        },
        allocateIP: function (e) {
            //分配IP

            var request_data = {
                "action": "new",
                "type": "ip",
                },
                form_data = $("#allocateIPForm").serializeArray(),
                value_data = {},
                self = this;

            $.each(form_data, function (index, content) {
                value_data[content["name"]] = content["value"];
            });

            var startip = value_data.startip;
            var endip = value_data.endip;

            if(!self.IPValid(startip)){
                self.err_message("startip", "IP不合法！");
                return false;
            }

            if(!self.IPValid(endip)){
                self.err_message("endip", "IP不合法！");
                return false;
            }

            request_data["value"] = value_data;
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, {data: JSON.stringify(request_data), method: "cmdb.ipmanagement.allocation"}, {
                type: "post", success:function (model, collection, response) {
                    $(".close").click();
                    if(response.status){
                        self.refreshData();
                        var ip_design = self.collection.toJSON()[0].ip_design;
                        var ip_allocate = self.collection.toJSON()[0].ip_allocate;
                        self.loadIPDesign(ip_design);
                        self.loadIPDetail(ip_allocate);
                        self.paginator(self.collection);
                    }
                }});

        },
        partitionSubnet: function (e) {
            //划分子网

            var request_data = {
                "action": "new",
                "type": "subnet",
                },
                form_data = $("#partitionSubnetForm").serializeArray(),
                value_data = {},
                self = this;

            $.each(form_data, function (index, content) {
                if (content["name"] == "ipaddr") {
                    var ip_list = content["value"].split("/");
                    var ipaddress = ip_list[0];
                    var mask = ip_list.length>0?ip_list[1]:"";

                    value_data["ipaddr"] = ipaddress;
                    value_data["maskbits"] = mask;
                } else {
                    value_data[content["name"]] = content["value"];
                }
            });

            var ipaddress = value_data.ipaddr;
            var mask = value_data.maskbits;

            if(!ipaddress || !self.IPValid(ipaddress)){
                var errmsg = "请填写有效IP！"
                self.err_message("ipaddr", errmsg);
                return false;
            }

            if(!mask || isNaN(mask) || !self.maskValid(mask)){
                var errmsg = "请填写有效掩码！"
                self.err_message("ipaddr", errmsg);
                return false;
            }

            var counts = value_data.counts;

            if(!this.subnetCountValid(counts)){
                var errmsg = "划分子网数量有误！";
                this.err_message("counts", errmsg);
                return false;
            }

            request_data["value"] = value_data;
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, {data: JSON.stringify(request_data), method: "cmdb.ipmanagement.allocation"}, {
                type: "post", success:function (model, collection, response) {
                    $(".close").click();
                    if(response.status){
                        self.refreshData();
                        var ip_design = self.collection.toJSON()[0].ip_design;
                        var ip_allocate = self.collection.toJSON()[0].ip_allocate;
                        self.loadIPDesign(ip_design);
                        self.loadIPDetail(ip_allocate);
                        self.paginator(self.collection);
                    }
                }});
        },
        modifyIP: function (e) {
            //提交修改IP的请求
            var request_data = {
                "action": "edit",
                "type": "ip",
            };
            var self = this;
            var form_data = $("#IPForm").serializeArray();
            var value_data = {}
            $.each(form_data, function (index, content) {
                value_data[content["name"]] = content["value"];
            })
            request_data["value"] = value_data;
            var initial_url = this.collection.url;
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, {data: JSON.stringify(request_data), method: "cmdb.ipmanagement.allocation"}, {
                type: "post", success:function (model, collection, response) {
                    $(".close").click();
                    if(response.status){
                        self.refreshData();
                        var ip_design = self.collection.toJSON()[0].ip_design;
                        var ip_allocate = self.collection.toJSON()[0].ip_allocate;
                        self.loadIPDesign(ip_design);
                        self.loadIPDetail(ip_allocate);
                        self.paginator(self.collection);
                    }
                }});
            this.collection.url = initial_url;
        },
        modifySubnet: function (e) {
            //修改IP或子网
            // 样例：
            // var request_data = {
            //     "value":{"id":10012,
            //         "ipaddr":"40.0.0.0",
            //         "maskbits":24,
            //         "counts":256,
            //         "netarea_id":10013,
            //         "datacenter_id":10012,
            //         "remark":"xxxx",
            //         "parentip_id":10012,
            //         "vlan": "100-102",
            //         "usefor":""
            //     },
            //    "action":"edit",
            //    "type":"ip"
            // }

            var request_data = {
                "action": "edit",
                "type": "subnet",
            };
            var self = this;
            var form_data = $("#modify-subnet-form").serializeArray();
            var value_data = {};
            $.each(form_data, function (index, content) {
                if (content["name"] == "ipaddr") {
                    var ip_list = content["value"].split("/");
                    var ipaddress = ip_list[0];
                    var mask = ip_list.length>0?ip_list[1]:"";

                    value_data["ipaddr"] = ipaddress;
                    value_data["maskbits"] = mask;
                } else {
                    value_data[content["name"]] = content["value"];
                }
            });

            var ipaddress = value_data.ipaddr;
            var mask = value_data.maskbits;

            if(!ipaddress || !self.IPValid(ipaddress)){
                var errmsg = "请填写有效IP！"
                self.err_message("ipaddr", errmsg);
                return false;
            }

            if(!mask || isNaN(mask) || !self.maskValid(mask)){
                var errmsg = "请填写有效掩码！"
                self.err_message("ipaddr", errmsg);
                return false;
            }

            var counts = value_data.counts;

            if(!this.subnetCountValid(counts)){
                var errmsg = "子网数量有误！";
                this.err_message("counts", errmsg);
                return false;
            }

            var allocated_count = $("#allocated-count").val();
            if(parseInt(value_data.counts) < parseInt(allocated_count)){
                var errmsg = "子网总数不能小于已分配子网数量！";
                this.err_message("counts", errmsg);
                return false;
            }

            request_data["value"] = value_data;
            var initial_url = this.collection.url;
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, {data: JSON.stringify(request_data), method: "cmdb.ipmanagement.allocation"}, {
                type: "post", success:function (model, collection, response) {
                    $(".close").click();
                    if(response.status){
                        self.refreshData();
                        var ip_design = self.collection.toJSON()[0].ip_design;
                        var ip_allocate = self.collection.toJSON()[0].ip_allocate;
                        self.loadIPDesign(ip_design);
                        self.loadIPDetail(ip_allocate);
                        self.paginator(self.collection);
                    }
                }});
            this.collection.url = initial_url;
        },
        searchSubnet: function (e) {
            //搜索网络
            var search_value = $('#subnet-value').val();
            var formData = {method: "cmdb.ipmanagement.subnet_info", page: 1, "condition": search_value};
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, formData, {async:false});
            var ip_subnet = this.collection.toJSON()[0];
            var self = this;
            $("#ip-config").html("");
            $.each(ip_subnet.record, function (index, record) {
                record["number"] = index+1;
                var view = new NetworkItemView({model:self.model, record: record, collection: self.collection});
                $("#ip-config").append(view.render().el);
            });

            $("#subnet-pagination").html("");
            if ("record" in ip_subnet) {
                var view = new CMDBPaginationView({model: ip_subnet});
                $("#subnet-pagination").append(view.render().el);
            }
        },
        searchIP: function (e) {
            //搜索IP
            var search_value = $('#ip-value').val();
            var formData = {method: "cmdb.ipmanagement.ipinfo", page: 1, "condition": search_value};
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, formData, {async:false});
            var ip_allocate = this.collection.toJSON()[0];
            var self = this;
            $("#ip-detail").html("");
            $.each(ip_allocate.record, function (index, record) {
                record["number"] = index+1;
                var view = new IPDetailItemView({model:self.model, record: record, collection: self.collection});
                $("#ip-detail").append(view.render().el);
            });

            $("#ip-pagination").html("");
            if ("record" in ip_allocate) {
                var view = new CMDBPaginationView({model: ip_allocate});
                $("#ip-pagination").append(view.render().el);
            }
        },
        paginator: function (model) {
            //页面分页
            var ip_design = model.toJSON()[0].ip_design;
            var ip_allocate = model.toJSON()[0].ip_allocate;
            $("#subnet-pagination").html("");
            if("record" in ip_design){
                var ip_design_view = new CMDBPaginationView({model: ip_design});
                $("#subnet-pagination").append(ip_design_view.render().el);
            }

            $("#ip-pagination").html("");
            if("record" in ip_allocate){
                var ip_allocate_view = new CMDBPaginationView({model: ip_allocate});
                $("#ip-pagination").append(ip_allocate_view.render().el);
            }
        },
        changePage: function (e) {
            //切换分页
            var curr_page = e.currentTarget.id;
            var tabIndex = $("#ip-manage-tabs").find("li.active").attr("id");
            var selected_node_id = $('#ip-treeview').jstree('get_selected')[0];
            if(selected_node_id){
                var node_index_ids = selected_node_id.split("-");
                var has_ip_id = node_index_ids.length>1
                var ip_id = has_ip_id?node_index_ids[1]:"";
                var datacenter_id = node_index_ids[0];
            }else{
                var ip_id = "";
                var datacenter_id = "";
            }

            var search_value = $('#subnet-value').val();

            var request_data = {
                page: curr_page,
                ip_id: ip_id,
                datacenter_id: datacenter_id,
                method: "cmdb.ipmanagement.info",
            };
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, request_data, {async:false});
            var ip_subnet = this.collection.toJSON()[0].ip_design;
            var ip_allocate = this.collection.toJSON()[0].ip_allocate;
            var self = this;
            var num_page = 15;

            if(tabIndex === "li-subnet"){
                $("#ip-config").html("");
                $.each(ip_subnet.record, function (index, record) {
                    record["number"] = (curr_page-1)*num_page+index+1;
                    var view = new NetworkItemView({model:self.model, record: record, collection: self.collection});
                    $("#ip-config").append(view.render().el);
                });
            }else{
                $("#ip-detail").html("");
                request_data["condition"] = search_value;
                $.each(ip_allocate.record, function (index, record) {
                    record["number"] = (curr_page-1)*num_page+index+1;
                    var view = new IPDetailItemView({model:self.model, record: record, collection: self.collection});
                    $("#ip-detail").append(view.render().el);
                });
            }
            this.paginator(this.collection);
        },
        initCreateSubnet: function (e) {
            var self = this;
            var request_data = {
                    "tables":["BaseDataCenter","BaseNetArea"]
                };
            var subnet_model = {};

            self.collection.url = "/cmdb/basedata/";
            self.collection.fetchData(false, {data:JSON.stringify(request_data)}, {type:"get", async:false, success: function (model, collection, response) {
                if(response.status){
                    subnet_model["basedatacenter"] = response.data.basedatacenter;
                    subnet_model["basenetarea"] = response.data.basenetarea;
                    $("#partition-subnet").empty();
                    var view = new CreateSubnetItemView({model: subnet_model});
                    $("#partition-subnet").append(view.render().el);
                }

            }});

            self.collection.url = "/api/v1/afcat/";
        },
        createSubnet: function (e) {
            //提交新建网络表单
            var request_data = {
                "action": "new",
                "type": "subnet",
                },
                form_data = $("#createSubnetForm").serializeArray(),
                value_data = {},
                self = this;

            $.each(form_data, function (index, content) {
                if (content["name"] == "ipaddr") {
                    var ip_list = content["value"].split("/");
                    var ipaddress = ip_list[0];
                    var mask = ip_list.length>0?ip_list[1]:"";

                    value_data["ipaddr"] = ipaddress;
                    value_data["maskbits"] = mask;
                } else {
                    value_data[content["name"]] = content["value"];
                }
            });

            var ipaddress = value_data.ipaddr;
            var mask = value_data.maskbits;

            if(!ipaddress || !self.IPValid(ipaddress)){
                var errmsg = "请填写有效IP！"
                self.err_message("ipaddr", errmsg);
                return false;
            }

            if(!mask || isNaN(mask) || !self.maskValid(mask)){
                var errmsg = "请填写有效掩码！"
                self.err_message("ipaddr", errmsg);
                return false;
            }

            var counts = value_data.counts;

            if(!this.subnetCountValid(counts)){
                var errmsg = "子网数量有误！";
                this.err_message("counts", errmsg);
                return false;
            }

            request_data["value"] = value_data;
            self.collection.url = "/api/v1/afcat/";
            self.collection.fetchData(false, {data: JSON.stringify(request_data), method: "cmdb.ipmanagement.allocation"}, {
                async:false, type: "post", success:function (model, collection, response) {
                    $(".close").click();
                    if(response.status){
                        self.refreshData();
                        var ip_design = self.collection.toJSON()[0].ip_design;
                        var ip_allocate = self.collection.toJSON()[0].ip_allocate;
                        self.loadIPDesign(ip_design);
                        self.loadIPDetail(ip_allocate);
                        self.paginator(self.collection);
                    }

                }});
        },
        subnetCountValid: function (count) {
            //子网数量合法性检查
            var count_is_valid = count>0&&count<257?true:false;
            return count_is_valid;
        },
        err_message: function (dom_id, err_msg) {
            //错误提示
            $("#" + dom_id).css("border", "1px solid red");
            $("#error-message").html("<b>" + err_msg + "</b>");
            $("#error-message").css("color", "red");
            setTimeout(function () {
                $("#error-message").text("");
                $("#" + dom_id).css("border", "");
            }, 3000);
            return false;
        },
        checkSubnetCount: function (evt) {
            //子网分配数量有效性检查
            var subnet_count = evt.currentTarget.value;
            if(!this.subnetCountValid(subnet_count)){
                var errmsg = "子网数量有误！";
                this.err_message("counts", errmsg);
            }
        },
        checkIPAddress: function (evt) {
            //IP地址有效性检查
            var ipaddrstr = evt.currentTarget.value;
            if(ipaddrstr.indexOf("/") == -1){
                var errmsg = "IP地址需要指定掩码！"
                this.err_message("ipaddr", errmsg);
                return false;
            }
            var ip_list = ipaddrstr.split("/");
            var ipaddress = ip_list[0];
            var mask = ip_list[1];
            if(!this.IPValid(ipaddress)){
                var errmsg = "IP地址不合法！";
                this.err_message("ipaddr", errmsg);
                return false;
            }

            if(!this.maskValid(mask)){
                var errmsg = "掩码不合法！";
                this.err_message("ipaddr", errmsg);
                return false;
            }

        },
        maskValid: function (mask) {
            //掩码有效性检验
            if(isNaN(mask) || !mask){
                return false;
            }
            if(mask<0 || mask>30){
                return false;
            }
            return true;
        },
        IPValid: function (value) {
            var ip = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
            var re = RegExp(ip);
            return re.test(value);
        },
        exportIP: function (e) {
            //导出IP
            $("#search-ip-form").submit();
        },
        statusFilter: function (evt) {
            //状态过滤
            var filter_status = evt.currentTarget.value;
            if(!filter_status){
                this.searchIP();
                return;
            }
            var search_value = $('#ip-value').val();
            var formData = {
                method: "cmdb.ipmanagement.ipinfo",
                page: this.page,
                status: filter_status,
                condition: search_value
            };
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.url = "/api/v1/afcat/";
            this.collection.fetchData(false, formData, {async:false});
            var ip_allocate = this.collection.toJSON()[0];
            var self = this;
            $("#ip-detail").html("");
            $.each(ip_allocate.record, function (index, record) {
                record["number"] = index+1;
                var view = new IPDetailItemView({model:self.model, record: record, collection: self.collection});
                $("#ip-detail").append(view.render().el);
            });

            $("#ip-pagination").html("");
            if ("record" in ip_allocate) {
                var view = new CMDBPaginationView({model: ip_allocate});
                $("#ip-pagination").append(view.render().el);
            }
        }

    });

    return CMDBView;
})
