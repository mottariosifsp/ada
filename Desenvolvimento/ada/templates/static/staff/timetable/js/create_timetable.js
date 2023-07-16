window.addEventListener('pageshow', function(event) {
  hide_loading()
});

$(document).ready(function() {
  
  $('.header-table').closest('table').find('.header-days').hide();
  $('.header-table').closest('table').find('tbody').hide();

  $('.header-table').click(function() {
    $(this).find('.icon-minimize').text('-');
    $(this).closest('table').find('.header-days').toggle();
    $(this).closest('table').find('tbody').toggle();
    if ( $(this).closest('table').find('.header-days').is(":visible")) {
      $('html, body').animate({
        scrollTop: $(this).closest('table').offset().top - 100
      }, 600);
      
    }else{
      $(this).find('.icon-minimize').text('+');
    }
  });

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
      $('.form-control').on('blur', function() {
        $(this).css('border-color', '#ced4da');
      });
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

  if($('#selected_class').text() == "") {
    // $('#course_select').hide();
    $('#course_select').css('opacity', '0.5');
    $('#course_select').css('pointer-events', 'none');
    $('#course_select').css('filter', 'grayscale(100%)');
  }

  $("#submit_timetable").click(function() {
    show_loading()

    let selected_courses = [];
    
    for (let index = 0; index < 6; index++) {
      selected_courses[index] = $('.datalist'+index).map(function() {
        if($(this).attr('course-id') == undefined){
          return '';
        }else{
          return $(this).attr('course-id');
        }
      }).get();
    }

    console.log("for acabado");
    alert($("#selected_class").text());
    
    let csrftoken = getCookie('csrftoken');
      $.ajax({
        method: 'POST',
        url: window.location.href, 
        data: {
          'selected_courses': JSON.stringify( selected_courses),
          'selected_class': $('#selected_class').text()
      },
        headers: {
          'X-CSRFToken': csrftoken
        },
        success: function(response) {

          if (response.erro) {
            $('#mensagem-erro').show();
            $('#mensagem-erro').text(response.mensagem).show();
            $('html, body').animate({
              scrollTop: $('#mensagem-erro').offset().top - 100
            }, 600);      
            hide_loading()
          } else {
            console.log(response);
            show_loading()
            window.location.href = "/staff/grade/ver/?class="+$('#selected_class').text();            
          }
        },
        error: function(xhr, status, error) {
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

function show_loading(){
  $('body').css('opacity', '0.5');
  $('.spinner-border').show();
}

function hide_loading(){
  $('body').css('opacity', '1');
  $('.spinner-border').hide();
}
