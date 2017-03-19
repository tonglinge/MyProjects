/**
 * Created by zengchunyun on 16/8/15.
 */
require.config({
    baseUrl: "/static/js/",
    shim: {
        'underscore': {exports: '_'},
        'backbone': {deps: ['underscore', 'jquery'], exports: 'Backbone'},
        "bootstrap": {deps: ["jquery"], exports: 'jquery'},
        "sweet_alert": {exports: 'sweetAlert'},
        "datetimepicker": {deps: ["bootstrap"]},
        "moment": {deps: ["datetimepicker"]},
        "daterangepicker": {deps: ["jquery"]},
        "bootstrap_switch": {deps: ["jquery"]},
        "app": {deps: ["jquery", "bootstrap"]},
        "jqueryui":{deps: ["jquery"]},
        "high_charts": {deps: ["jquery"]},
        "high_chart_exporting": {deps: ["high_charts"]},
        "high_chart_more": {deps: ["high_charts"]},
        "high_chart_solid_gauge": {deps: ["high_chart_more"]},
        "echarts": {exports: "echarts"}
    },
    paths: {
        "underscore": "libs/underscore/1.8.3/underscore-min",
        "backbone": "libs/backbone/1.3.3/backbone-min",
        "bootstrap": "libs/bootstrap/3.3.7/dist/js/bootstrap.min",
        "bootstrap_switch": "libs/bootstrap-switch/3.3.2/dist/js/bootstrap-switch.min",
        "domReady": "libs/domReady/2.0.1/domReady",
        "datetimepicker": "libs/bootstrap-datetimepicker/2.3.11/js/bootstrap-datetimepicker.min",
        "daterangepicker": "libs/bootstrap-daterangepicker/2.1.24/daterangepicker",
        "moment":"libs/bootstrap-daterangepicker/2.1.24/moment.min",
        "jquery": "libs/jquery/2.2.4/jquery-min",
        "echarts": "libs/echarts/3.3.2/dist/echarts.min",
        "jqueryui": "libs/jquery-ui/1.12.1/jquery-ui.min",
        "high_charts": "libs/highcharts/5.0.2/code/highcharts",
        "high_chart_more": "libs/highcharts/5.0.2/code/highcharts-more",
        "high_chart_solid_gauge": "libs/highcharts/5.0.2/code/modules/solid-gauge",
        "high_chart_exporting": "libs/highcharts/5.0.2/code/modules/exporting",
        "swal":"libs/sweet_alert/1.1.3/dist/sweetalert.min",
        "text": "libs/text/2.0.15/text",
        "app": "src/common/app",
        "common": "src/common/common",
        "bootstrap_select": "libs/bootstrap-select/1.12.1/dist/js/bootstrap-select.min",
        "jstree": "libs/jstree/js/jstree.min",
        "bootstrap_combox": "libs/bootstrap-combox/js/bootstrap-suggest.min"
    },
    waitSeconds: 10
});
