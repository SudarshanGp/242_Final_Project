/**
 * Created by Aadhya on 4/3/16.
 */


function submitComment(form) {
    $.ajax({
        url: "/authenticate/",
        method: "post",
        data: $(form).serialize(),
        success:function(data){
            console.log(data);
        },
        error:function(data){
            console.log(data);
        }
    });
}