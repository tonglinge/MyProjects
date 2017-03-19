/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var VolumeGroupDetailTemplate = require('text!./templates/volume_group_detail_template.tpl');
    var VolumeGroupDetailView = Backbone.View.extend({
        className: "",
        tagName: "div",
        template: _.template(VolumeGroupDetailTemplate),
        events: {

        },
        initialize: function (options) {
            this.model = options.model;
            this.collection = options.collection;
            this.url = options.url;
            this.sid = options.sid;
            this.vg_id = options.vg_id;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.collection.toJSON()[0])
            this.$el.html(this.template(this.collection.toJSON()[0]));
            return this;
        }
    });

    return {
        VolumeGroupDetailView: VolumeGroupDetailView,
    };
})