// @author : Sudarshan Govindaprasad

// MOTIVATION FROM FLASK-SOCKETIO DOCUMENTATION

var socket;
$(document).ready(function(){
    console.log("here");

    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat_session'); // Connect to socket.io server
    socket.on('connect', function() {
        // Retrive generated url link from browser
        var parser =  document.createElement('a');
        parser.href = window.location.href;
        var unique_id = parser.pathname.split('/')[2]; // should be 2
        console.log("UNIQUE ROOM ID " + unique_id);
        socket.emit('join', {'room': unique_id}); // On connect of a new user, emit join signal to socket.io server
    });


    /**
     * On status being emitted by socket.io server, this function catches the join information and
     * adds it to the chat message box
     */
    socket.on('status', function(data) {

        var data_html = "<p style = 'text-align: center;'>"+data.msg+"</p>";
        message = $.parseHTML(data_html);
        $('#chat').append(message);
        console.log($('#chat').scrollTop($('#chat')[0].scrollHeight));
    });

    /**
     * On a new message being emitted by socket.io server, this function
     * catches it and appends it to the chat box
     */
    socket.on('message', function(data) {
        console.log("message "  + data);
        var msg = linkifyHtml(data.msg, {
         defaultProtocol: 'https'
        });
        var data_html = "";
        if(data.type == "TA"){
            data_html = "<p style = 'text-align: right; padding-right: 10px;'>"+msg+"</p>";
        }
        else{
           data_html = "<p style = 'text-align: left; padding-left: 10px;'>"+msg+"</p>";
        }
        // var message = linkifyHtml(data_html, {
        //  defaultProtocol: 'https'
        // });
        message = $.parseHTML(data_html);
        console.log(message);
        console.log(message.innerHTML);
        console.log(typeof(message));
        
        
        $('#chat').append(message);
        var objDiv = document.getElementById("chat");
        objDiv.scrollTop = objDiv.scrollHeight;

    });

    /**
     * On Key Press of enter, message is retrieved from textbox (text) and emit signal with message is sent to
     * socket.io server
     */
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});
        }
    });
});

/**
 * When a user leaves the room, socket is disconnected and user is redirected to a common page
 */
function leave_room(data, rating_for, rating_by) {
    rating = ($('input[name=rating]:checked','#rate').val());
    console.log(rating_for);
    console.log(rating_by);
    socket.emit('add_rating_to_db',{"rating_for":rating_for, "rating_by":rating_by, "rating":rating});
    socket.emit('left', {}, function() {
        socket.disconnect();
        var redirect ='http://' + document.domain + ':' + location.port + '/';
        window.location.href = redirect;
    });
}