var timetables_complete = document.currentScript.getAttribute("timetables-complete");
var timetables_complete  = JSON.parse(timetables_complete);

$.each(timetables_complete, function(index, value) {

    $("#cel-"+value.cord).text(value.acronym);

    $("#cel-"+value.cord).closest('.content_collapsible').prev('.collapsible').addClass("default-open");

});

$(document).ready(function() {
  // console.log(tametables_user)

  // $('.header-table').click(function() {
  //   $(this).find('.icon-minimize').text('-');
  //   $(this).closest('table').find('.header-days').toggle();
  //   $(this).closest('table').find('tbody').toggle();
  //   if ( $(this).closest('table').find('.header-days').is(":visible")) {
  //     $('html, body').animate({
  //       scrollTop: $(this).closest('table').offset().top - 100
  //     }, 600);
      
  //   }else{
  //     $(this).find('.icon-minimize').text('+');
  //   }
  // });
});

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {

  var content = coll[i].nextElementSibling;

  if (coll[i].classList.contains("default-open")) {
    content.style.maxHeight = content.scrollHeight + "px";
  }

  coll[i].addEventListener("click", function() {
    this.classList.toggle("active_collapse");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
      content.scrollIntoView({ behavior: 'smooth' });
    } 
  });
}