var timetables_complete = document.currentScript.getAttribute("timetables-professor");
var timetables_complete  = JSON.parse(timetables_complete);

$.each(timetables_complete, function(index, value) {

  $("#cel-"+value.cord).text(value.acronym);

  $("#cel-"+value.cord).closest('.content_collapsible').prev('.collapsible').addClass("default-open");
  $("#cel-"+value.cord).closest('.content_collapsible').prev('.collapsible').addClass("active_collapse");
});

$(document).ready(function() {
  // console.log(tametables_user)
  

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