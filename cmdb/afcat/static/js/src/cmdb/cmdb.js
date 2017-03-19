/**
 * Created by zhanghai on 16/9/18.
 * 注意,当define改为require,exports,module时,会将所有该页面require对JS提前加载,如果想调用时加载,必须是define([依赖JS],function(回调函数))
 */
define([], function () {
    //页面主框架菜单事件都是通过app模块触发的,所以其它模块如果不继承该模块,则必须导入该模块才能使页面菜单生效
    require(["app"]);
    var $ = require(["jquery"]);

    (function ($) {
      $.getUrlParam = function (name) {
       var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
       var r = window.location.search.substr(1).match(reg);
       if (r != null) return decodeURI(r[2]); return null;
      }
     })($);

    //首页
    var Index = function () {
        require(["src/cmdb/cmdb_app"], function (cmdb) {
            cmdb.triggerIndexApp(".index-app", {url: "/api/v1/afcat/"})
        })
    };

    //服务器资产
    var ServerAsset = function () {
        require(["src/cmdb/server_asset_app", "jqueryui"], function (app) {
            app.trigerServerAssetApp(".server-asset-app", {type:'assets', url: "/cmdb/assetinfo/"});
        })
    };

    //服务器资产详情
    var ServerAssetDetail = function () {
        require(["src/cmdb/server_asset_app", "jqueryui"], function (app) {
            var sid = $.getUrlParam("sid");
            app.trigerServerAssetDetailApp(".server-asset-detail-app", {type:'assets', sid:sid, url: "/cmdb/assetdetail/"});
        })
    };

    //编辑或添加服务器资产
    var ModifyServerAsset = function () {
        require(["src/cmdb/server_asset_app", "jqueryui"], function (app) {
            var action = $.getUrlParam("action");
            var sid = $.getUrlParam("sid");
            app.triggerModifyServerAssetApp(".server-asset-app", {type:'assets', "action":action, "sid":sid, url: "/cmdb/assetmodify/"});
        })
    };

    //“主机管理”主页trigger
    var ServerHost = function () {
        require(["src/cmdb/server_host_app", "jqueryui"], function (app) {
            app.ServerHostApp(".server-asset-app", {type:'server', url: "/cmdb/assetinfo/"})
        })
    };

    //“主机管理”编辑页面trigger
    var ModifyServerHost = function () {
        var action = $.getUrlParam("action");
        var sid = $.getUrlParam("sid");
        require(["src/cmdb/server_host_app", "jqueryui"], function (app) {
            app.ModifyServerHostApp(".server-asset-app", {type:'server', sid:sid, action:action, url: "/cmdb/assetmodify/"})
        })
    };

    //“主机管理”详情页面trigger
    var ServerHostDetail = function () {
        var sid = $.getUrlParam("sid");
        require(["src/cmdb/server_host_app", "jqueryui"], function (app) {
            app.ServerHostDetailApp(".server-host-detail-app", {type:'server', sid:sid, url: "/cmdb/assetdetail/"})
        })
    };

    //设备资产
    var Equipment = function () {
        var sid = $.getUrlParam("sid");
        require(["src/cmdb/equipment_app", "jqueryui"], function (app) {
            app.addTrigerEquipmentApp(".equipment-app", {type:'equipment', "sid":sid, url: "/cmdb/assetinfo/"})
        })

    };

    //设备资产详情
    var EquipmentDetail = function () {
        //设备资产详情app
        var sid = $.getUrlParam("sid");
        require(["src/cmdb/equipment_app", "jqueryui"], function (app) {
            app.addTrigerEquipmentDetailApp(".equipment-app", {type:'equipment', sid:sid, url: "/cmdb/assetdetail/"});
        });
    };

    //编辑或添加设备资产app
    var ModifyEquipment = function () {
        var action = $.getUrlParam("action");
        var sid = $.getUrlParam("sid");
        require(["src/cmdb/equipment_app", "jqueryui"], function (app) {
            app.addTrigerModifyEquipmentApp(".server-asset-app", {"action":action, "sid":sid, url: "/cmdb/assetmodify/"});
        });
    };

    //基表维护
    var AdminIndex = function (options) {
        require(["src/cmdb/cmdb_app"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".cmdb_admin_index"};
            }
            var appSelector = ".cmdb_admin_index";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerAdminIndexApp(appSelector, {url: "/api/v1/cmdb/"})
        });
    };
    //备份数据库
    var SysDatabaseBackup = function (options) {
        require(["src/cmdb/cmdb_app"], function (app) {
            if(typeof options == "undefined"){
                options = {selector: ".sysconfig-backupdb"};
            }
            var appSelector = ".sysconfig-backupdb";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerBackupDBApp(appSelector, {url: "/api/v1/afcat/"});
            //app.triggerAdminIndexApp(appSelector, {url: "/api/v1/cmdb/admin/index/"})
        })
    };
    // 切换客户
    var ChangeCustomer = function (options) {
        require(["src/cmdb/cmdb_app"], function (app) {
            app.triggerChangeCustApp(".div-custinfo-content", {url: "/api/v1/afcat/"});
        })
    };

    //导入Excel接口
    var ImportExcel = function (options) {
        require(["src/cmdb/cmdb_app"], function (app) {
            app.triggerImportExcelApp(".import-excel-app", {url: "/cmdb/dataimport/"});
        })
    };

    //IP配置
    var IPManagement = function (options) {
        require(["src/cmdb/cmdb_app", "jstree"], function (app) {
            app.triggerIPManagementApp(".ip-config-app", {url: "/api/v1/afcat/"});
        })
    };
    //F5配置
    var BalanceMapping = function (options) {
        require(["src/cmdb/cmdb_app"], function (app) {
            app.triggerBalanceMapping(".lbmapping-app", {url:"/api/v1/afcat/"});
        })
    };

    ///新首页
    var Index2 = function () {
        require(["src/cmdb/cmdb_app"], function (cmdb) {
            cmdb.triggerIndexApp(".index-app", {url: "/api/v1/afcat/"})
        })
    };

    ///操作日志
    var OperationLog = function () {
        require(["src/cmdb/cmdb_app"], function (cmdb) {
            cmdb.triggerOperationLogApp(".oplog-app", {url: "/api/v1/afcat/"})
        })
    };

    //将上面封装的接口通过return暴露外部调用
    return {
        triggerServerAsset: ServerAsset,
        triggerServerAssetDetail: ServerAssetDetail,
        triggerModifyServerAsset: ModifyServerAsset,
        triggerServerHost: ServerHost,
        triggerModifyServerHost: ModifyServerHost,
        triggerServerHostDetail: ServerHostDetail,
        triggerEquipment: Equipment,
        triggerEquipmentDetail: EquipmentDetail,
        triggerModifyEquipment: ModifyEquipment,
        triggerIndex: Index,
        triggerAdminIndex: AdminIndex,
        triggerSysconfigDBBackup: SysDatabaseBackup,
        triggerChangeCust: ChangeCustomer,
        triggerImportExcel: ImportExcel,
        triggerIPManagement: IPManagement,
        triggerBalanceMapping: BalanceMapping,
        triggerNewIndex: Index2,
        triggerOperationLog: OperationLog
    }
});