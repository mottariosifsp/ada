var lang = document.currentScript.getAttribute('data-lang');
var disponibility = document.currentScript.getAttribute('disponibility');
var courses = document.currentScript.getAttribute('courses');
var blocks = document.currentScript.getAttribute('blocks');
var areas = document.currentScript.getAttribute('areas');
var disponibility_hour = document.currentScript.getAttribute('disponibility_hour');

var timetable_global = []

var disponibility_array = JSON.parse(disponibility.replace(/'/g, '"'));
var courses_array = JSON.parse(courses.replace(/'/g, '"'));
var blocks_array = JSON.parse(blocks.replace(/'/g, '"'));
var areas_array = JSON.parse(areas.replace(/'/g, '"'));

var disponibility_array_obj = [];

// For para transformar em array de objeto
for (var i = 0; i < disponibility_array.length; i++) {
    var elemento = disponibility_array[i];
    var frase = elemento.frase;
    var posicao = elemento.posicao;
    var sessao = elemento.sessao;
    var dia = elemento.dia;

    var novo_objeto = {
        frase: frase,
        posicao: posicao,
        sessao: sessao,
        dia: dia
    };

    disponibility_array_obj.push(novo_objeto);
}
var disponibility_array_hour = parseDisponibilityHour(disponibility_hour);
var disponibility_array_hour_obj = [];

// For para transformar em array de objeto com hora formatada
for (var i = 0; i < disponibility_array_hour.length; i++) {
  var elemento = disponibility_array_hour[i];
  var hour = elemento.hour;
  var minute = elemento.minute;
  var formattedHour = formatHour(hour, minute);

  var novo_objeto = {
    hour: formattedHour,
    frase: disponibility_array_obj[i].frase
  };

  disponibility_array_hour_obj.push(novo_objeto);
}

function parseDisponibilityHour(hourString) {
  var regex = /datetime\.time\((\d+), (\d+)\)/g;
  var matches = hourString.matchAll(regex);
  var hourArray = [];

  for (var match of matches) {
    var hours = parseInt(match[1]);
    var minutes = parseInt(match[2]);
    var hourObject = {
      hour: hours,
      minute: minutes
    };
    hourArray.push(hourObject);
  }

  return hourArray;
}

function formatHour(hour, minute) {
  var formattedHour = hour.toString().padStart(2, '0') + ':' +
    minute.toString().padStart(2, '0') + ':00';
  return formattedHour;
}

var courses_array_obj = [];

for (var i = 0; i < courses_array.length; i++) {
    var elemento = courses_array[i];
    var day = elemento.day;
    var hour_start = elemento.hour_start;
    var course = elemento.course;
    var classs = elemento.classs;

    var formattedHour = hour_start.substr(0, 5);
    var hour_start_real = formattedHour + ':00';

    var novo_objeto = {
        day: day,
        hour_start: hour_start_real,
        name_course: course,
        classs: classs
    };

    courses_array_obj.push(novo_objeto);
}

var blocks_array_obj = [];

for (var i = 0; i < blocks_array.length; i++) {
  var elemento = blocks_array[i];
  var name_block = elemento.name_block;
  var acronym = elemento.acronym;

  var novo_objeto = {
    name_block: name_block,
    acronym: acronym
  };

  blocks_array_obj.push(novo_objeto);
}

var areas_array_obj = [];

for (var i = 0; i < areas_array.length; i++) {
  var elemento = areas_array[i];
  var name_area = elemento.name_area;
  var acronym = elemento.acronym;
  var blocks = elemento.blocks;

  var novo_objeto = {
    name_area: name_area,
    acronym: acronym,
    blocks: acronym
  };

  areas_array_obj.push(novo_objeto);
}

courses = [] // lista de courses do modal

$("div[data-toggle='buttons']").on("click", function() {
    var dataId = $(this).closest("div[data-id]").data("id"); 
    $("#cel-position").text(dataId).css("visibility", "hidden");
    
    area_options()
    block_options()
    courses_options()
    $("#addCourseModal").modal("show");
});

function area_options() {
    var areaOptionsDatalist = document.getElementById('area-options');
    areaOptionsDatalist.innerHTML  = ''

    for (var i = 0; i < areas_array_obj.length; i++) {
        var area = areas_array_obj[i];
    
        var option = document.createElement('option');
        option.value = area.acronym;
        option.textContent = area.name_area;
        areaOptionsDatalist.appendChild(option);
    }
}

function block_options() {
    var blockOptionsDatalist = document.getElementById('block-options');
    blockOptionsDatalist.innerHTML = '';

    for (var i = 0; i < blocks_array_obj.length; i++) {
        var block = blocks_array_obj[i];

        var option = document.createElement('option');
        option.value = block.acronym;
        option.textContent = block.name_block;
        blockOptionsDatalist.appendChild(option);
    }
}

function courses_options() {
    var spanValue = $('#cel-position').text();

    var filteredHour = disponibility_array_hour_obj.find(function(element) {
        return element.frase === spanValue;
    });
    
    var filteredCourses = courses_array_obj.filter(function(course) {
        return course.hour_start === filteredHour.hour;
    });

    courses = filteredCourses;

    // Criar a lista de options para datalist com base nos cursos filtrados
    var courseOptionsDatalist = document.getElementById('course-options');
    courseOptionsDatalist.innerHTML = '';

    for (var i = 0; i < filteredCourses.length; i++) {
        var course = filteredCourses[i];

        var option = document.createElement('option');
        option.value = course.name_course;
        option.textContent = "Turma: " + course.classs;
        courseOptionsDatalist.appendChild(option);
    }
}

// function block_filter() {

// }

// function area_filter() {
    
// }

// Mapea na grade
for (var i = 0; i < disponibility_array_obj.length; i++) {
    var obj = disponibility_array_obj[i];
    var fraseId = obj.frase;
    $("label[for='" + fraseId + "']")
    .addClass("btn-checked").removeClass("disabled").removeClass("btn-notchecked");
    $("#" + fraseId)
    .prop("disabled", false);
    $("#sub-" + fraseId).text("+");
    $("#btn-" + fraseId).attr("data-toggle", "modal").attr("data-target", "#addCourseModal");
}

$(document).ready(function() {
    $("#addCourseButton").on("click", function() {
        var selectedCourse = $("#course-filter").val();
        var span = $("#cel-position").text();
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    
        if (selectedCourse !== "") {
          $.ajax({
            url: "/",
            type: "POST",
            data: {
              course: selectedCourse
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                var formattedText = selectedCourse.toUpperCase().substring(0, 3).trim();
                $("#sub-" + span).text(formattedText);
                var course = {
                    selectedCourse: selectedCourse,
                    postion
                }
                timetable_global.push(selectedCourse);
                $("#course-filter").val('');
                $('#error-alert').hide();
            },
            error: function(xhr, textStatus, errorThrown) {
                $('#error-message').text('Erro ao tentar adicionar uma aula.');
                $('#error-alert').show();
            }
          });
        } else {
          $('#error-message').text('Selecione uma aula.');
          $('#error-alert').show();
        }
      });
});


