var timetables_user = document.currentScript.getAttribute("timetables-user");
var timetables_user = JSON.parse(timetables_user);

$.each(timetables_user, function(index, value) {

  let professor = value.professor;
  
  $("#cel-"+value.cord).html("<strong>" + value.acronym + "</strong>" + "<br>" + professor);
  console.log(value.cord);
  console.log(value.course);
});

$(document).ready(function() {
  // console.log(tametables_user)
  
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
});