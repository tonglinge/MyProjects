/**
 * Created by zengchunyun on 16/8/18.
 * 注意,当define改为require,exports,module时,会将所有该页面require对JS提前加载,如果想调用时加载,必须是define([依赖JS],function(回调函数))
 */
define([], function () {
    var MonitorIndex = function () {
        require(["src/account/account_app"], function (account) {
            account.groupPermApp("#perm-list", {url:"account/group_management"})
        })
    };

    var UserIndex = function () {
        require(["src/account/account_app", "bootstrap_select"], function (users) {
            users.userPermApp("#perm-user-manage-div", {url:"account/user_management"})
        })

    };

    var UserProfile = function () {
        require(["src/account/account_app"], function (users) {
            users.userProfileApp("#userprofile", {url:"/api/v1/afcat/"})
        })
    };
    //将上面封装的接口通过return暴露外部调用
    return {
        triggerGroupPermIndex: MonitorIndex,
        triggerUserlistIndex: UserIndex,
        triggerUserProfile: UserProfile

    }
});