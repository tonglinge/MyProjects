/**
 * Created by zengchunyun on 16/8/18.
 * 注意,当define改为require,exports,module时,会将所有该页面require对JS提前加载,如果想调用时加载,必须是define([依赖JS],function(回调函数))
 */
define([], function () {
    //页面主框架菜单事件都是通过app模块触发的,所以其它模块如果不继承该模块,则必须导入该模块才能使页面菜单生效
    require(["app"]);

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


    //监控首页
    var MonitorIndex = function () {
        require(["src/monitor/monitor_app", "high_charts"], function (app) {
            app.triggerDashboardApp(".monitor_dashboard", { url: "/monitor/get_host_groups_status/"})
        });
    };

    //监控组/主机组
    var HostGroups = function () {
        require(["src/monitor/monitor_app"], function (app) {
            FormDateTime('.issue-time');
            app.triggerHostGroupsApp(".host-groups-app", {type:'group', url: "/monitor/get_host_groups/"})
        })
    };

    //主机信息
    var HostInfo = function () {
        require(["src/monitor/monitor_app", "bootstrap_switch", "high_charts", "daterangepicker"], function (app) {
            //通过url获取当前查询主机的页面类型
            var url = window.location.href;
            var display_type = url.toString().split('/')[6];
            var host_id = url.toString().split('/')[5];
            app.triggerHostInfoApp(".host-info", {'type': display_type, url: "/monitor/get_host_graph_detail/", host_id: host_id})
        });
    };

    //告警事件
    var EventTrigger = function (options) {
        require(["src/monitor/monitor_app"], function (app) {
            FormDateTime('.form_datetime');
            var appSelector = "#event_trigger";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerEventApp(appSelector, {url: "/monitor/get_event_trigger/"})
        });
    };

    //配置管理／主机群组
    var ConfigHostGroups = function (options) {
        require(["src/monitor/monitor_app"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".config_host_groups"};
            }
            var appSelector = ".config_host_groups";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            EventTrigger(options);
            app.triggerConfigHostGroupsApp(appSelector, {url: "/monitor/create_new_group/"})
        });
    };

    //配置管理／主机
    var ConfigHost = function (options) {
        require(["src/monitor/monitor_app"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".config_host"};
            }
            var appSelector = ".config_host";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            app.triggerConfigHostApp(appSelector, {url: "/monitor/config/host/detail/"})
        });
    };

    //报表／默认
    var ReportDefault = function (options) {
        require(["src/monitor/monitor_app"], function (app) {
            if(typeof options == "undefined"){
                options = {selector:".export_data"};
            }
            var appSelector = ".config_host_groups";
            if(typeof options != "undefined" && typeof options.selector != "undefined"){
                appSelector = options.selector
            }
            EventTrigger(options);
            app.triggerReportDefaultApp(appSelector, { url: "/monitor/export_data_to_file/"})
        });
    };

    //报表／默认
    var ReportCustom = function (options) {
        require(["src/monitor/monitor_app"], function (app) {
            app.triggerReportDefaultApp(".export_data", { url: "/monitor/export_data_to_file/"})
        });
    };

    //将上面封装的接口通过return暴露外部调用
    return {
        triggerMonitorIndex: MonitorIndex,
        triggerHostGroups: HostGroups,
        triggerHostInfo: HostInfo,
        triggerEventTrigger: EventTrigger,
        triggerConfigHostGroups: ConfigHostGroups,
        triggerConfigHost: ConfigHost,
        triggerReportDefault: ReportDefault,
        triggerReportCustom: ReportCustom
    }
});