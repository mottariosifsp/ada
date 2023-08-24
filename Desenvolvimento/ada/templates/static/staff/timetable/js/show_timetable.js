var timetables_complete = document.currentScript.getAttribute("timetables-complete");
var timetables_complete  = JSON.parse(timetables_complete);

$.each(timetables_complete, function(index, value) {

  $("#cel-"+value.cord).text(value.acronym);

  $("#cel-"+value.cord).closest('.content_collapsible').prev('.collapsible').addClass("default-open");

});

$(document).ready(function() {
 
});

