$(document).ready(function(){
    if ($(".user_msg").length > 0) {
        $("#login-link").addClass("hidden");
        $("#logout-link").addClass("visible");
    }
    else {
        $("#login-link").addClass("visible");
        $("#logout-link").addClass("hidden");
    }
});