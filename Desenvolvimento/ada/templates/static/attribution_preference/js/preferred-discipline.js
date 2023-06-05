var timeslots = []
var lang = document.currentScript.getAttribute('data-lang');
var time_left = 0.0


$(document).ready(function() {
  // Mudar horas restantes
  $('input[name="regime"]').click(function() {
    $('#hour-regime').val('');
    var valor = $(this).val();
    if (valor == 'rde') {
      $('#hour-regime').text(40.0);
      time_left = 40.0
    } else {
      $('#hour-regime').text(valor);
      time_left = valor
    }
  });

  // Limpar formulário inteiro
  $('#cleanFPA').click(function() {
    $('input[name="regime"]').prop('checked', false);
    $('.checkbox input[type="checkbox"]').prop('checked', false);
    $('label.checkbox').removeClass('active');

    timeslots.length = 0;
  });

  function atualizar_time_left(is_checked, value) {
    if(!is_checked) {
      time_left -= value;
      $('#hour-regime').text(time_left);
    }
  }

  // Pegar dados dos checkboxes
  $('.checkbox').click(function() {
    if(time_left == 00) {
      $('#hour-regime').text("?");
    } else {
      var input_id = $(this).attr('for');
      var input_val = $('#' + input_id).val();
      var is_checked = $('#' + input_id).prop('checked');

      if(is_checked) {
        time_left += 0.45;
        $('#hour-regime').text(time_left);
      } else {
        var [objeto_elemento, dia_elemento] = input_val.split(',');

        var aula = {
          hora_começo: objeto_elemento,
          dia_semana: dia_elemento
        };

        timeslots.push(aula);
        atualizar_time_left(is_checked, 0.45);
      }    
    }
  });  
});

