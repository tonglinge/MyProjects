/**
 * Created by zengchunyun on 16/8/18.
 */

define(["jquery", "bootstrap", "fastclick", "sparkline", "jvectormap", "jvectormap-world", "slimScroll", "chartjs"], function ($) {

    require(["app"])
    require(["demo"])
    require(["dashboard"])
    // $.ajax({
    //     url:"http://192.168.101.239/zabbix/api_jsonrpc.php",
    //     type: 'POST',
    //     data:{"jsonrpc": "2.0", "method": "user.login", "params": {"user": "Admin", "password": "zabbix"}, "id": 1, "auth": null},
    //     success: function (callback) {
    //         console.log('hi')
    //     },
    //     error: function (callback) {
    //         console.log('no', callback)
    //     }
    // })
})
