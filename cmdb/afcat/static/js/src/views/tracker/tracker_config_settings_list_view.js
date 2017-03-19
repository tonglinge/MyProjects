/**
 * Created by zengchunyun on 2016/12/5.
 */
define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require("underscore");
    var Backbone = require('backbone');
    var SettingsItemView = require("./tracker_config_settings_item_view").SettingsItemView;


    var SettingsView = Backbone.View.extend({
        events: {},
        initialize: function (options) {
            this.collection.url = options.url;
            this.model = options.options.model;
            this.listenTo(this.collection, 'reset', this.addAll);
            this.collection.fetchData(true, {method: "show.overview"})
        },
        addAll: function () {
            var models = this.collection.models;
            //针对每次reload数据时需要清空整个app页面数据，指定判断关键属性，用来决定是否对app内容清空
            if(this.collection.reseted && models.length > 0 && models[0].has("hosts_status")){
                this.$el.find('.hosts_tbody').html('')
            }
            this.collection.each(this.addOne, this);
        },
        addOne: function (model) {
            var view = new SettingsItemView({model: model});
            this.$el.find(".hosts_tbody").append(view.render().el);
        }
    });
    return SettingsView;

});