var lang = document.currentScript.getAttribute('data-lang');
var disponibility = document.currentScript.getAttribute('disponibility');
var timetables = document.currentScript.getAttribute('timetables');
var courses = document.currentScript.getAttribute('courses');
var blocks = document.currentScript.getAttribute('blocks');
var areas = document.currentScript.getAttribute('areas');
var disponibility_hour = document.currentScript.getAttribute('disponibility_hour');

var timetable_global = []

var disponibility_array = JSON.parse(disponibility.replace(/'/g, '"'));
var courses_array = parseDisponibilityHour(JSON.parse(courses.replace(/'/g, '"')));
var timetables_array = JSON.parse(timetables.replace(/'/g, '"'));
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
    var hour = elemento.hour;
    var minute = elemento.minute;
    var formattedHour = formatHour(hour, minute);


    var novo_objeto = {
        frase: frase,
        posicao: posicao,
        sessao: sessao,
        dia: dia,
        hora: formattedHour
    };

    disponibility_array_obj.push(novo_objeto);
}
// var disponibility_array_hour = parseDisponibilityHour(disponibility_hour);
// var disponibility_array_hour_obj = [];

// // For para transformar em array de objeto com hora formatada
// for (var i = 0; i < disponibility_array_hour.length; i++) {
//   var elemento = disponibility_array_hour[i];
//   var hour = elemento.hour;
//   var minute = elemento.minute;
//   var formattedHour = formatHour(hour, minute);

//   var novo_objeto = {
//     hour: formattedHour,
//     frase: disponibility_array_obj[i].frase
//   };

//   disponibility_array_hour_obj.push(novo_objeto);
// }

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

var timetables_array_obj = [];

for (var i = 0; i < timetables_array.length; i++) {
    var elemento = timetables_array[i];
    var day = elemento.day;
    var hour_start = elemento.hour_start;
    var course = elemento.course_acronym;
    var classs = elemento.classs;

    var formattedHour = hour_start.substr(0, 5);
    var hour_start_real = formattedHour + ':00';

    var novo_objeto = {
        day: day,
        hour_start: hour_start_real,
        course_acronym: course,
        classs: classs
    };

    timetables_array_obj.push(novo_objeto);
}

var blocks_array_obj = [];

for (var i = 0; i < blocks_array.length; i++) {
  var elemento = blocks_array[i];
  var id = elemento.registration_block_id;
  var name_block = elemento.name_block;
  var acronym = elemento.acronym;

  var novo_objeto = {
    id: id,
    name_block: name_block,
    acronym: acronym
  };

  blocks_array_obj.push(novo_objeto);
}

var areas_array_obj = [];

for (var i = 0; i < areas_array.length; i++) {
  var elemento = areas_array[i];
  var id = elemento.registration_area_id;
  var name_area = elemento.name_area;
  var acronym = elemento.acronym;
  var blocks = elemento.blocks;

  var novo_objeto = {
    id: id,
    name_area: name_area,
    acronym: acronym,
    blocks: acronym
  };

  areas_array_obj.push(novo_objeto);
}

var courses_array_obj = [];

for (var i = 0; i < courses_array.length; i++) {
  var elemento = courses_array[i];
  var id = elemento.registration_course_id;
  var name = elemento.name;
  var acronym = elemento.acronym;
  var area = elemento.area;
  var block = elemento.block;

  var novo_objeto = {
    id: id,
    name: name,
    acronym: acronym,
    area: area,
    block: block
  };

  courses_array_obj.push(novo_objeto);
}


timetables = [] // lista de timetables do modal

$("div[data-toggle='buttons']").on("click", function() {
    var dataId = $(this).closest("div[data-id]").data("id"); 
    $("#cel-position").text(dataId).css("visibility", "hidden");
    
    area_options()
    block_options()
    timetables_options()
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

function timetables_options() {
    var spanValue = $('#cel-position').text();

    var filteredHour = disponibility_array_hour_obj.find(function(element) {
        return element.frase === spanValue;
    });
    
    var filteredTimetables = timetables_array_obj.filter(function(course) {
        return course.hour_start === filteredHour.hour;
    });

    timetables = filteredTimetables;

    // Criar a lista de options para datalist com base nos cursos filtrados
    var timetableOptionsDatalist = document.getElementById('course-options');
    timetableOptionsDatalist.innerHTML = '';

    for (var i = 0; i < filteredTimetables.length; i++) {
        var timetable = filteredTimetables[i];

        var option = document.createElement('option');
        option.value = timetable.course_acronym;
        option.textContent = "Turma: " + timetable.classs;
        timetableOptionsDatalist.appendChild(option);
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


