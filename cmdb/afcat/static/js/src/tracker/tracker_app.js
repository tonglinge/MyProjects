/**
 * Created by zengchunyun on 2016/11/15.
 */
define(function (require, exports, module) {
    var $ = require('jquery');
    //启动app入口点


    //导入模型
    var Model = require('../models/tracker/tracker_model');

    //导入集合
    var Collection = require('../collections/collection');


    //首页app
    var IndexApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/tracker/tracker_index_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //应用app
    var ApplicationApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/tracker/tracker_application_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //网络app
    var NetworkApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/tracker/tracker_network_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //事件app
    var EventsApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/tracker/tracker_events_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //主机app
    var HostApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/tracker/tracker_host_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //主机配置app
    var HostConfigApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/tracker/tracker_config_host_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    //设置app
    var SettingsApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/tracker/tracker_config_settings_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    return {
        triggerIndexApp: IndexApp,
        triggerApplicationApp: ApplicationApp,
        triggerNetworkApp: NetworkApp,
        triggerEventsApp: EventsApp,
        triggerHostApp: HostApp,
        triggerHostConfigApp: HostConfigApp,
        triggerSettingsApp: SettingsApp
    };
});