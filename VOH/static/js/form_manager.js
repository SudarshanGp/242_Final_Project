/**
 * Created by Aadhya on 4/3/16.
 */
function submitComment(form) {

    $.ajax({
        url: "",
        method: "post",
        data: $(form).serialize(),
        success:function(data){
            console.log(data);
        }
    });
}