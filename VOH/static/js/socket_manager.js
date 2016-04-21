// @author : Sudarshan Govindaprasad

// MOTIVATION FROM FLASK-SOCKETIO DOCUMENTATION
var socket;
$(document).ready(function(){
    console.log("here");
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
    // TODO : editor.session.replace(new Range(row, 0, row, Number.MAX_VALUE), newText)


    
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat_session'); // Connect to socket.io server
    socket.on('connect', function() {
        // Retrive generated url link from browser
        var parser =  document.createElement('a');
        parser.href = window.location.href;
        console.log(parser);
        console.log("HI")
        var unique_id = parser.pathname.split('/')[1]; // should be 2
        console.log(parser.pathname.split('/'));
        console.log(unique_id);
        socket.emit('join', {'room': unique_id}); // On connect of a new user, emit join signal to socket.io server
    });
     editor.on("change", function(e){
       console.log(e);
        socket.emit('editor_change', {'change' : e});
    });
    socket.on('editor_change_api', function(data){
       console.log("CHANGE RECEIVED");
        console.log(data);
    });

    /**
     * On status being emitted by socket.io server, this function catches the join information and
     * adds it to the chat message box
     */
    socket.on('status', function(data) {
        console.log("HERE");
        $('#chat').val($('#chat').val() + '' + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    /**
     * On a new message being emitted by socket.io server, this function
     * catches it and appends it to the chat box
     */
    socket.on('message', function(data) {
        console.log("message "  + data);
        $('#chat').val($('#chat').val() + data.msg + '\n');
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
            console.log('emitting ' + text);
            socket.emit('text', {msg: text});
        }
    });
});

/**
 * When a user leaves the room, socket is disconnected and user is redirected to a common page
 */
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        var redirect ='http://' + document.domain + ':' + location.port + '/';
        window.location.href = redirect;
    });
}