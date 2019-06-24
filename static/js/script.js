$(document).ready(function(){
    // Get username in session and change navbar links
    fetch("/login")
    .then((resp) => resp.json())
    .then(function(data){
            $("#login-link").addClass("hidden");
            $("#signup-link").addClass("hidden");
            $("#logout-link").removeClass("hidden");
            $("#search-link").removeClass("hidden");
            $("#user-welcome").html(`Welcome `+ (data) + ` - Home`);
        }
    )
    .catch(function() {
   
    });
    
    
    // Add ingredient form will add extra inputs on add-recipe
    $('#ing-btn').click(function(event) {
        event.preventDefault();
        let inginput = `<div class="form-inline">
                <label class="sr-only" for="ingredient">Ingredient</label>
                <input type="text" class="form-control mb-2 mr-sm-2" id="ingredient" name="ingredient" placeholder="Ingredient">
                <label class="sr-only" for="amount">Ingredient</label>
                <input type="text" class="form-control mb-2 mr-sm-2" id="amount" name="amount" placeholder="e.g. 100g">
            </div>`;
        $(".ing-group").append(inginput);
    });
    
    // Any button labelled cancel will take the user back
    $('.cancel-btn').click(function() {
        history.back(-1);
    });
    if (window.location.href.indexOf("/like_recipe") > -1) {
        $(".cancel-btn").attr("id", "cancel-cancel");
    }
    $('#cancel-cancel').click(function() {
        history.back(-2);
    });
    
    // User can click on checkbox text to select checkbox
    $('.form-check').click(function() {
        $(this).prop('checked');
    });
    
    // Filter results on results page
    $("#checkgluten").on("click", function() {
        if ($(this).prop("checked")) {
            $(".r-card-text:not(:contains('Gluten-free'))").parents(".r-card-col:visible").addClass("hidden");
        }
        else {
            $(".r-card-text:not(:contains('Gluten-free'))").parents(".r-card-col").removeClass("hidden")
        }
    });
    $("#checkvegan").on("click", function() {
        if ($(this).prop("checked")) {
            $(".r-card-text:not(:contains('Vegan'))").parents(".r-card-col:visible").addClass("hidden")
        }
        else {
            $(".r-card-text:not(:contains('Vegan'))").parents(".r-card-col").removeClass("hidden")
        }
            
    });
    $("#checkdairy").on("click", function() {
        if ($(this).prop("checked")) {
            $(".r-card-text:not(:contains('Dairy-free'))").parents(".r-card-col:visible").addClass("hidden")
        }
        else {
            $(".r-card-text:not(:contains('Dairy-free'))").parents(".r-card-col").removeClass("hidden")
        }
    });
    $("#checkquick").on("click", function() {
        if ($(this).prop("checked")) {
            $(".r-card-text:not(:contains('under 30 mins'))").parents(".r-card-col:visible").addClass("hidden");
        }
        else {
            $(".r-card-text:not(:contains('under 30 mins'))").parents(".r-card-col").removeClass("hidden");
        }
    });
    
    $("#reset-btn").on('click', function() {
       $(".r-card-col").removeClass("hidden");
       $(".filter-check:checked").prop("checked", false);

    });
    
    // Change results display on filter
    $("input:checkbox").change(function() {
        var cards = $('.r-card:visible').length;
        $('.result-count').html(cards);
    });
    $("#reset-btn").click(function() {
        var cards = $('.r-card:visible').length;
        $('.result-count').html(cards);
    });
    
    // Provide quick link to search again if there are 0 results
    
    
});
    
