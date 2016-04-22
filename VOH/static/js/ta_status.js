var socket;
$(document).ready(function() {
    /**
     * All socket IO listeners that catch different emit calls in order to update
     * either the TA queue or the List of Online TA's
     */
    socket = io.connect('http://' + document.domain + ':' + location.port + '/queue'); // Connect to socket.io server
    socket.on('connect', function () {
        socket.emit('loginTA', {});
        socket.emit('getTAQueue', {});
        if (window.location.href.includes("/TA/")) {
            var parser =  document.createElement('a');
            parser.href = window.location.href;
            var ta = parser.pathname.split('/')[2];
            socket.emit('join', {"id" : ta});
        }
    });
    /**
     * Function acts as a debug check to check only if a TA has joined a room when
     * the TA logs in
     */
    socket.on('join_room_ta', function(data){
        console.log("hi, you joined the room and got messge " + data);

    });
    /**
     * Call back function is called when a user comes online.
     * The function updates updates information about the queue
     * and about which TAs are online
     */
    socket.on('online', function (data) {
        get_ta_status(data['online']);
        get_ta_queue(data['queue']);

    });
    /**
     * Add the student to a Queue and updates the queue structure
     * to reflect students on queue
     */
    socket.on('add_student_queue', function(data){
        if (window.location.href.includes("/TA/")) {
            if(data){
                get_ta_queue(data['queue']);
            }
        }
    });

    /**
     * When a TA/student is ready to start a chat, we need to disconnect them
     * from the correct socket connection and redirect them a new chat link that
     * is unique to their conversation
     */
    socket.on('start_chat', function(data){
        socket.disconnect();
        window.location.href = 'http://' + document.domain + ':' + location.port + '/chat' + '/' + data['room']+data['link'];

    });
    /**
     * Lister is used to catch student_join_emit signal which keeps track of a request from a TA asking a
     * student to join a room. This function will contact the socket io server with data about the chat room
     * the student is going to join
     */
    socket.on('student_join_emit', function(data){
        if (window.location.href.includes("/student/")) {
            var parser =  document.createElement('a');
            parser.href = window.location.href;
            var student = parser.pathname.split('/')[2]; // student
            if(student == data['student']){
                socket.emit('student_join', data);
            }
        }
    });

    socket.on('logout_alert', function(data){
        if (window.location.href.includes('student')){
            alert(data["message"]);
        }

    });

    socket.on('student_logout', function(data){
        if (window.location.href.includes('/TA/')){
            socket.emit('loginTA',{});
        }

    });

});

function get_ta_status(data) {
    /**
     * Updates the list of Online TA's for all clients
     */
    var parser =  document.createElement('a');
    parser.href = window.location.href;
    var ta_net_id = parser.pathname.split('/')[2]; // student
    var mydiv = document.getElementById('ta_status');
    if (data){
        var html_data = "";
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
     * Update the queue for a given TA's view
     */
    var parser =  document.createElement('a');
    parser.href = window.location.href;
    var ta_net_id = parser.pathname.split('/')[2]; // student
    var mydiv = document.getElementById('ta_queue');
    if (Object.keys(data).length > 0 ){
        var html_data = "<h5>Queue</h5><br>";
        var parser =  document.createElement('a');
        parser.href = window.location.href;
        var ta = parser.pathname.split('/')[2];
        for (var i = 0; i< Object.keys(data).length; i++) {
            if(data[i]['ta'] == ta) {
                console.log("here");
                console.log(data[i]);
                var student_net_id = data[i]["student"];
                html_data = html_data.concat('<blockquote style = "float:left;"><a class="waves-effect waves-light btn blue darken-4" onclick = \"answer_student(this);\" id = \"');
                html_data = html_data.concat(student_net_id);
                html_data = html_data.concat('\">Answer</a><text style = "font-size:18px; margin-left:15px;">');
                html_data = html_data.concat(student_net_id);
                html_data = html_data.concat('</text></blockquote><br><br>');
            }
        }

        $(mydiv).html("");
        $(mydiv).html(html_data);
    }
    else{
        $(mydiv).html("");

    }

}

/**
 * On clicking to answer a particular student, student is removed from queue and a
 * answer_student signal is emitted to the socket_io server
 * @param id keeps track of the id of the button that is clicked (student_id)
 */
function answer_student(id) {
    var parser =  document.createElement('a');
    parser.href = window.location.href;
    var ta = parser.pathname.split('/')[2];
    socket.emit('remove_student_answer', {net_id: id.id, ta:ta});
    socket.emit('answer_student', {"net_id":id.id, "ta": ta});

}
