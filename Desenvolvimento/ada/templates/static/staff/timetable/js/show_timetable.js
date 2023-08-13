var timetables_complete = document.currentScript.getAttribute("timetables-complete");
var timetables_complete  = JSON.parse(timetables_complete);

$('.header-table').closest('table').find('.header-days').hide();
$('.header-table').closest('table').find('tbody').hide();

$.each(timetables_complete, function(index, value) {

    $("#cel-"+value.cord).text(value.acronym);

    $("#cel-"+value.cord).closest('table').find('.header-days').show();
    $("#cel-"+value.cord).closest('table').find('tbody').show();

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