/**
 * Created by zengchunyun on 2016/10/21.
 */
define(function (require,exports,module) {
    var $ = require("jquery");
    function resizeWidth(innerElement,outerElement) {
        /*
        * @innerElement:需要修改偏移位置的元素
        * @outerElement:被参照的元素
        * */
        var innerElementWidth = $(innerElement).width();
        var windowWidth = $(outerElement).width();
        var differWidth = parseInt(windowWidth) - parseInt(innerElementWidth);
        if (differWidth > 0) {
            $(innerElement).css("right", differWidth / 2);
        }
    }

    function resizeHeight(innerElement,outerElement) {
        /*
        * @innerElement:需要修改偏移位置的元素
        * @outerElement:被参照的元素
        * */
        var innerElementHeight = $(innerElement).height();
        var outerElementHeight = $(window).height();

        var differHeight = parseInt(outerElementHeight) - parseInt(innerElementHeight);
        if (differHeight > 0) {
            $(innerElement).css("top", differHeight / 2);
        }
    }

    function resizeElement(innerElement,outerElement) {
        $(window).resize(function () {
            resizeWidth(innerElement,outerElement);
            resizeHeight(innerElement,outerElement);
        });
        $(window).ready(function () {
            resizeWidth(innerElement,outerElement);
            resizeHeight(innerElement,outerElement);
        });
    }

    return {
        resizeWidth:resizeWidth,
        resizeHeight:resizeHeight,
        resizeElement:resizeElement
    }
    
})