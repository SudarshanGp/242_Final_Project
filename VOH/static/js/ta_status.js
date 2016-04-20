var socket;
$(document).ready(function() {
    /**
     * All socket IO listeners that catch different emit calls in order to update
     * either the TA queue or the List of Online TA's
     */
    socket = io.connect('http://' + document.domain + ':' + location.port + '/login'); // Connect to socket.io server
    socket.on('connect', function () {
        socket.emit('loginTA', {});
        socket.emit('getTAQueue', {});
    });
    socket.on('online', function (data) {
        get_ta_status(data['online']);
        get_ta_queue(data['queue']);

    });
    /**
     * Add the student to a Queue
     */
    socket.on('add_student_queue', function(data){
        if (window.location.href.includes("/TA/")) {
            if(data){
                get_ta_queue(data['queue']);
            }
        }
    });
    socket.on('answer_info', function(data){
        console.log(data);
        if (window.location.href.includes("/TA/")) {
            var parser =  document.createElement('a');
            parser.href = window.location.href;
            var ta = parser.pathname.split('/')[2];
            console.log(ta);
            if(ta == data['ta']){

                console.log("ITS A TA");
                socket.emit('join_room', {room : data['room']});
                var redirect ='http://' + document.domain + ':' + location.port + '/chat';
                window.location.href = redirect;
            }

        }
        else if( window.location.href.includes("/student/")){
            var parser =  document.createElement('a');
            parser.href = window.location.href;
            var student = parser.pathname.split('/')[2]; // student
            console.log(student);
            if(student == data['student']){
                console.log("ITS TSUDNET");
                socket.emit('join_room', {room : data['room']});
                var redirect ='http://' + document.domain + ':' + location.port + '/chat';
                window.location.href = redirect;
            }


        }
        
        // RETDIRECT TO NEW CHAT WINDOW
        // DATA has to contain unique chat id/ url data
    })

});

function get_ta_status(data) {
    /**
     * Updates the list of Online TA's
     */
    if (data){
        var html_data = "";
        mydiv = document.getElementById('ta_status');
        for (var i = 0; i< Object.keys(data).length; i++) {

            var ta_net_id = data[i]["net_id"];
            var ta_status = data[i]["status"];
            var ta_name = data[i]['name'];
            id_add = ta_net_id;
            id_remove = ta_net_id ;
            path = "../static/data/img/" + ta_net_id + ".jpg";
            html_data = html_data.concat('<div class = "row"></div><a class="btn-floating btn-large green" onclick = \"add_queue(this);\" id = \"');
            html_data = html_data.concat(id_add);
            html_data = html_data.concat('\">Join</a>');
            html_data = html_data.concat('<a class="btn-floating red btn-large" onclick = \"remove_queue(this');
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

function remove_queue(id){
    // console.log("in remove");
    socket.emit('remove_student', {"net_id":id.id});
}

function add_queue(id){
    /**
     Emits a socket io call to add a student to a TA's queue
    **/
    socket.emit('add_student', {"net_id":id.id});
}

function get_ta_queue(data){
    /**
     * Update the queue for a given TA
     */
    console.log("Updating Queue");
    console.log(data);
    if (Object.keys(data).length > 0 ){
       var html_data = "<h5>Queue</h5><br>";
        var parser =  document.createElement('a');
        parser.href = window.location.href;
        var ta = parser.pathname.split('/')[2];
        mydiv = document.getElementById('ta_queue');
        for (var i = 0; i< Object.keys(data).length; i++) {
            if(data[i]['ta'] == ta) {
                var student_net_id = data[i]["student"];
                html_data = html_data.concat('<blockquote style = "float:left;"><a class="waves-effect waves-light btn blue darken-4" onclick = \"answerstudent(this);\" id = \"');
                html_data = html_data.concat(student_net_id);
                html_data = html_data.concat('\">Answer</a><text style = "font-size:18px; margin-left:15px;">');
                html_data = html_data.concat(student_net_id);
                html_data = html_data.concat('</text></blockquote><br><br>');
            }
        }
        if (data[0]['ta'] == ta){
            $(mydiv).html("");
            $(mydiv).html(html_data);
        }

    }
    else{
        $(mydiv).html("");

    }

}

function answerstudent(id) {
    var parser =  document.createElement('a');
    parser.href = window.location.href;
    var ta = parser.pathname.split('/')[2];
    console.log(id.id);
    socket.emit('answer_student', {"net_id":id.id, "ta": ta});

}