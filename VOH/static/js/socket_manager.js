// @author : Sudarshan Govindaprasad

// MOTIVATION FROM FLASK-SOCKETIO DOCUMENTATION
var loaded_archive = false;
var ta = false;
var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat_session'); // Connect to socket.io server
    socket.on('connect', function() {
        // Retrive generated url link from browser
        var parser =  document.createElement('a');
        parser.href = window.location.href;
        var unique_id = parser.pathname.split('/')[2]; // should be 2
        socket.emit('join', {'room': unique_id}); // On connect of a new user, emit join signal to socket.io server
    });

    /**
     * On status being emitted by socket.io server, this function catches the join information and
     * adds it to the chat message box
     */ 
    socket.on('status', function(data) {
        console.log(data);
        var data_html = "<p style = 'text-align: center;'>"+data.msg+"</p>";
        message = $.parseHTML(data_html);
        $('#chat').append(message);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
        old_messages = data.old;
        if(loaded_archive == false){
            message = $.parseHTML( "<p style = 'text-align: center;'> Old Archived Messages</p>");
            $('#chat').append(message);
            old_messages.forEach(function(d){
                var data_html = "";
                if(d.type == "TA"){
                    ta = true;
                    data_html = "<p style = 'text-align: right; padding-right: 10px;'>"+d.by + ": " + d.message.msg+"</p>";
                }
                else{
                   data_html = "<p style = 'text-align: left; padding-left: 10px;'>"+d.by + ": " +d.message.msg+"</p>";
                }
                message = $.parseHTML(data_html);

                $('#chat').append(message);
            });
            loaded_archive = true;
        }
        message = $.parseHTML( "<p style = 'text-align: center;'> Start New Conversation</p>");
        $('#chat').append(message);

        if (data.type == "TA") {
            socket.emit('get_student_list', {"ta": data.net_id, "type":data.type})
        }
        
        
    });

    socket.on('load_student_list', function(data){
        var mydiv = document.getElementById("student_list");
        var student_list = data["student_list"];
        var html_data = "<h6>Students on your queue</h6>";
        student_list.forEach(function(d){
                var student_net_id = d["student"];
                html_data = html_data.concat('<blockquote style = "float:left;">');
                html_data = html_data.concat(student_net_id);
                html_data = html_data.concat('</blockquote><br>');
        });
        // Updates HTML Div
        $(mydiv).html("");
        if(data["type"] == "TA"){
            console.log("is a ta");
            $(mydiv).html(html_data);
        }
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
        message = $.parseHTML(data_html);
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