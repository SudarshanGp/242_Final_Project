var socket;
$(document).ready(function() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/login'); // Connect to socket.io server
    socket.on('connect', function () {
        console.log("EMIT LOGIN TA");
        socket.emit('loginTA', {}); // On connect of a new user, emit join signal to socket.io server
    });
    socket.on('online', function (data) {
        console.log("here in online");
        console.log(data);
        get_ta_status(data);
    })
        
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
            path = "../static/data/img/" + ta_net_id + ".jpg";
            html_data = html_data.concat('<div class = "row"></div><a class="btn-floating green" >Join</a>');
            html_data = html_data.concat('<a class="btn-floating red" >Leave</a>');
            html_data = html_data.concat('<div class = "chip large"><img src =');
            html_data = html_data.concat(path);
            html_data = html_data.concat('></img>');
            html_data = html_data.concat(ta_name);
            html_data = html_data.concat('</h5></div></div>');

        }
        $(mydiv).html("");
        $(mydiv).html(html_data);

    }

}