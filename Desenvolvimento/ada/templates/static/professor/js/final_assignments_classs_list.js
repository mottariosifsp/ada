var timetables_user = document.currentScript.getAttribute("timetables-user");
var timetables_user = JSON.parse(timetables_user);
console.log("timetables_user", timetables_user);

var timeslots = document.currentScript.getAttribute("timeslots");
console.log("Timeslots", timeslots);

var timetable_json = document.currentScript.getAttribute("timetable_json");
console.log("timetable_json data", JSON.parse(timetable_json));

var json_data = document.currentScript.getAttribute("jsonData");
json_data = decodeURIComponent(JSON.parse('"' + json_data + '"'));
console.log("Json data", JSON.parse(json_data));

$('.header-table').closest('table').find('.header-days').hide();
$('.header-table').closest('table').find('tbody').hide();

$.each(timetables_user, function (index, value) {

    let professor = value.professor;

    $("#cel-" + value.cord).html("<strong>" + value.acronym + "</strong>" + "<br>" + professor);
    $("#cel-" + value.cord).closest('table').find('.header-days').show();
    $("#cel-" + value.cord).closest('table').find('tbody').show();
    // console.log(value.cord);
    // console.log(value.course);
});

$('.header-table').closest('table').find('.header-days').hide();
$('.header-table').closest('table').find('tbody').hide();

$.each(timetables_user, function (index, value) {

    let professor = value.professor;

    $("#cel-" + value.cord).html("<strong>" + value.acronym + "</strong>" + "<br>" + professor);
    $("#cel-" + value.cord).closest('table').find('.header-days').show();
    $("#cel-" + value.cord).closest('table').find('tbody').show();
    // console.log(value.cord);
    // console.log(value.course);
});

$(document).ready(function () {

    $('#rectangle-container').hide();
    var jsonData = JSON.parse(json_data);
    var json_array = Array.isArray(jsonData) ? jsonData : [jsonData];

    function showCard() {
        $('.card').removeClass('hidden');
    }

    function hideCard() {
        $('.card').addClass('hidden');
    }

    $('.square').click(function () {
        var registrationAreaId = $(this).data('registration_area_id');
        console.log('Clicked square with registration_area_id:', registrationAreaId);

        var filteredData = json_array.filter(function (objeto) {
            return objeto.registration_area_id === registrationAreaId;
        });

        $('#rectangle-container').empty();

        filteredData.forEach(function (objeto) {
            var rectangle = $('<div class="rectangle"></div>').text(objeto.registration_class_id);

            rectangle.click(function () {
                showCard();
            });

            $('#rectangle-container').append(rectangle);
        });

        $('#rectangle-container').show();

        $('.square').click(function () {
            hideCard();
        });


    });
    // console.log(tametables_user)

    $('.header-table').click(function () {
        $(this).find('.icon-minimize').text('-');
        $(this).closest('table').find('.header-days').toggle();
        $(this).closest('table').find('tbody').toggle();
        if ($(this).closest('table').find('.header-days').is(":visible")) {
            $('html, body').animate({
                scrollTop: $(this).closest('table').offset().top - 100
            }, 600);

        } else {
            $(this).find('.icon-minimize').text('+');
        }
    });

});
