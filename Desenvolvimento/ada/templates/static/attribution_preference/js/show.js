var lang = document.currentScript.getAttribute("data-lang");
var user_regime = document.currentScript.getAttribute("user_regime");
var user_disponibility_choosed = document.currentScript.getAttribute("user_disponibility_choosed");
var user_courses_choosed = document.currentScript.getAttribute("user_courses_choosed");

var user_disponibility_choosed_array = JSON.parse(user_disponibility_choosed.replace(/'/g, '"'));
var user_courses_choosed_array = JSON.parse(user_courses_choosed.replace(/'/g, '"'));


$('.'+ user_regime).css({
    "background-color": "#507c75",
    "color": "white",
    "font-weight": 700
})

for(var i = 0; i < user_disponibility_choosed_array.length; i++) {
    var element = user_disponibility_choosed_array[i];
    var id = element.id;

    $('#btn-'+ id).css({
        "background-color": "#507c75",
    });
    $("#" + id + " i").addClass("fas fa-check-circle check");
    $('#'+ id).css({
        "color": "white",
    });
}

for (var i = 0; i < user_courses_choosed_array.length; i++) {
    var course = user_courses_choosed_array[i];
    var acronym = course.acronym;
    var name_course = course.name_course;
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
  
    var new_row = '<tr>' +
      '<td class="text-center">' + acronym + '</td>' +
      '<td class="text-center">' + name_course + '</td>' +
      '<td class="text-center">' + course_area + '</td>' +
      '<td class="text-center">' + period_language + '</td>' +
      '<td class="text-center">' + classes + '</td>' +
      '</tr>';
  
    $('#courses-list').append(new_row);
  }


