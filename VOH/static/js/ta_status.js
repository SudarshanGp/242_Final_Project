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
    });

    socket.on('add_student', function(data){
        console.log("ADD STUDENT");
        if (window.location.href.includes("/TA/")) {

            console.log("iN ADD STUDENT");
            console.log(data);
            get_ta_queue(data);
        }
        else{
        console.log("Boo");
         }

    });

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
            id_add = ta_net_id;
            id_remove = ta_net_id + "remove";
            path = "../static/data/img/" + ta_net_id + ".jpg";
            html_data = html_data.concat('<div class = "row"></div><a class="btn-floating green" onclick = \"addqueue(this);\" id = \"');
            //html_data = html_data.concat(ta_net_id);
            //html_data = html_data.concat(')\" id = \"');
            html_data = html_data.concat(id_add);
            html_data = html_data.concat('\">Join</a>');
            html_data = html_data.concat('<a class="btn-floating red" onclick = \"removequeue(');
            html_data = html_data.concat(ta_net_id);
            html_data = html_data.concat(');\" id = \"');
            html_data = html_data.concat(id_remove);
            html_data = html_data.concat('\">Leave</a>');
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

function removequeue(id){
    console.log("in remove");

}

function addqueue(id){

    console.log(id.id);
     socket.emit('add_student', {"net_id":id.id});
}

function get_ta_queue(data){
    if (data){
       var html_data = ""
        console.log("data");
        console.log(data);
        mydiv = document.getElementById('ta_queue');
        for (var i = 0; i< Object.keys(data).length; i++) {

            var student_net_id = data[i]["student"];
            console.log(student_net_id);
            html_data = html_data.concat('<div class = "row"></div><a class="btn-floating green" onclick = \"answerstudent(this);\" id = \"');
            //html_data = html_data.concat(ta_net_id);
            //html_data = html_data.concat(')\" id = \"');
            html_data = html_data.concat(student_net_id);
            html_data = html_data.concat('\">Answer</a>');
            html_data = html_data.concat('<div class = "chip large">');
            html_data = html_data.concat(student_net_id);
            html_data = html_data.concat('</h5></div>');

        }
        $(mydiv).html("");
        $(mydiv).html(html_data);
    }

}

function answerstudent(id) {
    console.log(id.id);
    // socket.emit('add_student', {"net_id":id.id});

}