var timetables_user = document.currentScript.getAttribute("timetables-user");
var timetables_user = JSON.parse(timetables_user);

$.each(timetables_user, function(index, value) {

  let professor = value.professor;
  
  $("#cel-"+value.cord).html("<strong>" + value.acronym + "</strong>" + "<br>" + professor);
  console.log(value.cord);
  console.log(value.course);
});

$(document).ready(function() {
  console.log(tametables_user)

});