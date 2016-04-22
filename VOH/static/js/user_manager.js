var socket;

// Managing the click of the Login/Logout button on the Navigation menu
// If the user is logging in then redirect the user to the login page
// If the user is logging out then call Flask via ajax to clear the sessions then reload the online TA queue
// If the user logging out is a TA then emit signal to alert all students that the TA is logging out and clear
// the TAs queue
// If the user logging out is a student then emit signal to remove student from all queues he is a part of
// Redirect logging out users to the main homepage

function manage_log_status(status){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/queue');
    if (status == "Login"){
        console.log("Logging In");
        window.location.href = 'http://' + document.domain + ':' + location.port +"/Login/";
    }
    else{
        console.log("Logging Out");
        $.ajax({
            url:"/Logout/",
            method:"post",
            success:function(data){
                socket.emit('loginTA', {});
                if( window.location.href.includes('/TA/')){

                    socket.emit('logout_alert',{"name":data["name"]});
                }
                else{
                    socket.emit('student_logout',{});
                }

                window.location.href = "http://localhost:5000/"
            }
        });

    }
}