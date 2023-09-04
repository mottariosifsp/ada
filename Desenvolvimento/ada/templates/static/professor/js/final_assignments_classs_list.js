var json_data = document.currentScript.getAttribute("jsonData");
json_data = decodeURIComponent(JSON.parse('"' + json_data + '"'));
console.log("Json data", JSON.parse(json_data));

$('.header-table').closest('table').find('.header-days').hide();
$('.header-table').closest('table').find('tbody').hide();

$(document).ready(function () {

    $('#rectangle-container').hide();

    var jsonData = JSON.parse(json_data);
    var json_array = Array.isArray(jsonData) ? jsonData : [jsonData];

    $('.square').click(function () {
        var registrationAreaId = $(this).data('registration_area_id');
        console.log('Clicked square with registration_area_id:', registrationAreaId);

        var filteredData = json_array.filter(function (objeto) {
            return objeto.registration_area_id === registrationAreaId;
        });

        $('#rectangle-container').empty();

        filteredData.forEach(function (objeto) {
            var rectangle = $('<div class="rectangle"></div>').text(objeto.registration_class_id);
            let isUpdating = false;

        rectangle.click(function () {
            var valorDoElementoClicado = $(event.target).text().trim();
            console.log("valor do elemento clicado", valorDoElementoClicado);


            var novaURL = "/professor/ver/?registration_class_id=" + valorDoElementoClicado;
            window.location.href = novaURL;

        });

            $('#rectangle-container').append(rectangle);
        });

        $('#rectangle-container').show();


    });

});
