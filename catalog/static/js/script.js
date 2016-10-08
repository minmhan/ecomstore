$(function(){
    $("#submit_review").click(addProductReview);
    $("#review_form").addClass('hidden');
    $("#add_review").click(slideToggleReviewForm);
    $("#cancel_review").click(slideToggleReviewForm);
    statusBox();
})

function statusBox(){
    $("<div id='loading'>Loading...</div>")
        .prependTo("#main")
        .ajaxStart(function() { $(this).show();})
        .ajaxStop(function() { $(this).hide();})
}


function slideToggleReviewForm(){
    $("#review_form").slideToggle();
    $("#add_review").slideToggle();
}

function addProductReview(){
    var review = {
        title: $("#id_title").val(),
        content: $("#id_content").val(),
        rating: $("#id_rating").val(),
        slug: $("#id_slug").val()
    };

    $.post("/review/product/add/", review,
        function(response){
            $("#review_errors").empty();
            if(response.success == "True"){
                $("#submit_review").attr('disabled', 'disabled');
                $("#no_reviews").empty()
                $("#reviews").prepend(response.html).slideDown();
                new_review = $("#reviews").children(":first");
                new_review.addClass('new_review');
                $("#review_form").slideToggle();
            }
            else{
                $("#review_errors").append(response.html);
            }
        }, "json");
}


// TODO: Clean up
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});