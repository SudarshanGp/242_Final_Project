/**
 * Created by Aadhya on 4/20/16.
 */
var socket;
//$(document).ready(function() {
//    socket = io.connect('http://' + document.domain + ':' + location.port + '/queue'); // Connect to socket.io server
//    socket.on('connect', function () {
//            socket.emit('loginTA', {});
//        }
//    )});

function manage_log_status(status){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/queue'); // Connect to socket.io server
    if (status == "Login"){
        console.log("Logging In");
        window.location.href = "http://localhost:5000/Login/";
    }
    else{
        console.log("Logging Out");
        $.ajax({
            url:"/Logout/",
            method:"post",
            success:function(data){
                socket.emit('loginTA', {});
                window.location.href = "http://localhost:5000/"
            }
        });

    }
}