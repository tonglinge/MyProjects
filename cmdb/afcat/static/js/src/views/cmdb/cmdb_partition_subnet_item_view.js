/**
 * Created by zhanghai on 2016/9/20.
 */

define(function (require, exports, module) {
    var $ = require("jquery");
    var _ = require('underscore');
    var Backbone = require('backbone');
    var partitionSubnetItemTemplate = require('text!./templates/partition_subnet_template.tpl');
    var createSubnetItemTemplate = require('text!./templates/create_subnet_template.tpl');
    var modifySubnetItemTemplate = require('text!./templates/modify_subnet_template.tpl');
    var allocateIPItemTemplate = require('text!./templates/allocate_ip_template.tpl');

    var SubnetItemView = Backbone.View.extend({
        template: _.template(partitionSubnetItemTemplate),
        events: {
        },
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.record)
            console.log("model:", this.model)
            this.$el.html(this.template(this.model));
            return this;
        }
    });

    var CreateSubnetItemView = Backbone.View.extend({
        template: _.template(createSubnetItemTemplate),
        events: {
        },
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.record)
            console.log("model:", this.model)
            this.$el.html(this.template(this.model));
            return this;
        }
    });

    var ModifySubnetItemView = Backbone.View.extend({
        template: _.template(modifySubnetItemTemplate),
        events: {
        },
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.record)
            console.log("model:", this.model)
            this.$el.html(this.template(this.model));
            return this;
        }
    });

    var AllocateIPItemView = Backbone.View.extend({
        template: _.template(allocateIPItemTemplate),
        events: {
        },
        initialize: function (options) {
            this.model = options.model;
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function () {
            //console.log(this.record)
            console.log("model:", this.model)
            this.$el.html(this.template(this.model));
            return this;
        }
    });

    return {
        SubnetItemView: SubnetItemView,
        CreateSubnetItemView: CreateSubnetItemView,
        ModifySubnetItemView: ModifySubnetItemView,
        AllocateIPItemView: AllocateIPItemView,
    };
})