/**
 * Created by Aadhya on 4/20/16.
 */
var socket;
$(document).ready(function() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/queue'); // Connect to socket.io server
    socket.on('connect', function () {
            socket.emit('loginTA', {});
        }
    )});