/**
 * Created by super on 2016/5/11.
 */


function delCurrtr(ths){
    var choose = window.confirm("是否确定要删除该记录!");
    console.log(choose);
    if (choose){
        var book_id = $(ths).parent().prevAll().last().children().val();
        $.ajax({
            url:'/day16/books/'+book_id+"/del/",
            method:'POST',
            success:function (data) {
                console.log(data);
                window.location.reload();
            }
        });

        return true
    }else{
        return false
    }
}

function editCurrtr(ths) {
    var book_id = $(ths).parent().prevAll().last().children().val();
    window.location.href = '/day16/books/'+book_id+'/edit/';
}

function searchbook(ths) {
    $("#search_form").submit();
}