/**
 * Created by zengchunyun on 2016/9/30.
 */

//配置主机组页面
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var ConfigHostItemView = require("./monitor_config_host_item_view").ConfigHostItemView;


    var ConfigHostView = Backbone.View.extend({
        events: {
            "click #search_btn": "getHost",
            "click .add_host": "addHost"
        },
        initialize: function (options) {
            this.addToMenu = false;
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true)
        },
        addAll: function () {
            if(this.collection.reseted && typeof this.collection.models[0].get("get_hosts") == 'undefined'){
                this.$el.find('.hosts_tbody').html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new ConfigHostItemView({model: model});
            this.$el.find(".hosts_tbody").append(view.render().el);
        },
        getHost: function (e) {
            var filter_host = this.$el.find('[name="filter_host"]').val();
            var filter_dns = this.$el.find('[name="filter_dns"]').val();
            var filter_ip = this.$el.find('[name="filter_ip"]').val();
            var filter_port = this.$el.find('[name="filter_port"]').val();
            this.collection.fetchData(true,{filter_host:filter_host,filter_dns:filter_dns,filter_ip:filter_ip,filter_port:filter_port})
        },
        addHost: function (e) {

        }
    });
    return ConfigHostView;

});