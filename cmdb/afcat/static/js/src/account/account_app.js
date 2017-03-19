/**
 * Created by zengchunyun on 16/8/25.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var AccountCommonModel = require("../models/account/account_model");

    var AccountCommonCollection = require("../collections/account/account_collection");

    //导入模型
    var Model = require('../models/cmdb/cmdb_models');

    //导入集合
    var Collection = require('../collections/collection');

    //修改密码
    var UserProfileApp = function (element, options) {
        options.model = Model.CommonModel;
        var collection = new Collection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/account/account_user_profile_list_view'], function (AppView) {
            var appView = new AppView({
                el: $(element),
                collection: collection,
                url: options.url,
                options: options
            });
        });
    };

    var ChangeGroup = function (element, options) {
        options.model = AccountCommonModel.PermModel;
        options.model.url = options.url;
        var collections = new AccountCommonCollection(options);

        require(["../views/account/account_group_perm_list_view"],function(PermView) {
            var permview = new PermView({
                el:$(element),
                collection:collections,
                url:options.url,
                model:options.model
            });
        })
    };

    //用户app
    var Userlist = function (element, options) {
        options.model = AccountCommonModel.UserModel;
        options.model.url = options.url;  // 用户操作的url
        var collection = new AccountCommonCollection(options);
        require(["../views/account/account_user_list_view"], function(UserView) {
            var userview = new UserView({
                el: $(element),
                collection: collection,
                url:options.url,
                model: options.model
            });
        })

    };

    return {
        groupPermApp: ChangeGroup,
        userPermApp: Userlist,
        userProfileApp: UserProfileApp
    }
});