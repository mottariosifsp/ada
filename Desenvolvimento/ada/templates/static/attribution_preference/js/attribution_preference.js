var lang = document.currentScript.getAttribute("data-lang");
var work_regime = document.currentScript.getAttribute("work_regime");
var work_disponibility = document.currentScript.getAttribute("work_disponibility");
var work_courses = document.currentScript.getAttribute("work_courses");

var work_disponibility_array = JSON.parse(work_disponibility.replace(/'/g, '"'));
var work_courses_array = JSON.parse(work_courses.replace(/'/g, '"'));

$('.'+ work_regime).css({
    "background-color": "#507c75",
    "color": "white",
    "font-weight": 700
})

for(var i = 0; i < work_disponibility_array.length; i++) {
    var elemento = work_disponibility_array[i];
    var phrase = elemento.frase;

    $('#btn-'+ phrase).css({
        "background-color": "#507c75",
    });
    $("#" + phrase + " i").addClass("fas fa-check-circle check");
    $('#'+ phrase).css({
        "color": "white",
    });
}

for (var i = 0; i < work_courses_array.length; i++) {
    var course = work_courses_array[i];
    var sigla = course.sigla;
    var nome = course.name_course;
    var curso = course.course_area;
    var turno = course.period;
    var aulas = course.classes;
  
    var newRow = '<tr>' +
      '<td class="text-center">' + sigla + '</td>' +
      '<td class="text-center">' + nome + '</td>' +
      '<td class="text-center">' + curso + '</td>' +
      '<td class="text-center">' + turno + '</td>' +
      '<td class="text-center">' + aulas + '</td>' +
      '</tr>';
  
    $('#courses-list').append(newRow);
  }

