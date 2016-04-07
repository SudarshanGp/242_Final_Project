var socket;

$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    console.log(socket);
    socket.on('connect', function() {
        console.log("EMIT CONNECT JOINED");
        socket.emit('joined', {});
    });
    socket.on('status', function(data) {
        console.log("ON STATUS");
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        console.log("ON MESSAGE");
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#text').keypress(function(e) {
        console.log("ON TEXT ENTER");
        var code = e.keyCode || e.which;
        if (code == 13) {
            console.log("YOU PRESSED ENTER");
            text = $('#text').val();
            console.log(text);
            $('#text').val('');
            socket.emit('text', {msg: text});
        }
    });
});

function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('index') }}";
    });
}