var timeslots = []
var lang = document.currentScript.getAttribute('data-lang');
var time_left = 0.0
var hour = 0
var minute = 0


$(document).ready(function() {
  // Mudar horas restantes
  $('input[name="regime"]').click(function() {
    $('#hour-regime').val('');
    var valor = $(this).val();
    if (valor == 'rde' || valor == '40') {
      $('#hour-regime').text(40.0);
      $('#min-regime').text(00);
      time_left = 40.0;
    } else {
      $('#hour-regime').text(20.0);
      $('#min-regime').text(00);
      time_left = 20.0;
    }

    if ($('#error-alert-form').is(':visible')) {
      $('#error-alert-form').hide();
      $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').removeClass('disabled').removeAttr('aria-disabled');
      $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').prop('disabled', false);
    }
  });

  // Limpar formulário inteiro
  $('#cleanFPA').click(function() {
    $('input[name="regime"]').prop('checked', false);
    $('.checkbox input[type="checkbox"]').prop('checked', false);
    $('label.checkbox').removeClass('active');
    $('#hour-regime').text("--");
    $('#min-regime').text("--");
    $('#error-alert-form').hide();

    window.scrollTo({
      top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
      behavior: 'smooth'
    });

    timeslots.length = 0;
    time_left = 0;
  });

  function atualizar_time_left(is_checked, value) {
    if(!is_checked) {
      time_left -= value;
      time_left = parseFloat(time_left.toFixed(2));
      transformar_hora();
      $('#hour-regime').text(hour);
      $('#min-regime').text(minute);
    }
  }

  function transformar_hora() {
    hour = Math.floor(time_left);
    minute = Math.round((time_left - hour) * 60);
    alert(hour, minute);
  }

  // Pegar dados dos checkboxes
  $('.checkbox').click(function() {
    if(time_left == 00) {
      $('#hour-regime').text("--");
      $('#min-regime').text("--");
      $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').addClass('disabled').attr('aria-disabled', 'true');
      $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').prop('disabled', true);

      $('#error-message-form').text('Insira o regime de trabalho antes de continuar.');
      $('#error-alert-form').show();
      window.scrollTo({
        top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
        behavior: 'smooth'
      });
    } else {
      var input_id = $(this).attr('for');
      var input_val = $('#' + input_id).val();
      var is_checked = $('#' + input_id).prop('checked');

      if(is_checked) {
        time_left = (parseFloat(time_left) + 0.45).toFixed(2);
        timeslots.pop();
        transformar_hora();
        $('#hour-regime').text(hour);
        $('#min-regime').text(minute);
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

  $('#sendFPA').click(function() {
    var work_regime =  $('input[name="regime"]:checked').val();


    let csrftoken = getCookie('csrftoken');

    if (work_regime && timeslots.length !== 0) {
      $.ajax({
        type: 'POST',
        url: 'professor/preferencia-atribuicao/ver-fpa/',
        data: {
          work_regime: work_regime,
          work_timeslot: [...timeslots]
        },
        headers: {
          'X-CSRFToken': csrftoken
        },
        success: function(response) {
          $('input[name="regime"]:checked').prop('checked', false);
          $('#error-alert-form').hide();
          alert("foi");
          window.location.href = '/' + lang + '/professor/preferencia-atribuicao/ver-fpa/';
        },
        error: function(xhr, status, error) {
          $('#error-message-form').text('Ocorreu um erro no envio de FPA.');
          $('#error-alert-form').show();
          window.scrollTo({
            top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
            behavior: 'smooth'
          });
        }
      });
    } else {
      $('#error-message-form').text('Insira as informações pedidas em cada seção.');
      $('#error-alert-form').show();
      window.scrollTo({
        top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
        behavior: 'smooth'
      });
    }
  });

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

