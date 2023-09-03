var current_language = document.currentScript.getAttribute('data-lang');
var timeslots = []
var cell_left_number = 0
var cell_type_choosed = 0
var cell_situation = "not_checked"

var user_blocks = document.currentScript.getAttribute('blocks');
var user_timetables = document.currentScript.getAttribute('timetables');
var timeslot_minutes = document.currentScript.getAttribute('variation_minutes');
var max_quantity_cells = 11;
var cells_3_hours = document.currentScript.getAttribute('quantity_cells_3_hours');
var user_disponibility = JSON.parse(document.currentScript.getAttribute("user_disponibility").replace(/'/g, '"'));
var user_regime = document.currentScript.getAttribute("user_regime");
var eight_hours_passed;
var eleven_hours_passed;
var checkboxes = [];

  if (user_regime == '20') {
    const checkbox_element = document.querySelector('input[id="radio-20"]');
    checkbox_element.checked = true;
    var this_duration = 12*60/timeslot_minutes;
    $('#cel-regime').text(this_duration);
    cell_left_number = this_duration
    cell_type_choosed = 20;
    cell_situation = "not_checked"
  } else if (user_regime == '40') {
    const checkbox_element = document.querySelector('input[id="radio-40"]');
    checkbox_element.checked = true;
    var this_duration = 24*60/timeslot_minutes;
    $('#cel-regime').text(this_duration);
    cell_left_number = this_duration
    cell_type_choosed = 40;
    cell_situation = "not_checked"
  } else if (user_regime == 'RDE'){
    const checkbox_element = document.querySelector('input[id="rde"]');
    checkbox_element.checked = true;
    var this_duration = 24*60/timeslot_minutes;
    $('#cel-regime').text(this_duration);
    cell_left_number = this_duration
    cell_type_choosed = 40;
    cell_situation = "not_checked"
  } else if (user_regime == 'Temporário'){
    const checkbox_element = document.querySelector('input[id="temporario"]');
    checkbox_element.checked = true;
    var this_duration = 24*60/timeslot_minutes;
    $('#cel-regime').text(this_duration);
    cell_left_number = this_duration
    cell_type_choosed = 40;
    cell_situation = "not_checked"
  } else if (user_regime == 'Substituto') {
    const checkbox_element = document.querySelector('input[id="substituto"]');
    checkbox_element.checked = true;
    var this_duration = 12*60/timeslot_minutes;
    $('#cel-regime').text(this_duration);
    cell_left_number = this_duration
    cell_type_choosed = 20;
    cell_situation = "not_checked"
  }


for (var i = 0; i < user_disponibility.length; i++) {
  var obj = user_disponibility[i];
  var checked_id = obj.id;
  var checked_value = $('#' + checked_id).val();

  update_cell_left_number(false);
  var [checked_object, checked_day] = checked_value.split(',');
  var [timeslot_begin_hour, timeslot_end_hour] = checked_object.split('-');
  var lesson = {
    id: checked_id,
    timeslot_begin_hour: timeslot_begin_hour,
    timeslot_end_hour: timeslot_end_hour,
    day_of_week: checked_day,
  };

  checkboxes.push(lesson.id)
  timeslots.push(lesson)

  var checkbox = document.getElementById(checked_id);
  if (checkbox) {
    checkbox.checked = true;
    var button = checkbox.parentElement;
    var label = button.parentElement;
    button.classList.add("active");
    label.classList.add("active");
  }
  if(cell_left_number < 0) {
    $('.custom-icon').css('display', '');
    $('.cel-plus').css('display', '');
    $('.cel').css('display', 'none');
  } else {
    $('#cel-regime').text(cell_left_number);
    $('.custom-icon').css('display', 'none');
    $('.cel-plus').css('display', 'none');
    $('.cel').css('display', '');
  }
}


$(document).ready(function() {
  if(cell_left_number > 0) {
    $('.custom-icon').css('display', 'none');
    $('.cel-plus').css('display', 'none');
  }

  $('input[name="regime"]').click(function() {
    $('#cel-regime').val('');
    var value = $(this).val();
    if (value == 'RDE' || value == '40' || value == 'Substituto' ) {
      var this_duration = 24*60/timeslot_minutes;
      $('#cel-regime').text(this_duration);
      cell_left_number = this_duration
      cell_type_choosed = 40;
      cell_situation = "not_checked"
      $('.checkbox input[type="checkbox"]').prop('checked', false);
      $('label.checkbox').removeClass('active');
      timeslots = []
    } else if (value == '20' || value == 'Temporário'){
      var this_duration = 12*60/timeslot_minutes;
      $('#cel-regime').text(this_duration);
      cell_left_number = this_duration
      cell_type_choosed = 20;
      cell_situation = "not_checked"
      $('.checkbox input[type="checkbox"]').prop('checked', false);
      $('label.checkbox').removeClass('active');
      timeslots = []
    }

    if ($('#error-alert-form').is(':visible')) {
      $('#error-alert-form').hide();
      $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').add('label[for^="sat-"]').removeClass('disabled').removeAttr('aria-disabled');
      $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').add('input[type="checkbox"][id^="sat-"]').prop('disabled', false);
    }

    $('tbody.block').find('*').css({
      "background-color": "",
      "color": "",
      "font-weight": ""
    });

    $('thead.block').find('*').css({
      "background-color": "",
      "color": "",
      "font-weight": ""
    });

    $('.custom-icon').css('display', 'none');
    $('.cel-plus').css('display', 'none');
    $('.cel').css('display', '');
  });

  // Limpar formulário inteiro
  $('#clean-fpa').click(function() {
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
    cell_left_number = 0;
  });

  // Pegar dados dos checkboxes
  $('.checkbox').click(function() {

    var input_id = $(this).attr('for');
    var [input_day_of_week, input_period, input_timeslot] = input_id.split('-');

    if(cell_left_number == 0 && cell_type_choosed == 0) {
      block_options();
    } else {
      var input_val = $('#' + input_id).val();
      var button_is_checked = $('#' + input_id).prop('checked');

      if(button_is_checked) {
        
        cell_left_number += 1;
        var [input_object, input_day] = input_val.split(',');
        var [timeslot_begin_hour, timeslot_end_hour] = input_object.split('-');

        if (cell_situation == "checked") {
          //pode causar conflito com regra de 8 horas e 11 
          $('input[type="checkbox"][id^="mon-"], input[type="checkbox"][id^="tue-"], input[type="checkbox"][id^="wed-"], input[type="checkbox"][id^="thu-"], input[type="checkbox"][id^="fri-"], input[type="checkbox"][id^="sat-"]').each(function() {
            if (!$(this).prop('checked')) {
              $(this).prop('disabled', false);
              $('label[for="' + $(this).attr('id') + '"]').removeClass('disabled').removeAttr('aria-disabled');
            }
          });
          cell_situation = "not_checked"
          cell_left_number += 1

          $('#error-alert-form').hide();
        }

        var index = timeslots.findIndex(function(lesson) {
          return lesson.id === input_id;
        });

        if (index !== -1) {
          timeslots.splice(index, 1);
        }

        var [id_day, id_period, id_timeslot] = input_id.split('-');

        $('#period-' + id_period).css({
          "background-color": "",
          "color": "",
          "font-weight": ""
        });
        $('#timeslot-' + id_period + '-' + id_timeslot).css({
          "background-color": "",
          "color": "",
          "font-weight": ""
        });
        $('#day_of_week-' + id_day).css({
          "background-color": "",
          "color": "",
          "font-weight": ""
        });

        if(cell_left_number < 0) {
          var positive_value = Math.abs(cell_left_number)
          $('#cel-regime').text('+'+positive_value);
          $('.custom-icon').css('display', '');
          $('.cel-plus').css('display', '');
          $('.cel').css('display', 'none');
        } else {
          $('#cel-regime').text(cell_left_number);
          $('.custom-icon').css('display', 'none');
          $('.cel-plus').css('display', 'none');
          $('.cel').css('display', '');
        }
      } else {
        if(cell_situation != "checked") {
          update_cell_left_number(button_is_checked);
          if (cell_situation != "checked") {
            var [input_object, input_day] = input_val.split(',');
            var [timeslot_begin_hour, timeslot_end_hour] = input_object.split('-');
            var lesson = {
              id: input_id,
              timeslot_begin_hour: timeslot_begin_hour,
              timeslot_end_hour: timeslot_end_hour,
              day_of_week: input_day,
            };

            timeslots.push(lesson) // mon-mor-1
          }
        }
      }
    }
  });

  // Enviar formulário inteiro
  $('#send-disponibility').click(function() {
    var user_regime =  $('input[name="regime"]:checked').val();
    var json_data = JSON.stringify(timeslots);

     eight_hours_passed = eight_work_hours_rule();
     eleven_hours_passed = eleven_hours_rule();

    let csrftoken = get_cookie('csrftoken');

    if (user_regime && timeslots.length !== 0) {
      if(cell_left_number <= 0) {
        if(!eleven_hours_passed) {
          if (!eight_hours_passed) {
            $.ajax({
              type: 'post',
              url: '/' + current_language + '/professor/preferencia-atribuicao/',
              data: {
                user_regime: user_regime,
                user_timeslots: json_data
              },
              headers: {
                'X-CSRFToken': csrftoken
              },
              success: function (response) {
                $('input[name="regime"]:checked').prop('checked', false);
                $('#error-alert-form').hide();
                window.location.href = '/' + current_language + '/professor/preferencia-atribuicao'
              },
              error: function (xhr, status, error) {
                $('#error-message-form').text('Ocorreu um erro no envio de FPA.');
                $('#error-alert-form').show();
                window.scrollTo({
                  top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
                  behavior: 'smooth'
                });
              }
            });
          } else {
            if(lang == 'pt-br' || lang == '') {
              $('#error-message-form').text('A seleção da disponibilidade de horário não pode ultrapassar 8 horas de trabalho diárias.');
            } else {
              $('#error-message-form').text('The selection of time availability cannot exceed 8 hours of work per day.');
            }
            
            $('#error-alert-form').show();
            window.scrollTo({
              top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
              behavior: 'smooth'
            });
          }
        } else {
          if(lang == 'pt-br' || lang == '') {
            $('#error-message-form').text('A seleção da disponibilidade deve permitir no mínimo 11 horas de intervalo entre a hora inicial do trabalho de um dia e a hora final de trabalho do dia seguinte.');
          } else {
            $('#error-message-form').text("The availability selection must allow for a minimum of 11 hours between the start time of one day's work and the end time of the next day's work.");
          }
            $('#error-alert-form').show();
            window.scrollTo({
              top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
              behavior: 'smooth'
            });
          }
      } else {
        if(lang == 'pt-br' || lang == '') {
          $('#error-message-form').text('Por favor insira todas as células.');
        } else {
          $('#error-message-form').text('Please enter all cells.');
        }
        $('#error-alert-form').show();
        window.scrollTo({
          top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
          behavior: 'smooth'
        });
      }
    } else {
      if(lang == 'pt-br' || lang == '') {
        $('#error-message-form').text('Insira as informações pedidas em cada seção.');
      } else {
        $('#error-message-form').text('Enter the information requested in each section.');
      }
      $('#error-alert-form').show();
      window.scrollTo({
        top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
        behavior: 'smooth'
      });
    }
  });

  function get_cookie(name) {
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

function eight_work_hours_rule() {
  checkboxes = $('input[type="checkbox"]:checked');

  if (checkboxes.filter('[id^="mon"]').length > max_quantity_cells ||
      checkboxes.filter('[id^="tue"]').length > max_quantity_cells ||
      checkboxes.filter('[id^="wed"]').length > max_quantity_cells ||
      checkboxes.filter('[id^="thu"]').length > max_quantity_cells ||
      checkboxes.filter('[id^="fri"]').length > max_quantity_cells ||
      checkboxes.filter('[id^="sat"]').length > max_quantity_cells) {
    return true;
  } else {
    return false;
  }
}

function check_checkboxes(checkboxes) {
  var control = 0;
  for (var i = 0; i < checkboxes.length; ++i) {
    var checkbox_disable = document.getElementById(checkboxes[i]);
    if (checkbox_disable && checkbox_disable.checked == true) {
      control++;
    }
  }

  if (control > 0) {
    return true;
  } else {
    return false;
  }
}

function eleven_hours_rule() {

   var tue_mor = [];
   var wed_mor = [];
   var thu_mor = [];
   var fri_mor = [];
   var sat_mor = [];

   var mon_noc = [];
   var tue_noc = [];
   var wed_noc = [];
   var thu_noc = [];
   var fri_noc = [];

   for (var i = 1; i <= 4; ++i) {
     tue_mor.push(document.getElementById("tue-mor-" + i));
     wed_mor.push(document.getElementById("wed-mor-" + i));
     thu_mor.push(document.getElementById("thu-mor-" + i));
     fri_mor.push(document.getElementById("fri-mor-" + i));
     sat_mor.push(document.getElementById("sat-mor-" + i));
   }

   for (var i = 0; i < 4; ++i) {
     mon_noc.push(document.getElementById("mon-noc-" + (3+i)));
     tue_noc.push(document.getElementById("tue-noc-" + (3+i)));
     wed_noc.push(document.getElementById("wed-noc-" + (3+i)));
     thu_noc.push(document.getElementById("thu-noc-" + (3+i)));
     fri_noc.push(document.getElementById("fri-noc-" + (3+i)));
   }

   if (mon_noc[0].id == "mon-noc-3") {
     if (mon_noc[0] && mon_noc[0].checked == true && tue_mor[0] && tue_mor[0].checked == true)
       return true;
   }
   if (mon_noc[1].id == "mon-noc-4") {
     var tue_mor1= [];
     tue_mor1.push(tue_mor[0].id, tue_mor[1].id);
     if (mon_noc[1] && mon_noc[1].checked == true && check_checkboxes(tue_mor1))
       return true;
   }
   if (mon_noc[2].id == "mon-noc-5") {
     var tue_mor1= [];
     tue_mor1.push(tue_mor[0].id, tue_mor[1].id, tue_mor[2].id);
     if (mon_noc[2] && mon_noc[2].checked == true && check_checkboxes(tue_mor1))
       return true;
   }
   if (mon_noc[3].id == "mon-noc-6") {
     var tue_mor1= [];
     tue_mor1.push(tue_mor[0].id, tue_mor[1].id, tue_mor[2].id, tue_mor[3].id);
     if (mon_noc[3] && mon_noc[3].checked == true && check_checkboxes(tue_mor1))
       return true;
   }
   //
   if (tue_noc[0].id == "tue-noc-3") {
     if (tue_noc[0] && tue_noc[0].checked == true && wed_mor[0] && wed_mor[0].checked == true)
       return true;
   }
   if (tue_noc[1].id == "tue-noc-4") {
     var wed_mor1= [];
     wed_mor1.push(wed_mor[0].id, wed_mor[1].id);
     if (tue_noc[1] && tue_noc[1].checked == true && check_checkboxes(wed_mor1))
       return true;
   }
   if (tue_noc[2].id == "tue-noc-5") {
     var wed_mor1= [];
     wed_mor1.push(wed_mor[0].id, wed_mor[1].id, wed_mor[2].id);
     if (tue_noc[2] && tue_noc[2].checked == true && check_checkboxes(wed_mor1))
       return true;
   }
   if (tue_noc[3].id == "tue-noc-6") {
     var wed_mor1= [];
     wed_mor1.push(wed_mor[0].id, wed_mor[1].id, wed_mor[2].id, wed_mor[3].id);
     if (tue_noc[3] && tue_noc[3].checked == true && check_checkboxes(wed_mor1))
       return true;
   }
   //
   if (wed_noc[0].id == "wed-noc-3") {
     if (wed_noc[0] && wed_noc[0].checked == true && thu_mor[0] && thu_mor[0].checked == true)
       return true;
   }
   if (wed_noc[1].id == "wed-noc-4") {
     var thu_mor1= [];
     thu_mor1.push(thu_mor[0].id, thu_mor[1].id);
     if (wed_noc[1] && wed_noc[1].checked == true && check_checkboxes(thu_mor1))
       return true;
   }
   if (wed_noc[2].id == "wed-noc-5") {
     var thu_mor1= [];
     thu_mor1.push(thu_mor[0].id, thu_mor[1].id, thu_mor[2].id);
     if (wed_noc[2] && wed_noc[2].checked == true && check_checkboxes(thu_mor1))
       return true;
   }
   if (wed_noc[3].id == "wed-noc-6") {
     var thu_mor1= [];
     thu_mor1.push(thu_mor[0].id, thu_mor[1].id, thu_mor[2].id, thu_mor[3].id);
     if (wed_noc[3] && wed_noc[3].checked == true && check_checkboxes(thu_mor1))
       return true;
   }
   //
   if (thu_noc[0].id == "thu-noc-3") {
     if (thu_noc[0] && thu_noc[0].checked == true && fri_mor[0] && fri_mor[0].checked == true)
       return true;
   }
   if (thu_noc[1].id == "thu-noc-4") {
     var fri_mor1= [];
     fri_mor1.push(fri_mor[0].id, fri_mor[1].id);
     if (thu_noc[1] && thu_noc[1].checked == true && check_checkboxes(fri_mor1))
       return true;
   }
   if (thu_noc[2].id == "thu-noc-5") {
     var fri_mor1= [];
     fri_mor1.push(fri_mor[0].id, fri_mor[1].id, fri_mor[2].id);
     if (thu_noc[2] && thu_noc[2].checked == true && check_checkboxes(fri_mor1))
       return true;
   }
   if (thu_noc[3].id == "thu-noc-6") {
     var fri_mor1= [];
     fri_mor1.push(fri_mor[0].id, fri_mor[1].id, fri_mor[2].id, fri_mor[3].id);
     if (thu_noc[3] && thu_noc[3].checked == true && check_checkboxes(fri_mor1))
       return true;
   }
   //
   if (fri_noc[0].id == "fri-noc-3") {
     if (fri_noc[0] && fri_noc[0].checked == true && sat_mor[0] && sat_mor[0].checked == true)
       return true;
   }
   if (fri_noc[1].id == "fri-noc-4") {
     var sat_mor1= [];
     sat_mor1.push(sat_mor[0].id, sat_mor[1].id);
     if (fri_noc[1] && fri_noc[1].checked == true && check_checkboxes(sat_mor1))
       return true;
   }
   if (fri_noc[2].id == "fri-noc-5") {
     var sat_mor1= [];
     sat_mor1.push(sat_mor[0].id, sat_mor[1].id, sat_mor[2].id);
     if (fri_noc[2] && fri_noc[2].checked == true && check_checkboxes(sat_mor1))
       return true;
   }
   if (fri_noc[3].id == "fri-noc-6") {
     var sat_mor1= [];
     sat_mor1.push(sat_mor[0].id, sat_mor[1].id, sat_mor[2].id, sat_mor[3].id);
     if (fri_noc[3] && fri_noc[3].checked == true && check_checkboxes(sat_mor1))
       return true;
   }
}

function period_input(value) {
  var element = document.getElementById("period-" + value);
  var backgroundColor = getComputedStyle(element).backgroundColor;
  var isTrue = backgroundColor == "rgb(80, 124, 117)";
  if(isTrue) {
    take_off_ckecked(value);

    $('#period-' + value).css({
      "background-color": "",
      "color": "",
      "font-weight": ''
    })

    for (var i = 1; i <= 6; i++) {
      $('#timeslot-' + value + '-' + i).css({
          "background-color": "",
          "color": "",
          "font-weight": ""
      });
  }
  } else {
    if(cell_left_number == 0 && cell_type_choosed == 0) {
      block_options();
      if(lang == 'pt-br' || lang == '') {
        $('#error-message-form').text('Insira o regime de trabalho para poder acrescestar sua disponibilidade.');
      } else {
        $('#error-message-form').text('Enter the work regime so you can add your availability.');
      }
      
    } else {
      $('#period-' + value).css({
        "background-color": "#507c75",
        "color": "white",
        "font-weight": 700
      })

      take_off_ckecked(value);
      put_in_checked(value);
    }
  }
  
}

function timeslot_input(value) {
  var element = document.getElementById("timeslot-" + value);
  var backgroundColor = getComputedStyle(element).backgroundColor;
  var isTrue = backgroundColor == "rgb(80, 124, 117)";
  if(isTrue) {
    take_off_ckecked(value);

    $('#timeslot-' + value).css({
      "background-color": "",
      "color": "",
      "font-weight": ''
    })

    $('#period-' + value.substring(0, 3)).css({
      "background-color": "",
      "color": "",
      "font-weight": ''
    })
  } else {
    if(cell_left_number == 0 && cell_type_choosed == 0) {
      block_options();
      if(lang == 'pt-br' || lang == '') {
        $('#error-message-form').text('Insira o regime de trabalho para poder acrescestar sua disponibilidade.');
      } else {
        $('#error-message-form').text('Enter the work regime so you can add your availability.');
      }
    } else {
      $('#timeslot-' + value).css({
        "background-color": "#507c75",
        "color": "white",
        "font-weight": 700
      })

      take_off_ckecked(value);
      put_in_checked(value);
    }
  }
}

function day_of_week_input(value) {
  var element = document.getElementById("day_of_week-" + value);
  var backgroundColor = getComputedStyle(element).backgroundColor;
  var isTrue = backgroundColor == "rgb(80, 124, 117)";
  if(isTrue) {
    take_off_ckecked(value);

    $('#day_of_week-' + value).css({
      "background-color": "",
      "color": "",
      "font-weight": ''
    });

    $('.period').css({
      "background-color": "",
      "color": "",
      "font-weight": ""
    });
  } else {
    if(cell_left_number == 0 && cell_type_choosed == 0) {
      block_options();
      if(lang == 'pt-br' || lang == '') {
        $('#error-message-form').text('Insira o regime de trabalho para poder acrescestar sua disponibilidade.');
      } else {
        $('#error-message-form').text('Enter the work regime so you can add your availability.');
      }
    } else {
      $('#day_of_week-' + value).css({
        "background-color": "#507c75",
        "color": "white",
        "font-weight": 700
      })

      take_off_ckecked(value);
      put_in_checked(value);
    }
  }
  
}

function block_options() {
  $('#cel-regime').text("--");
  $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').add('label[for^="sat-"]').addClass('disabled').attr('aria-disabled', 'true');
  $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').add('input[type="checkbox"][id^="sat-"]').prop('disabled', true);

  $('#error-message-form').text('Insira o regime de trabalho antes de continuar.');
  $('#error-alert-form').show();
  window.scrollTo({
    top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
    behavior: 'smooth'
  });
}

function take_off_ckecked(value) {
  var checkboxes_checked = Array.from(document.querySelectorAll('input[type="checkbox"]:checked[id*="'+value+'"]')).map(function(checkbox) {
    return checkbox.id;
  });

  for(var i = 0; i < checkboxes_checked.length; i++) {
    var checked_id = checkboxes_checked[i]
    var index = timeslots.findIndex(function(lesson) {
      return lesson.id === checked_id;
    });
    
    if (index !== -1) {
      timeslots.splice(index, 1);
    }

    var checkbox = document.getElementById(checked_id);
    if (checkbox) {
      checkbox.checked = false;
      var button = checkbox.parentElement;
      var label = button.parentElement;
      button.classList.remove("active");
      label.classList.remove("active");
    }

    cell_left_number += 1

    if(cell_left_number < 0) {
      var positive_value = Math.abs(cell_left_number)
      $('#cel-regime').text('+'+positive_value);
      $('.custom-icon').css('display', '');
      $('.cel-plus').css('display', '');
      $('.cel').css('display', 'none');
    } else {
      $('#cel-regime').text(cell_left_number);
      $('.custom-icon').css('display', 'none');
      $('.cel-plus').css('display', 'none');
      $('.cel').css('display', '');
    }
  }
}

function put_in_checked(value) {
  var checkboxes_not_checked = Array.from(document.querySelectorAll('input[type="checkbox"]:not(:checked)[id*="'+value+'"]')).map(function(checkbox) {
    return checkbox.id;
  });

  for(var i = 0; i < checkboxes_not_checked.length; i++) {
    var checked_id = checkboxes_not_checked[i];
    var checked_value = $('#' + checked_id).val();

    update_cell_left_number(false);
    var [checked_object, checked_day] = checked_value.split(',');
    var [timeslot_begin_hour, timeslot_end_hour] = checked_object.split('-');
    var lesson = {
      id: checked_id,
      timeslot_begin_hour: timeslot_begin_hour,
      timeslot_end_hour: timeslot_end_hour,
      day_of_week: checked_day,
    };

    checkboxes.push(lesson.id)

    timeslots.push(lesson)

    var checkbox = document.getElementById(checked_id);
    if (checkbox) {
      checkbox.checked = true;
      var button = checkbox.parentElement;
      var label = button.parentElement;
      button.classList.add("active");
      label.classList.add("active");
    }
  }
}

function update_cell_left_number(button_is_checked) {
  if(!button_is_checked) {
    if (cell_situation == "checked") {
      cell_left_number = 0;
      $('#cel-regime').text(cell_left_number);
    } else {
      cell_left_number -= 1;
      if(cell_left_number < 0) {
        var positive_value = Math.abs(cell_left_number)
        $('#cel-regime').text('+'+positive_value);
        $('.custom-icon').css('display', '');
        $('.cel-plus').css('display', '');
        $('.cel').css('display', 'none');
      } else {
        $('#cel-regime').text(cell_left_number);
        $('.custom-icon').css('display', 'none');
        $('.cel-plus').css('display', 'none');
        $('.cel').css('display', '');
      }
    }
  }
}
