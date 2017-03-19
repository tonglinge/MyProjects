/**
 * Created by super on 2016/12/12.
 */
define(function (require, exports, module) {
    var _ = require("underscore");
    var Backbone = require("backbone");
    var BackupDBItemViewTemplate = require("text!./templates/sysconfig_dbbackup_record_template.tpl");

    //监控主页模版
    var BackupDBItemView = Backbone.View.extend({
        tagName: "tr",
        events: {},
        template: _.template(BackupDBItemViewTemplate),
        initialize: function (options) {
            this.model = options.model;
            this.showindex = options.showindex;
        },
        render: function () {
            var model_to_json= this.model.toJSON();
            model_to_json["showindex"] = this.showindex;
            this.$el.html(this.template(model_to_json));
            return this;
        }
    });
    return {
        BackupDBItemView: BackupDBItemView
    }
});