// When the Instructor page is rendered, it makes an AJAX post to Flask to get the data regarging the ratings
// and hours logged by a TA as a JSON object. The data is then rendered using d3plus to different ids
$(document).ready(function(){
    $.ajax({
        url:"/get_ratings/",
        method:"post",
        success:function(data){
            var visualization = d3plus.viz()
                .container("#ratingviz")
                .data(data['ratings'])
                .type("bar")
                .id("name")
                .x("name")
                .y("score")
                .draw();
            var visualization = d3plus.viz()
                .container("#timeviz")
                .data(data['timings'])
                .type("bar")
                .id("name")
                .x("name")
                .y("time in minutes")
                .draw()
        }
    })

});