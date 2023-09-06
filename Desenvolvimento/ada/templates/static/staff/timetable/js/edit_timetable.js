var timetables_complete = document.currentScript.getAttribute("timetables-complete");
var timetables_complete = JSON.parse(timetables_complete);


window.addEventListener('pageshow', function (event) {
  hide_loading()
});

$.each(timetables_complete, function(index, value) {
  console.log(value);
  $("#cel-"+value.cord).val(value.acronym);
  $("#cel-"+value.cord).attr('course-id', value.id);
  console.log()
  console.log("#cel-"+value.cord);
  // add_course_id("#cel-"+value.cord);


  $("#cel-"+value.cord).closest('.content_collapsible').prev('.collapsible').addClass("default-open");
  $("#cel-"+value.cord).closest('.content_collapsible').prev('.collapsible').addClass("active_collapse");
});

$(document).ready(function () {

  $('.course-input').on('input', function() {
    var course = $(this).val();
    var list_name = $(this).attr('list');
    var selectedOption = $('#'+list_name+' option').filter(function() {
      return $(this).val() === course;
    });
    if(selectedOption.attr('course-id') != undefined){
      $(this).attr('course-id', selectedOption.attr('course-id'));
      $('.form-control').on('focus', function() {
        $(this).css('border-color', '#80bdff');
      });
      // $('.form-control').on('blur', function() {
      //   $(this).css('border-color', '#ced4da');
      // });
      $(this).css('border', '1px solid #ced4da');
    }else{
      $(this).attr('course-id', course);
      if(course == ""){
        $(this).css('border', '1px solid #ced4da');
      }else{
        $(this).css('border', '1px solid rgb(255, 0, 0,0.3)');
      }
    }
  });

  if ($('#selected_class').text() == "") {
    $('#course_select').css('opacity', '0.5');
    $('#course_select').css('pointer-events', 'none');
    $('#course_select').css('filter', 'grayscale(100%)');
  }

  // var courses_selected = [];
  // });

  $("#submit_timetable").click(function () {
    show_loading();

    let selected_courses = [];

    for (let index = 0; index < 6; index++) {
      selected_courses[index] = $('.datalist' + index).map(function () {
        if($(this).attr('course-id') == undefined){
          return '';
        }else{
          return $(this).attr('course-id');
        }
      }).get();
    }

    let csrftoken = getCookie('csrftoken');
    $.ajax({
      method: 'POST',
      url: window.location.href,
      data: {
        'selected_courses': JSON.stringify(selected_courses),
        'selected_class': $('#selected_class').text()
      },
      headers: {
        'X-CSRFToken': csrftoken
      },
      success: function (response) {

        if (response.erro) {
          $('#mensagem-erro').show();
          $('#mensagem-erro').text(response.mensagem).show();
          hide_loading();
        } else {
          console.log(response);
          show_loading();
          window.location.href = "/staff/grade/ver/?class=" + $('#selected_class').text();
        }
      },
      error: function (xhr, status, error) {
        console.log(error);
      }
    });
  });

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

function show_loading() {
  $('body').css('opacity', '0.5');
  $('.spinner-border').show();
}

function hide_loading() {
  $('body').css('opacity', '1');
  $('.spinner-border').hide();
}

function add_course_id(element){
  var course = $(element).val();
  var list_name = $(element).attr('list');
  var selectedOption = $('#'+list_name+' option').filter(function() {
    return $(element).val() === course;
  });
  if(selectedOption.attr('course-id') != undefined){
    $(element).attr('course-id', selectedOption.attr('course-id'));
    $('.form-control').on('focus', function() {
      $(element).css('border-color', '#80bdff');
    });
    // $('.form-control').on('blur', function() {
    //   $(this).css('border-color', '#ced4da');
    // });
    $(element).css('border', '1px solid #ced4da');
  }else{
    $(element).attr('course-id', course);
    if(course == ""){
      $(element).css('border', '1px solid #ced4da');
    }else{
      $(element).css('border', '1px solid rgb(255, 0, 0,0.3)');
    }
  }
}