
var disponilibity_done = document.currentScript.getAttribute("disponilibity_done");
var lang = document.currentScript.getAttribute("data-lang");

if(disponilibity_done == 'False') {
    $(document).ready(function() {
        $('.overlay').css('display', '');
        $('#container *').prop('disabled', true);
        $('#container div.card').css('opacity', '0.4');
    });
}
function normalizeTime(days, hours, minutes) {
    while (minutes >= 60) {
        hours++;
        minutes -= 60;
    }

    while (hours >= 24) {
        days++;
        hours -= 24;
    }

    while (minutes < 0) {
        hours--;
        minutes += 60;
    }

    while (hours < 0) {
        days--;
        hours += 24;
    }

    return { days, hours, minutes };
}

function updateCountdown() {
    const countdownElements = {
        days: document.getElementById('days'),
        hours: document.getElementById('hours'),
        minutes: document.getElementById('minutes')
    };

    const currentDate = new Date();
    const targetDate = new Date(2023, 8, 31, 18, 0, 0); // Substitua com a sua data
    const timeDifference = targetDate - currentDate;

    const { days, hours, minutes } = normalizeTime(0, 0, Math.floor(timeDifference / (1000 * 60)));

    countdownElements.days.textContent = days;
    countdownElements.hours.textContent = hours;
    countdownElements.minutes.textContent = minutes;

    setTimeout(updateCountdown, 60000); // Agendando a atualização a cada minuto
    alert()
}

updateCountdown();

function open_case(value) {
    
    if(value == 1) {
        $('.diponibility-case').css({
            'display': 'block'
        });
        window.scrollTo({
            top: $(".diponibility-case").offset().top - $(".navbar").outerHeight() - 30,
            behavior: "smooth",
        });
        $('.button-1').removeClass('fa-caret-down').addClass('fa-sort-up');alert("h")

    } else if(value == 2) {

    } else {

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

