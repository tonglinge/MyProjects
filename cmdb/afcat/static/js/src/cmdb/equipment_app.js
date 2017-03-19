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
    var EquipmentApp = function (element, options) {
        options.model = CMDBModel.EquipmentModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_equipment_list_view'], function (EquipmentView) {
            var equipmentView = new EquipmentView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var EquipmentDetailApp = function (element, options) {
        options.model = CMDBModel.EquipmentModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_equipment_detail_list_view'], function (EquipmentDetailView) {
            var equipmentDetailView = new EquipmentDetailView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    var modifyEquipmentApp = function (element, options) {
        options.model = CMDBModel.EquipmentModel;
        var cmdbCollection = new CMDBCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_modify_equipment_list_view'], function (EquipmentView) {
            var equipmentView = new EquipmentView({
                el: $(element),
                collection: cmdbCollection,
                url: options.url,
                options: options
            });
        });
    };

    return {
        addTrigerEquipmentApp: EquipmentApp,
        addTrigerEquipmentDetailApp: EquipmentDetailApp,
        addTrigerModifyEquipmentApp: modifyEquipmentApp,
    };
});