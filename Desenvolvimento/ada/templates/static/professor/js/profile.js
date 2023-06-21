var timetables_user = document.currentScript.getAttribute("timetables-professor");
var timetables_user = JSON.parse(timetables_user);

$.each(timetables_user, function(index, value) {
    $("#cel-"+value.cord).text(value.course);
    console.log(value.cord);
    console.log(value.course);
});


$("document").ready(function() {


});
