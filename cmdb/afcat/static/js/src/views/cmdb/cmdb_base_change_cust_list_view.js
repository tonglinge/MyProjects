/**
 * Created by super on 2016/12/26.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');

    var ChangeCustView = Backbone.View.extend({
        events: {
            "click .li-custinfo": "changeCust"
        },
        initialize: function (options) {
            this.collection.url = options.url;
            this.model = options.options.model;

        },
        afterChange: function (args, collection, response, options) {
            window.location.reload();
        },
        changeCust: function (e) {
            var custid = $(e.currentTarget).find(".a-custinfo").attr("cid");
            if (!$(e.currentTarget).hasClass("isactive")) {
                this.collection.fetchData(false, {custid: custid, method: 'cmdb.configure.change_cust'},
                    {type: "get", success: this.afterChange})
            }
        }
    });
    return ChangeCustView;

});