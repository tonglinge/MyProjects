/**
 * Created by zengchunyun on 2016/11/15.
 */

define(["app"], function () {
    //页面主框架菜单事件都是通过app模块触发的,所以其它模块如果不继承该模块,则必须导入该模块才能使页面菜单生效

    var FormDateTime = function (selector) {
        //包含时间和日期的插件
        require(["jquery","datetimepicker"], function ($) {
            $(selector).datetimepicker({
                weekStart: 1,
                todayBtn:  1,
                autoclose: 1,
                todayHighlight: 1,
                startView: 2,
                forceParse: 0,
                showMeridian: 1
            });
        });
    };

    var FormTime = function (selector) {
        //包含时间的插件
        require(["jquery","datetimepicker"], function ($) {
            $(selector).datetimepicker({
                language:  'fr',
                weekStart: 1,
                todayBtn:  1,
                autoclose: 1,
                todayHighlight: 1,
                startView: 1,
                minView: 0,
                maxView: 1,
                forceParse: 0
            });
        });
    };

    //首页
    var Index = function (options) {
        require(["src/tracker/tracker_app", "high_charts"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".tracker_index"};
            }
            var appSelector = ".tracker_index";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerIndexApp(appSelector, {url: "/api/v1/tracker/index/"})
        });
    };

    //应用
    var Application = function (options) {
        require(["src/tracker/tracker_app", "bootstrap_switch", "high_charts", "high_chart_solid_gauge"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".tracker_application"};
            }
            var appSelector = ".tracker_application";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerApplicationApp(appSelector, {url: "/api/v1/tracker/application/"})
        });
    };

    //网络
    var Network = function (options) {
        require(["src/tracker/tracker_app", "bootstrap_switch", "high_charts", "high_chart_solid_gauge"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".tracker_network"};
            }
            var appSelector = ".tracker_network";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerNetworkApp(appSelector, {url: "/api/v1/tracker/network/"})
        });
    };

    //事件
    var Events = function (options) {
        require(["src/tracker/tracker_app", "bootstrap_switch"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".tracker_events"};
            }
            var appSelector = ".tracker_events";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerEventsApp(appSelector, {url: "/api/v1/tracker/events/"})
        });
    };

    //主机
    var Host = function (options) {
        require(["src/tracker/tracker_app", "bootstrap_switch", "high_charts", "high_chart_solid_gauge"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".tracker_host"};
            }
            var appSelector = ".tracker_host";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerHostApp(appSelector, {url: "/api/v1/tracker/host/"})
        });
    };

    //配置管理／主机管理
    var HostConfig = function (options) {
        require(["src/tracker/tracker_app"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".tracker_host_config"};
            }
            var appSelector = ".tracker_host_config";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerHostConfigApp(appSelector, {url: "/api/v1/tracker/host/config/"})
        });
    };

    //配置管理／设置
    var Settings = function (options) {
        require(["src/tracker/tracker_app"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".tracker_settings"};
            }
            var appSelector = ".tracker_settings";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerSettingsApp(appSelector, {url: "/api/v1/tracker/settings/"})
        });
    };


    //将上面封装的接口通过return暴露外部调用
    return {
        triggerIndex: Index,
        triggerApplication: Application,
        triggerNetwork: Network,
        triggerEvents: Events,
        triggerHost: Host,
        triggerHostConfig: HostConfig,
        triggerSettings: Settings
    }
});