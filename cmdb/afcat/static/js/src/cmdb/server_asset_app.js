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
    var ServerAssetApp = function (element, options) {
        options.model = CMDBModel.AssetModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_server_asset_list_view'], function (ServerAssetView) {
            var serverAssetView = new ServerAssetView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var ServerAssetDetailApp = function (element, options) {
        options.model = CMDBModel.AssetModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_server_asset_detail_list_view'], function (ServerAssetDetailView) {
            var serverAssetDetailView = new ServerAssetDetailView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var ModifyServerAssetApp = function (element, options) {
        options.model = CMDBModel.AssetModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_modify_server_asset_list_view'], function (ServerAssetView) {
            var serverAssetView = new ServerAssetView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    return {
        trigerServerAssetApp: ServerAssetApp,
        trigerServerAssetDetailApp: ServerAssetDetailApp,
        triggerModifyServerAssetApp: ModifyServerAssetApp,
    }
});