// update_ta_status();
// setInterval(function(){
//     update_ta_status();
// }, 5000);
var socket;
$(document).ready(function() {
    console.log("ADDING SOCKETIO");
    socket = io.connect('http://' + document.domain + ':' + location.port + '/login'); // Connect to socket.io server
    console.log('socket');
    socket.on('connect', function () {
        console.log("EMIT LOGIN TA");
        socket.emit('loginTA', {}); // On connect of a new user, emit join signal to socket.io server
        // socket.emit('updateTA', {msg : "update"});
    });
    socket.on('online', function (data) {
        console.log("here in online");
        console.log(data);
        get_ta_status(data);
    })
    // socket.on('newonline', function () {
    //      socket.emit('updateTA', {msg : "update"}); // On connect of a new user, emit join signal to socket.io server
    // });
        
});
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
            //html_data = html_data.concat('<div class="fixed-action-btn horizontal click-to-toggle">');
            //html_data = html_data.concat('<a class="btn-floating btn blue accent-3">');
            //html_data = html_data.concat('<i class="large material-icons">mode_edit</i>');
            html_data = html_data.concat('<div class = "row"></div><a class="btn-floating  green" style = "width: 25px; height: 25px;"><i class="tiny material-icons">add</i></a>');
            html_data = html_data.concat('<a class="btn-floating red" style = "width: 25px; height: 25px;"><i class="tiny material-icons">remove</i></a>');
            html_data = html_data.concat('<div class = "chip"><img src =');
            html_data = html_data.concat(path);
            html_data = html_data.concat('></img>');
            html_data = html_data.concat(ta_name);
            html_data = html_data.concat('</h5></div></div>');

        }
        $(mydiv).html("");
        $(mydiv).html(html_data);

    }

}
// /**
//  * Created by Aadhya on 4/14/16.
//  */
// function update_ta_status(){
//     console.log("in ere");
//    $.ajax({
//     url: "/update_ta_status/",
//     method: "post",
//     success:function(data){
//         setTimeout(function(){get_ta_status(data);}, 1000);
//     }
// });
// }