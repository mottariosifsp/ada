
var disponilibity_done = document.currentScript.getAttribute("disponilibity_done");
var lang = document.currentScript.getAttribute("data-lang");

if(disponilibity_done == 'False') {
    $(document).ready(function() {
        $('.overlay').css('display', '');
        $('#container *').prop('disabled', true);
        $('#container div.card').css('opacity', '0.4');
    });
}



function fpa_blockk_animation() {
    window.scrollTo({
        top: $("#fpa-blockk").offset().top - $(".navbar").outerHeight() - 30,
        behavior: "smooth",
    });
}

function fpa_disponibility_animation() {
    window.scrollTo({
        top: $("#disponibility-block").offset().top - $(".navbar").outerHeight() - 30,
        behavior: "smooth",
    });
    $("#disponibility-block").css({
        "border": "1px solid #507c75"
    });
}

