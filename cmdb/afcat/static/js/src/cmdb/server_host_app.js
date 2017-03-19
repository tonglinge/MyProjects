/**
 * Created by zhanghai on 2016/9/18.
 */

define(function (require, exports, module) {
    var $ = require('jquery');
    //启动app入口点

    require("datetimepicker");

    //导入CMDB模型
    var CMDBModel = require('../models/cmdb/cmdb_model');

    //导入集合
    var CMDBCollection = require('../collections/cmdb/cmdb_collection');

    //实例化APP, 服务器资产app
    var ServerHostApp = function (element, options) {
        options.model = CMDBModel.HostModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_server_host_list_view'], function (ServerHostView) {
            var serverHostView = new ServerHostView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var ServerHostDetailApp = function (element, options) {
        options.model = CMDBModel.HostModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_server_host_detail_list_view'], function (ServerAssetDetailView) {
            var serverAssetDetailView = new ServerAssetDetailView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var ModifyServerHostApp = function (element, options) {
        options.model = CMDBModel.HostModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_modify_server_host_list_view'], function (ServerAssetView) {
            var serverAssetView = new ServerAssetView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var ServerHostDetailApp = function (element, options) {
        options.model = CMDBModel.HostModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_server_host_detail_list_view'], function (ServerAssetView) {
            var serverAssetView = new ServerAssetView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var StorageApp = function (element, options) {
        options.model = CMDBModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_storage_detail_list_view'], function (StorageView) {
            var storageView = new StorageView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };
    return {
        ServerHostApp: ServerHostApp,
        ServerHostDetailApp: ServerHostDetailApp,
        ModifyServerHostApp: ModifyServerHostApp,
        addTriggerStorageApp: StorageApp,
    };
});