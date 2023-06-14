var timeslots = []
var lang = document.currentScript.getAttribute('data-lang');
var cel_left = 0
var type_cel = 0
var cel_final = "not_checked"
var hour = 0
var minute = 0
var user_blocks = document.currentScript.getAttribute('blocks');
var user_timetables = document.currentScript.getAttribute('timetables');

$(document).ready(function() {

  var timetables = JSON.parse(user_timetables)
  console.log("Timetables",timetables)
  marcarCombos(1);

  function turnCheckboxLabelActive(checkboxId) {
    var checkbox  = document.getElementById(checkboxId);
    checkbox.checked = true;
    var label = document.querySelector('label[for="' + checkboxId + '"]');
    label.classList.add('active');
  }

  function marcarCombos(position) {
    console.log("Entrou no marcar combos");
    for (i = 1; i <= timetables.length - 1; i++) {
      if (timetables[i].timeslot_position == 1 ) {
        console.log("parou na posicao 1");
        if (timetables[i+1].classs == timetables[i].classs && timetables[i+1].course == timetables[i].course ) {
          console.log("marcou o primeiro");
          var checkboxId = "mon-mat-2";
          turnCheckboxLabelActive(checkboxId);
        }
        if (timetables[i+2].classs == timetables[i].classs && timetables[i+2].course == timetables[i].course ) {
          console.log("marcou o segundo");
          var checkboxId = "mon-mat-3";
          turnCheckboxLabelActive(checkboxId);
        }
      }
      console.log("Day", timetables[i].day);
    }
  }

  // Variáveis para saber a última posição de cada período
  var last_matutine_position = 0;
  var last_vespertine_position = 0;
  var last_nocturnal_position = 0;
  // console.log("Timetables", user_timetables);

  $('[id^="mon-mat"]').each(function() {
    var number = $(this).attr('id').split('-')[2];
    last_matutine_position = Number(number);
  });

  $('[id^="mon-ves"]').each(function() {
    var number = $(this).attr('id').split('-')[2];
    last_vespertine_position = last_matutine_position + Number(number);
  });

  $('[id^="mon-not"]').each(function() {
    var number = $(this).attr('id').split('-')[2];
    last_nocturnal_position = last_vespertine_position + Number(number);
  });

  console.log("Matutino", last_matutine_position);
  console.log("Vespertino", last_vespertine_position);
  console.log("Noturno", last_nocturnal_position);

  $('.checkbox').click(function() {
    // Pega o valor do id do input do checkbox
    var inputId = $(this).find('input').attr('id')
    console.log(inputId);

    // Segunda
    if(inputId.startsWith("mon-mat")) {
      var selectedCell = Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("mon-ves")) {
      var selectedCell = last_matutine_position + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("mon-not")) {
      var selectedCell = last_vespertine_position + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    // Terça
    if(inputId.startsWith("tue-mat")) {
      var selectedCell = last_nocturnal_position + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("tue-ves")) {
      var selectedCell = last_matutine_position + last_nocturnal_position + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("tue-not")) {
      var selectedCell =  last_vespertine_position + last_nocturnal_position + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    // Quarta
    if(inputId.startsWith("wed-mat")) {
      var selectedCell = last_nocturnal_position * 2 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("wed-ves")) {
      var selectedCell = last_matutine_position + last_nocturnal_position * 2 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("wed-not")) {
      var selectedCell =  last_vespertine_position + last_nocturnal_position * 2 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    // Quinta
    if(inputId.startsWith("thu-mat")) {
      var selectedCell = last_nocturnal_position * 3 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("thu-ves")) {
      var selectedCell = last_matutine_position + last_nocturnal_position * 3 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("thu-not")) {
      var selectedCell =  last_vespertine_position + last_nocturnal_position * 3 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    // Sexta
    if(inputId.startsWith("fri-mat")) {
      var selectedCell = last_nocturnal_position * 4 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("fri-ves")) {
      var selectedCell = last_matutine_position + last_nocturnal_position * 4 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("fri-not")) {
      var selectedCell =  last_vespertine_position + last_nocturnal_position * 4 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    // Sabado
    if(inputId.startsWith("sat-mat")) {
      var selectedCell = last_nocturnal_position * 5 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("sat-ves")) {
      var selectedCell = last_matutine_position + last_nocturnal_position * 5 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }

    if(inputId.startsWith("sat-not")) {
      var selectedCell =  last_vespertine_position + last_nocturnal_position * 5 + Number(inputId.split('-').pop());
      console.log("selectedCell", selectedCell)
    }
  });


  // Mudar horas restantes
  $('input[name="regime"]').click(function() {
    $('#cel-regime').val('');
    var valor = $(this).val();
    if (valor == 'rde' || valor == '40') {
      var this_duracao = 24*60/45;
      $('#cel-regime').text(this_duracao);
      cel_left = this_duracao
      type_cel = 40;
      cel_final = "not_checked"
      $('.checkbox input[type="checkbox"]').prop('checked', false);
      $('label.checkbox').removeClass('active');
      timeslots = []
    } else {
      var this_duracao = 12*60/45;
      $('#cel-regime').text(this_duracao);
      cel_left = this_duracao
      type_cel = 20;
      cel_final = "not_checked"
      $('.checkbox input[type="checkbox"]').prop('checked', false);
      $('label.checkbox').removeClass('active');
      timeslots = []
    }

    if ($('#error-alert-form').is(':visible')) {
      $('#error-alert-form').hide();
      $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').add('label[for^="sat-"]').removeClass('disabled').removeAttr('aria-disabled');
      $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').add('input[type="checkbox"][id^="sat-"]').prop('disabled', false);
    }
  });

  // Limpar formulário inteiro
  $('#cleanFPA').click(function() {
    $('input[name="regime"]').prop('checked', false);
    $('.checkbox input[type="checkbox"]').prop('checked', false);
    $('label.checkbox').removeClass('active');
    $('#cel-regime').text("--");
    $('#error-alert-form').hide();

    window.scrollTo({
      top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
      behavior: 'smooth'
    });

    timeslots.length = 0;
    cel_left = 0;
  });

  // Pegar dados dos checkboxes
  $('.checkbox').click(function() {
    if(cel_left == 0 && type_cel == 0) {
      $('#cel-regime').text("--");
      $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').add('label[for^="sat-"]').addClass('disabled').attr('aria-disabled', 'true');
      $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').add('input[type="checkbox"][id^="sat-"]').prop('disabled', true);

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
        cel_left += 1;
        var [objeto_elemento, dia_elemento] = input_val.split(',');
        var [inicio, fim] = objeto_elemento.split('-');

        if (cel_final == "checked") {
          $('input[type="checkbox"][id^="mon-"], input[type="checkbox"][id^="tue-"], input[type="checkbox"][id^="wed-"], input[type="checkbox"][id^="thu-"], input[type="checkbox"][id^="fri-"], input[type="checkbox"][id^="sat-"]').each(function() {
            if (!$(this).prop('checked')) {
              $(this).prop('disabled', false);
              $('label[for="' + $(this).attr('id') + '"]').removeClass('disabled').removeAttr('aria-disabled');
            }
          });
          cel_final = "not_checked"
          cel_left += 1

          $('#error-alert-form').hide();
        }

        var index = timeslots.findIndex(function(aula) {
          return aula.hora_comeco === inicio;
        });
        
        if (index !== -1) {
          timeslots.splice(index, 1);
        }

        $('#cel-regime').text(cel_left);
      } else {
        if(cel_final != "checked") {
          atualizar_cel_left(is_checked);
          if (cel_final != "checked") {
            var [objeto_elemento, dia_elemento] = input_val.split(',');
            var [inicio, fim] = objeto_elemento.split('-');
            var aula = {
              hora_comeco: inicio,
              hora_fim: fim,
              dia_semana: dia_elemento
            };

            timeslots.push(aula)
          }
        }
      }
    }
  });

  // Area e disponibilidade

  // $('#campoInputBlock').on('input', function() {
  //   var valor_selecionado = $(this).val();
  //   $('.block').each(function() {
  //     var block = $(this).attr('id').replace('block-', '');
  //     $(this).hide();

  //     var opcoes = $('#opcoes option').map(function() {
  //       return $(this).val();
  //     }).get();

  //     for (var i = 0; i < opcoes.length; i++) {
  //       if (block === opcoes[i]) {
  //         $(this).hide();
  //         break;
  //       }
  //     }

  //     $('#block-none').hide();
  //   });

  //   if (valor_selecionado == '' || valor_selecionado == null || valor_selecionado.length < 3) {
  //     $('#block-none').show();
  //   }

  //   $('#block-' + valor_selecionado).show();
  // });

  

  // Enviar formulário inteiro
  $('#sendDisponibility').click(function() {
    for (var i = 0; i < timeslots.length; i++) {
      alert(timeslots[i].hora_comeco);
    }
    var work_regime =  $('input[name="regime"]:checked').val();
    var jsonData = JSON.stringify(timeslots);

    let csrftoken = getCookie('csrftoken');

    if (work_regime && timeslots.length !== 0) {
      $.ajax({
        type: 'post',
        url: '/' + lang + '/professor/preferencia-atribuicao/criar-fpa/editar-cursos/',
        data: {
          work_regime: work_regime,
          work_timeslots: jsonData
        },
        headers: {
          'X-CSRFToken': csrftoken
        },
        success: function(response) {
          $('input[name="regime"]:checked').prop('checked', false);
          $('#error-alert-form').hide();
          window.location.href = '/' + lang + '/professor/preferencia-atribuicao/criar-fpa/editar-cursos/'
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

function atualizar_cel_left(is_checked) {
  if(!is_checked) {
    if (cel_final == "checked") {
      cel_left = 0;
      $('#cel-regime').text(cel_left);
    } else {
      cel_left -= 1;
      if(cel_left == -1) {
        $('input[type="checkbox"][id^="mon-"], input[type="checkbox"][id^="tue-"], input[type="checkbox"][id^="wed-"], input[type="checkbox"][id^="thu-"], input[type="checkbox"][id^="fri-"], input[type="checkbox"][id^="sat-"]').each(function() {
          if (!$(this).prop('checked')) {
            $(this).prop('disabled', true);
            $('label[for="' + $(this).attr('id') + '"]').addClass('disabled').attr('aria-disabled', 'true');
          }
        });
        $('#error-message-form').text('Você atingiu seu limite de disponibilidade.');
        $('#error-alert-form').show();
        window.scrollTo({
          top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
          behavior: 'smooth'
        });
        cel_final = "checked";
      } else {
        $('#cel-regime').text(cel_left);
      }
    }    
  }
}
