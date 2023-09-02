var lang = document.currentScript.getAttribute("data-lang");
var user_regime = document.currentScript.getAttribute("user_regime");
var user_disponibility_choosed = document.currentScript.getAttribute("user_disponibility_choosed");
var user_courses_choosed = document.currentScript.getAttribute("user_courses_choosed");

var user_disponibility_choosed_array = JSON.parse(user_disponibility_choosed.replace(/'/g, '"'));
var user_courses_choosed_array = JSON.parse(user_courses_choosed.replace(/'/g, '"'));

$('.'+ user_regime).css({
    "background-color": "#285f5236",
    "color": "#507c75",
    "font-weight": 700
})

var tables_checked = {
    mor_pri: false,
    aft_pri: false,
    noc_pri: false,
    mor_sec: false,
    aft_sec: false,
    noc_sec: false,
}

for(var i = 0; i < user_disponibility_choosed_array.length; i++) {
    var element = user_disponibility_choosed_array[i];
    var id = element.id;
    var idParts = id.split('-');
    var time = idParts[1]; // mor, aft, noc
    var priority = idParts[3]; // sec ou pri

    $('#btn-'+ id).css({
        "background-color": "#285f5236",
    });
    $("#" + id + " i").addClass("fas fa-check-circle check");
    $('#'+ id).css({
        "color": "#507c75",
    });

    var key = time + '_' + priority;
    if (tables_checked.hasOwnProperty(key)) {
        tables_checked[key] = true;
    }
}


for (var i = 0; i < user_courses_choosed_array.length; i++) {
    var course = user_courses_choosed_array[i];
    var acronym = course.acronym;
    var name_course = course.name_course;
    var priority_attr = course.priority_attr;
    var course_area = course.course_area;
    var period = course.period;
    var classes = course.classes;
    var id_positions = course.id_position;

    for (var y = 0; y < id_positions.length; y++) {
        var id_position = id_positions[y].id;
        $("#" + id_position + " i").removeClass("fas fa-check-circle check");
        $("#" + id_position).text(acronym);
        $('#'+ id_position).css({
            "font-weight": "600",
        });
    }

    period_language = period

    if(period_language == 'morning' && lang == 'pt-br') {
        period_language = 'matutino'
    } else if(period_language == 'afternoon' && lang == 'pt-br') {
        period_language = 'vespertino'
    } else if(period_language == 'nocturnal' && lang == 'pt-br') {
        period_language = 'noturno'
    }

    if(priority_attr == 'priority' && lang == 'pt-br') {
        priority_attr = 'prioritária'
    } else if(priority_attr == 'secondary' && lang == 'pt-br') {
        priority_attr = 'secundária'
    }
  
    var new_row = '<tr>' +
      '<td class="text-center align-middle">' + acronym + '</td>' +
      '<td class="text-center align-middle">' + name_course + '</td>' +
      '<td class="text-center align-middle">' + course_area + '</td>' +
      '<td class="text-center align-middle">' + primeiraLetraMaiuscula(priority_attr) + '</td>' +
      '<td class="text-center align-middle">' + primeiraLetraMaiuscula(period_language) + '</td>' +
      '<td class="text-center align-middle">' + classes + '</td>' +
      '</tr>';
  
    $('#courses-list').append(new_row);
  }

function primeiraLetraMaiuscula(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
  
if (!tables_checked.mor_pri) {
    $('.mor-pri').css({
        "display": "none",
    });
}
if (!tables_checked.aft_pri) {
    $('.aft-pri').css({
        "display": "none",
    });
}
if (!tables_checked.noc_pri) {
    $('.noc-pri').css({
        "display": "none",
    });
}
if (!tables_checked.mor_sec) {
    $('.mor-sec').css({
        "display": "none",
    });
}
if (!tables_checked.aft_sec) {
    $('.aft-sec').css({
        "display": "none",
    });
}
if (!tables_checked.noc_sec) {
    $('.noc-sec').css({
        "display": "none",
    });
}

