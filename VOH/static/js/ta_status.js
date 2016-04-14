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