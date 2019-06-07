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
    });
    
    $('#ing-btn').click(function() {
        var inginput = `<div class="form-inline">
                <label class="sr-only" for="ingredient">Ingredient</label>
                <input type="text" class="form-control mb-2 mr-sm-2" id="ingredient" name="ingredient" placeholder="Ingredient">
                <label class="sr-only" for="amount">Ingredient</label>
                <input type="text" class="form-control mb-2 mr-sm-2" id="amount" name="amount" placeholder="e.g. 100g">
                <a class="btn" id="ing-btn">Add Ingredient</a>
            </div>`
        $(this).parent().append(inginput);
    });
    /*
    
    $.ajax({
        type: "POST",
        data: "submit=1&username="+username+"&email="+email+"&password="+password+"&passconf="+passconf,
        url: "http://rt.ja.com/includes/register.php",
        success: function(data)
        {   
            //alert(data);
            $('#userError').html(data);
            $("#userError").html(userChar);
            $("#userError").html(userTaken);
        }
    });
    
    */
    
    
});
    
