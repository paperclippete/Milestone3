$(document).ready(function(){
    //Get username in session and change navbar links
    $.ajax({
            type: "GET",
            url: "/login",
            success: function(data) {
                console.log(data);
                $("#login-link").addClass("hidden");
                $("#signup-link").addClass("hidden");
                $("#logout-link").removeClass("hidden");
                $("#add-recipe-link").removeClass("hidden");
                $("#user-home-link").removeClass("hidden");
                $("#user-welcome").html(`Welcome `+ (data));
            }
})});
    
