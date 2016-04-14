function get_ta_status(data) {
    if (data){
        console.log(data);
        var html_data = "";
        mydiv = document.getElementById('ta_status');
        for (var i = 0; i< Object.keys(data).length; i++) {

            var ta_name = data[i]["net_id"];
            var ta_status = data[i]["status"];
            console.log(ta_name);
            html_data = html_data.concat('<div><span>');
            html_data = html_data.concat(ta_name);
            html_data = html_data.concat(":");
            html_data = html_data.concat(ta_status);
            html_data = html_data.concat("</span></div>");
        }
        $(mydiv).html("");
        $(mydiv).html(html_data);

    }

}
/**
 * Created by Aadhya on 4/14/16.
 */
$.ajax({
    url: "/update_ta_status/",
    method: "post",
    success:function(data){
        get_ta_status(data);
    }
});
