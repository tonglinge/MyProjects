/**
 * Created by zengchunyun on 2016/11/17.
 */
define(function (require, exports, module) {
    var $ = require('jquery');
    //启动app入口点

    //导入模型
    var Model = require('../models/cmdb/cmdb_models');

    //导入集合
    var Collection = require('../collections/collection');


    //首页app
    var AdminIndexApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_admin_index_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //首页app
    var IndexApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_index_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //数据库备份
    var BackupDBApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/cmdb/cmdb_sysconfig_backupdb_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };
    // 切换客户
    var ChangeCustApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        require(['../views/cmdb/cmdb_base_change_cust_list_view'], function (CustView) {
            var appView = new CustView({
                el: $(element),
                collection: collection,
                url: options.url,
                options:options
            })
        })
    };

    // 导入Excel
    var ImportExcelApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        require(['../views/cmdb/cmdb_import_excel_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options:options
            })
        })
    };

    //IP配置
    var IPManagementApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        require(['../views/cmdb/cmdb_ip_management_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options:options
            })
        })
    };

    //F5地址映射
    var BalanceMapping = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        require(['../views/cmdb/cmdb_lbmapping_list_view'], function (AppView) {
            var appview = new AppView({
                el: $(element),
                collection:collection,
                url:options.url,
                model:options.model
            })
        })
    };

    //操作日志
    var OperationLogApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        require(['../views/cmdb/cmdb_oplog_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };


    return {
        triggerAdminIndexApp: AdminIndexApp,
        triggerIndexApp: IndexApp,
        triggerBackupDBApp: BackupDBApp,
        triggerChangeCustApp: ChangeCustApp,
        triggerImportExcelApp: ImportExcelApp,
        triggerIPManagementApp: IPManagementApp,
        triggerBalanceMapping: BalanceMapping,
        triggerOperationLogApp: OperationLogApp
    };
});