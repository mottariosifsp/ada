var timeslots = []
var lang = document.currentScript.getAttribute('data-lang');

$(document).ready(function() {
  $('.checkbox').click(function() {
    var input_id = $(this).attr('for');
    var input_val = $('#' + input_id).val();

    var [objeto_elemento, dia_elemento] = input_val.split(',');

    var aula = {
      hora_começo: objeto_elemento,
      dia_semana: dia_elemento
    };

    timeslots.push(aula);

    alert(aula);
  });
});