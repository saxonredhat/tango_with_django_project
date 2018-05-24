$(document).ready(function(){
   $("#about-btn").click( function(event) {
        $(this).addClass('btn btn-primary');
        $("#about-btn2").removeClass('btn btn-primary');
        msgstr = $("#msg").html()
        msgstr = msgstr + "!"
        $("#msg").html(msgstr)
   });
   $("#about-btn2").click( function(event) {
        $(this).addClass('btn btn-primary');
        $("#about-btn").removeClass('btn btn-primary');
        msgstr = $("#msg").html()
        re = new RegExp("(.*)!")
        msgstr = msgstr.replace(re,"$1")
        $("#msg").html(msgstr)

   });
});