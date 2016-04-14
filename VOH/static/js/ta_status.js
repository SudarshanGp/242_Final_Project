update_ta_status();
setInterval(function(){
    update_ta_status();
}, 5000);

function get_ta_status(data) {
    if (data){
        console.log(data);
        var html_data = "";
        mydiv = document.getElementById('ta_status');
        for (var i = 0; i< Object.keys(data).length; i++) {

            var ta_net_id = data[i]["net_id"];
            var ta_status = data[i]["status"];
            var ta_name = data[i]['name'];
            console.log(ta_name);
            path = "../static/data/img/" + ta_net_id + ".jpg";
            html_data = html_data.concat('<div class = "container"><div class="fixed-action-btn horizontal click-to-toggle">');
            html_data = html_data.concat('<a class="btn-floating btn pink accent-3">');
            html_data = html_data.concat('<i class="large material-icons">mode_edit</i>');
            html_data = html_data.concat('</a><ul>');
            html_data = html_data.concat('<li><a class="btn-floating green"><i class="material-icons">add</i></a></li>');
            html_data = html_data.concat('<li><a class="btn-floating red"><i class="material-icons">remove</i></a></li>');
            html_data = html_data.concat('</ul></div><div class = "chip"><img src =');
            html_data = html_data.concat(path);
            html_data = html_data.concat('></img>');
            html_data = html_data.concat(ta_name);
            html_data = html_data.concat('</h5></div></div>');

        }
        $(mydiv).html("");
        $(mydiv).html(html_data);

    }

}
/**
 * Created by Aadhya on 4/14/16.
 */
function update_ta_status(){
    console.log("in ere");
   $.ajax({
    url: "/update_ta_status/",
    method: "post",
    success:function(data){
        setTimeout(function(){get_ta_status(data);}, 1000);
    }
});
}