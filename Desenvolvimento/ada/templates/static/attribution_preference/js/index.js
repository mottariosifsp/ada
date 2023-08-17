var disponilibity_done = document.currentScript.getAttribute("disponilibity_done");
var seconds = document.currentScript.getAttribute("seconds");
var lang = document.currentScript.getAttribute("data-lang");

if (disponilibity_done == 'False') {
    $(document).ready(function() {
        $('.overlay').css('display', '');
        $('#container *').prop('disabled', true);
        $('#container div.card').css('opacity', '0.4');
    });
}

function updateTimer() {
    seconds--;
  
    if (seconds === 0) {
        let minutes = parseInt(document.getElementById("cel-minute").textContent);
        minutes--;
        
        if (minutes === 0) {
            let hours = parseInt(document.getElementById("cel-hour").textContent);
            hours--;
    
            if (hours === 0) {
                let days = parseInt(document.getElementById("cel-day").textContent);
                days--;
    
                if (days === 0) {
                    window.location.reload();
                }
    
                $('#cel-day').text(days);
                hours = 24;
            }
    
            $('#cel-hour').text(hours);
            minutes = 60;
        }
    
        $('#cel-minute').text(minutes);
        seconds = 60;
    } else {
        setTimeout(updateTimer, 1000);
    }
}
updateTimer();

function open_case(value) {
    var buttonElement = document.querySelector(".button-" + value);
    var isCaretDown = buttonElement.classList.contains('fa-caret-down');
    if(value == 1) {
        if (isCaretDown) {
            $('.diponibility-case').css({
                'display': 'block'
            });
            window.scrollTo({
                top: $(".diponibility-case").offset().top - $(".navbar").outerHeight() - 30,
                behavior: "smooth",
            });
            $('.button-' + value).removeClass('fa-caret-down').addClass('fa-sort-up');
        } else {
            $('.diponibility-case').css({
                'display': 'none'
            });
            $('.button-' + value).removeClass('fa-sort-up').addClass('fa-caret-down');
        }
    } else if(value == 2) {
        if (isCaretDown) {
            $('.courses-case').css({
                'display': 'block'
            });
            window.scrollTo({
                top: $(".diponibility-case").offset().top - $(".navbar").outerHeight() - 30,
                behavior: "smooth",
            });
            $('.button-' + value).removeClass('fa-caret-down').addClass('fa-sort-up');
        } else {
            $('.courses-case').css({
                'display': 'none'
            });
            $('.button-' + value).removeClass('fa-sort-up').addClass('fa-caret-down');
        }
    } else {
        if (isCaretDown) {
            $('.final-case').css({
                'display': 'block'
            });
            window.scrollTo({
                top: $(".diponibility-case").offset().top - $(".navbar").outerHeight() - 30,
                behavior: "smooth",
            });
            $('.button-' + value).removeClass('fa-caret-down').addClass('fa-sort-up');
        } else {
            $('.final-case').css({
                'display': 'none'
            });
            $('.button-' + value).removeClass('fa-sort-up').addClass('fa-caret-down');
        }
    }
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

