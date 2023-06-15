
var lang = document.currentScript.getAttribute('data-lang');
var disponibility = document.currentScript.getAttribute('disponibility');
var timetables = document.currentScript.getAttribute('timetables');
var courses = document.currentScript.getAttribute('courses');
var blocks = document.currentScript.getAttribute('blocks');
var areas = document.currentScript.getAttribute('areas');

var timetable_global = []

var disponibility_array = JSON.parse(disponibility.replace(/'/g, '"'));
var courses_array = JSON.parse(courses.replace(/'/g, '"'));
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
  var horaString = elemento.hour;

  var novo_objeto = {
    frase: frase, // mon-ves-3
    posicao: posicao,
    sessao: sessao,
    dia: dia,
    hour: horaString // 7:45:00
  };

  disponibility_array_obj.push(novo_objeto);
}

var timetables_array_obj = [];

for (var i = 0; i < timetables_array.length; i++) {
  var timetable_object = timetables_array[i];
  var timetable_id = parseInt(timetable_object.id);
  var day_combo_objects = timetable_object.day_combo;
  var day_combo_data = [];

  for (var j = 0; j < day_combo_objects.length; j++) {
    var day_combo = day_combo_objects[j];
    var day = day_combo.day;
    var timeslots = day_combo.timeslots;
    var timeslot_data = [];

    for (var k = 0; k < timeslots.length; k++) {
      var timeslot = timeslots[k];
      timeslot_data.push({
        'hour_start': timeslot.hour_start,
        'hour_end': timeslot.hour_end,
      });
    }

    day_combo_data.push({
      'day': day,
      'timeslots': timeslot_data,
    });
  }

  var timetable_item = {
    'id': timetable_id,
    'day_combo': day_combo_data,
    'course_acronym': timetable_object.course_acronym,
    'course_name': timetable_object.course_name,
    'classs': timetable_object.classs,
  };

  // alert(timetable_item.day_combo[0].day);
  // alert(timetable_item.day_combo[0].timeslots[0].hour_start);

  timetables_array_obj.push(timetable_item);
}

var blocks_array_obj = [];

for (var i = 0; i < blocks_array.length; i++) {
  var elemento = blocks_array[i];
  var id = elemento.id;
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
  var id = elemento.id;
  var name_area = elemento.name_area;
  var acronym = elemento.acronym;
  var blocks = elemento.blocks;

  var novo_objeto = {
    id: id,
    name_area: name_area,
    acronym: acronym,
    blocks: blocks
  };

  areas_array_obj.push(novo_objeto);
}

var courses_array_obj = [];

for (var i = 0; i < courses_array.length; i++) {
  var elemento = courses_array[i];
  var id = elemento.id;
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


$("#timetable-courses div[data-toggle='buttons'] label").on("click", function() {
    var dataId = $(this).closest("div[data-id]").data("id");
    $("#cel-position").text(dataId).css("visibility", "hidden");

    $('#area-filter').val('');
    $('#block-filter').val('');
    $('#course-filter').val('');

    area_options();
    block_options();
    timetables_options();
    $("#addCourseModal").modal("show");
});

function area_options() {
    var areaOptionsDatalist = document.getElementById('area-options');
    areaOptionsDatalist.innerHTML  = '';

    for (var i = 0; i < areas_array_obj.length; i++) {
        var area = areas_array_obj[i];

        var option = document.createElement('option');
        option.value = area.id;
        option.textContent = "Área: " + area.acronym + " | " + area.name_area;
        areaOptionsDatalist.appendChild(option);
    }
}

function block_options() {
    var blockOptionsDatalist = document.getElementById('block-options');
    blockOptionsDatalist.innerHTML = '';

    for (var i = 0; i < blocks_array_obj.length; i++) {
        var block = blocks_array_obj[i];

        var option = document.createElement('option');
        option.value = block.id;
        option.textContent = "Bloco: " + block.acronym + " | " + block.name_block;
        blockOptionsDatalist.appendChild(option);
    }
}

function timetables_options() {
    var spanValue = $('#cel-position').text();

    var filteredElement = disponibility_array_obj.find(function(element) {
      return element.frase === spanValue;
    });

    var filteredTimetables = timetables_array_obj.filter(function(timetable) {
      var dayCombos = timetable.day_combo;

      for (var i = 0; i < dayCombos.length; i++) {
        var dayCombo = dayCombos[i];
        var timeslotDay = dayCombo.day.substring(0, 3);;
        var timeslots = dayCombo.timeslots;

        for (var j = 0; j < timeslots.length; j++) {
          var timeslot = timeslots[j];
          var timeslotHour = timeslot.hour_start;
          //alert(timeslotDay)
          if (timeslotHour === filteredElement.hour && timeslotDay === filteredElement.dia) {
            return true;
          }
        }
      }

      return false;
    });


    timetables = filteredTimetables;

    // Criar a lista de options para datalist com base nos cursos filtrados
    var timetableOptionsDatalist = document.getElementById('course-options');
    timetableOptionsDatalist.innerHTML = '';

    if(filteredTimetables.length == 0) {
      $('#course-filter').val('Nenhuma aula disponível neste horário.');
      $('#course-filter').prop('disabled', true);
    }

    for (var i = 0; i < filteredTimetables.length; i++) {
      $('#course-filter').prop('disabled', false);
        var timetable = filteredTimetables[i];

        var option = document.createElement('option');
        option.value = timetable.id;
        option.textContent = "Curso: " + timetable.course_name + " | " + timetable.classs;
        timetableOptionsDatalist.appendChild(option);
    }
}

function block_filter() {
  var block_value = $('#block-filter').val();
  $('#area-filter').val('');

  area_options();
  timetables_options();

  if (block_value == '') {

  } else {
    var filteredArray = areas_array_obj.filter(function(element) {
      return element.blocks.includes(block_value);
    });

    var areaOptionsDatalist = document.getElementById('area-options');
    areaOptionsDatalist.innerHTML  = '';

    for (var i = 0; i < filteredArray.length; i++) {
        var area = filteredArray[i];

        var option = document.createElement('option');
        option.value = area.id;
        option.textContent = "Área: " + area.acronym + " | " + area.name_area;
        areaOptionsDatalist.appendChild(option);
    }
  }



}

// function area_filter() {

// }

// Mapea na grade
for (var i = 0; i < disponibility_array_obj.length; i++) {
    var obj = disponibility_array_obj[i];

                 var filtered_disponibility = disponibility_array_obj.filter(function(disponibility) {
                      // tem todos as frases + posição
                      console.log("verdadeXXX?", disponibility.dia === day && disponibility.hour === hour_start)


                    return disponibility.dia === day && disponibility.hour === hour_start;
                  }); // dia=mon day=monday *colocar primeiras 3 letras

    console.log("disponibility array 1", obj)
    var fraseId = obj.frase;
    $("label[for='" + fraseId + "']")
    .removeClass("disabled").removeClass("btn-notchecked");
    $("label[for='" + fraseId + "']").css({
      "font-weight": "700",
      "color": "white",
      "background-color": "#2f7363",
    });
    $("#" + fraseId)
    .prop("disabled", false);
    $("#sub-" + fraseId).text("+");
    $("#btn-" + fraseId).attr("data-toggle", "modal").attr("data-target", "#addCourseModal");
}

$(document).ready(function() {
  $("#addCourseButton").on("click", function() {
        var timetable_id = parseInt($("#course-filter").val());
        console.log("timetable id", timetable_id);

        var courseFilterValue = $("#course-filter").val();
console.log("course filter value", courseFilterValue);

var timetable_id = parseInt(courseFilterValue);
console.log("timetable id", timetable_id);
        var grade_position = $("#cel-position").text(); //mon-mat-1 mon-mat-2 mon-mat-3
      console.log("grade position", grade_position )

        var filtered_timetable = timetables_array_obj.filter(function(timetable_item) {
          return timetable_item.id === timetable_id;
            console.log("oi")
        });

        console.log("filtered_timetable", filtered_timetable) // ok - pega todos os daycombos


        var csrftoken = $('[name=csrfmiddlewaretoken]').val();

        if (timetable_id !== "") {
          $.ajax({
            url: "/",
            type: "POST",
            data: {
              timetable: filtered_timetable
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                console.log("course acerony",filtered_timetable[0].course_acronym )
                $("#sub-" + grade_position).text(filtered_timetable[0].course_acronym);

                console.log("filteredx", filtered_timetable[0]); // ok
                // console.log("filteredx");
              var day_combo_data = filtered_timetable[0].day_combo; // erro, noa passa daqui
                console.log("day_combo_data", day_combo_data); // Já pega todos os dias com o timetable + timeslots *2

              for (var i = 0; i < day_combo_data.length; i++) {
                var day_combo = day_combo_data[i];
                var day = day_combo.day;
                console.log("dia 1", day)
                var timeslots = day_combo.timeslots;
                console.log("timeslots", timeslots);

                  console.log("Tamanho do timeslots:", timeslots.length);

                timeslots.forEach(function(timeslot) {
                  console.log("Entrou no loop forEach");
                  var hour_start = timeslot.hour_start;
                  console.log("hour_start", hour_start);

                  // Filtra o disponibility_array_obj pelo mesmo dia e hour_start
                  var filtered_disponibility = disponibility_array_obj.filter(function(disponibility) {
                      // tem todos as frases + posição
                      // console.log("filtered_disponibilityx", filtered_disponibility);
                      // console.log("filtered_disponibilityx");
                      console.log("verdade?", disponibility.dia === getDayOfWeekMenor(day) && disponibility.hour === hour_start)
                      console.log("dia before", day)
                    return disponibility.dia === getDayOfWeekMenor(day) && disponibility.hour === hour_start;
                  }); // dia=mon day=monday *colocar primeiras 3 letras - ok

                          console.log("FF filtered_disponibilityx", filtered_disponibility); // apenas do que clicou - frase: 'mon-mat-1', posicao: 1, sessao: 'mat', dia: 'mon', hour: '07:00:00
                      // console.log("FF filtered_disponibilityx");
                  // Extrai apenas a propriedade "frase" do objeto filtrado
                  var frases = filtered_disponibility.map(function(disponibility) {
                      console.log("fraseee", disponibility.frase)
                    return disponibility.frase;
                  }); // pegar a frase do timetable filtrado acima
                    console.log("frases", frases)

                  // if (frases.length > 0) {
                    console.log("acronimo anter", filtered_timetable);
                    console.log("acronimo", filtered_timetable[0].course_acronym);
                    frases.forEach(function(frase) {
                      $("#sub-" + frase).text(filtered_timetable[0].course_acronym);
                    }); // colocando acronym em todos do timetable
                  // }
                });
              }
                $("#sub-" + grade_position).text(filtered_timetable.course.acronym);

                timetable_global.push(filtered_timetable.id);
                $("#course-filter").val('');
                $('#error-alert').hide();
            },
            error: function(xhr, textStatus, errorThrown) {
                $('#error-message').text('Erro ao tentar adicionar uma aula.');
                $('#error-alert').show();alert("d")
            }
          });
        } else {
          $('#error-message').text('Selecione uma aula.');
          $('#error-alert').show();
        }
      });
});

function getDayOfWeekMenor(day) {
  var tresPrimeirasLetras = day

  if (tresPrimeirasLetras === 'monday') {
    return 'mon';
  } else if (tresPrimeirasLetras === 'tuesday') {
    return 'tue';
  } else if (tresPrimeirasLetras === 'wednesday') {
    return 'wed';
  } else if (tresPrimeirasLetras === 'thursday') {
    return 'thu';
  } else if (tresPrimeirasLetras === 'friday') {
    return 'fri';
  } else if (tresPrimeirasLetras === 'saturday') {
    return 'sat';
  } else {
    return 'Dia da semana errado';
  }
}