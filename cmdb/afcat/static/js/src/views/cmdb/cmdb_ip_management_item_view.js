/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var NetworkItemViewTemplate = require('text!./templates/cmdb_network_template.tpl');
    var ModifySubnetItemView = require("./cmdb_partition_subnet_item_view").ModifySubnetItemView;
    var SubnetItemView = require("./cmdb_partition_subnet_item_view").SubnetItemView;
    var AllocateIPItemView = require("./cmdb_partition_subnet_item_view").AllocateIPItemView;

    var NetworkItemView = Backbone.View.extend({
        tagName: "tr",
        template: _.template(NetworkItemViewTemplate),
        events: {
            "click .modify-subnet": "initModifySubnet",
            "click .delete-subnet": "deleteSubnet",
            "click .partition-subnet": "initPartitionSubnet",
            "click .allocate-ip": "initAllocateIP",

        },
        initialize: function (options) {
            this.model = options.model;
            this.record = options.record;
            this.collection = options.collection;
            this.listenTo(this.record, 'destroy', this.remove);
        },
        initAllocateIP: function (e) {
            //分配IP

            // 数据结构
            // {"value":{"ipmask_id":10016,
            //            "startip":"40.1.1.4",
            //            "endip":"40.1.1.5",
            //            "status":2,
            //            "allocateto":"资金系统DB",
            //            "vlan":102},
            //   "action": "new",
            //   "type": "ip"
            //   }

            var ip_id = this.record.id,
                allocate_state = {
                    "1":"未分配",
                    "2":"已分配",
                    "3":"已使用",
                    "4":"待回收"
                };

            this.record["status"] = allocate_state;
            self = this;
            $("#allocate-ip").empty();
            var view = new AllocateIPItemView({model: self.record});
            $("#allocate-ip").append(view.render().el);
        },
        initPartitionSubnet: function (e) {
            //划分子网modal加载

            var subnet_model = this.record,
                request_data = {
                    "tables":["BaseDataCenter","BaseNetArea"]
                };

            if(this.record.allocatecount === this.record.counts){
                swal(
                    {
                        title: "",
                        text: this.record.ipaddr+"子网数量不足，请及时扩容！",
                        type: "warning",
                        showCancelButton: false,
                        confirmButtonColor: "#DD6B55",
                        closeOnConfirm: false
                    }
                );
                return;
            }

            this.collection.url = "/cmdb/basedata/";
            this.collection.fetchData(false, {data:JSON.stringify(request_data)}, {type:"get", async:false, success: function (model, collection, response) {
                if(response.status){
                    subnet_model["basedatacenter"] = response.data.basedatacenter;
                    subnet_model["basenetarea"] = response.data.basenetarea;
                    $("#partition-subnet").empty();
                    var view = new SubnetItemView({model: subnet_model});
                    $("#partition-subnet").append(view.render().el);
                    var original_datacenter_id = subnet_model.datacenter_id;
                    var original_netarea_id = subnet_model.netarea_id;
                    var datacenter_select_obj = $("#partitionSubnetForm").find("select[name='datacenter_id']");
                    var netarea_select_obj = $("#partitionSubnetForm").find("select[name='netarea_id']");
                    datacenter_select_obj.val(original_datacenter_id);
                    netarea_select_obj.val(original_netarea_id);
                }
            }});

        },
        deleteSubnet: function (e) {
            //删除IP或子网
            var ip_id = this.record.id,
                self = this;

            self.collection.url = "/api/v1/afcat/";
            swal(
                {
                    title: "确定删除该IP/网络？",
                    text: "删除后将无法恢复！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    cancelButtonText: '取消',
                    confirmButtonText: "删除",
                    closeOnConfirm: true
                },
                function(){
                    var request_data = {
                        "value":{"id":ip_id},
                        "action":"delete",
                        "type":"subnet",

                    };
                    swal.setDefaults({closeOnConfirm:false});
                    self.collection.fetchData(false, {data: JSON.stringify(request_data), method: "cmdb.ipmanagement.allocation", success:function (model, collection, response) {
                        window.location.href = "/cmdb/cmdb_ip_management/list/";
                    }});

               }
            );
        },
        initModifySubnet: function (e) {
            //修改子网
            var request_data = {
                "tables":["BaseDataCenter","BaseNetArea"]
            };
            var ip_model = this.record;
            var self = this;
            self.collection.url = "/cmdb/basedata/";
            self.collection.fetchData(false, {data:JSON.stringify(request_data)}, {type:"get", async:false, success: function (model, collection, response) {
                if(response.status){
                    ip_model["basedatacenter"] = response.data.basedatacenter;
                    ip_model["basenetarea"] = response.data.basenetarea;
                    $("#modify-ip-config").empty();
                    var view = new ModifySubnetItemView({model: ip_model});
                    $("#modify-ip-config").append(view.render().el);
                    var original_datacenter_id = ip_model.datacenter_id;
                    var original_netarea_id = ip_model.netarea_id;
                    var datacenter_select_obj = $("#modify-subnet-form").find("select[name='datacenter_id']");
                    var netarea_select_obj = $("#modify-subnet-form").find("select[name='netarea_id']");
                    datacenter_select_obj.val(original_datacenter_id);
                    netarea_select_obj.val(original_netarea_id);
                }
            }});
            self.collection.url = "/api/v1/afcat/";
        },
        render: function () {
            // console.log("model:", this.record)
            this.$el.html(this.template(this.record));
            return this;
        }
    });

    return {
        NetworkItemView: NetworkItemView,
    };
})