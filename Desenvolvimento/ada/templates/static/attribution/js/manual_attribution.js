var lang = document.currentScript.getAttribute("data-lang");
var timetables_user = document.currentScript.getAttribute("timetables-user");
var timetables_user_array = JSON.parse(timetables_user.replace(/'/g, '"'));

var timetables_user_array_obj = [];

for (var i = 0; i < timetables_user_array.length; i++) {
    var elemento = timetables_user_array[i];
    var phrase = elemento.phrase;
    var course_acronym = elemento.course_acronym;
    var course_name = elemento.course_name;

    var novo_objeto = {
        phrase: phrase,
        course_acronym: course_acronym,
        course_name: course_name,
    };
    timetables_user_array_obj.push(novo_objeto);
}


var user_regime = document.currentScript.getAttribute("user_regime");
var user_is_fgfcc = document.currentScript.getAttribute("user_is_fgfcc").replace(/'/g, '"');

var timetable_choosed = [];
var buttons_clicked = [];

var timetable_choosed_objects = []

var user_disponibility = JSON.parse(document.currentScript.getAttribute("user_disponibility").replace(/'/g, '"'));
var user_courses = JSON.parse(document.currentScript.getAttribute("user_courses").replace(/'/g, '"'));
var user_timetables = JSON.parse(document.currentScript.getAttribute("user_timetables").replace(/'/g, '"'));
var user_blocks = JSON.parse(document.currentScript.getAttribute("user_blocks").replace(/'/g, '"'));
var user_areas = JSON.parse(document.currentScript.getAttribute("user_areas").replace(/'/g, '"'));
var user_courses_from_blockk = JSON.parse(document.currentScript.getAttribute("user_courses_from_blockk").replace(/'/g, '"'));

var cell_left_number = {
    time: 21,
    type: ''
}

var type_discipline = {
    primary_max: 0,
    secondary_max: 0,
    primary_choosed: 0,
    secondary_choosed: 0,
}

if (user_regime == '20' || user_regime == 'Temporário') {
    cell_left_number.type = '20h';
    $('#count-cel').css({
        'color': '#913f3f'
    })
} else if (user_regime == '40' || user_regime == 'RDE' || user_regime == 'Substituto') {
    cell_left_number.type = '40h';
    $('#count-cel').css({
        'color': '#913f3f'
    })
}
$('#cel-hour').text('21')

for (var i = 0; i < user_disponibility.length; i++) {
    var obj = user_disponibility[i];
    var obj_id = obj.id;
    $("label[for='" + obj_id + "']")
        .removeClass("disabled")
        .removeClass("btn-notchecked");
    $("label[for='" + obj_id + "']").css({
        "font-weight": "700",
        "color": "white",
        "background-color": "#507c75",
    });
    $("#" + obj_id).prop("disabled", false);
    $("#sub-" + obj_id).text("+");
    $("#btn-" + obj_id)
        .attr("data-toggle", "modal")
        .attr("data-target", "#add-course-modal");
}

$("div.primary").css({
    "font-weight": "500",
    "background-color":  "#2f7363",
    "color": "white"
});
$('#secondary-timetable-courses').css({
    'display': 'none'
});

if(user_courses_from_blockk.length > 0) {
    for (var i = 0; i < user_courses_from_blockk.length; i++) { // colcoar primary na view
        var obj = user_courses_from_blockk[i];
        var obj_id = obj.id;
        var array_position_id = obj.position_id;
        var priority = array_position_id[0].id.substr(-3);
        var count = 0

        for (var y = 0; y < array_position_id.length; y++) {
            var position = array_position_id[y].id;
            count++
            $("#sub-" + position).text(user_courses_from_blockk[i].course_acronym);
            $("#btn-" + position)
                .attr("data-toggle", "none")
                .attr("data-target", "#");
            buttons_clicked.push(position);
        }

        if(priority == 'pri') {
            type_discipline.primary_choosed += count
        } else {
            type_discipline.secondary_choosed += count
        }


        global = {
            id_timetable: user_courses_from_blockk[i].id,
            position: array_position_id.map((objeto) => objeto.id.toString()),
        };
        timetable_choosed.push(global);
        cell_left_number.time -= array_position_id.length
        $('#cel-hour').text(cell_left_number.time)
        timetable_choosed_objects.push(user_courses_from_blockk[i])
        user_timetables = user_timetables.filter(timetable => timetable.id !== user_courses_from_blockk[i].id);
    }
}

function show_table(value) {
    $("#warning-list-message").empty();
    if(value == 1) {
        $('#primary-timetable-courses').css({
            'display': ''
        });
        $('#secondary-timetable-courses').css({
            'display': 'none'
        });
        $("div.primary").css({
            "font-weight": "500",
            "background-color":  "#2f7363",
            "color": "white"
        });
        $("div.secondary").css({
            "font-weight": "",
            "background-color":  "",
            "color": ""
        });
        window.scrollTo({
            top: $('#primary-timetable-courses').offset().top - $('.navbar').outerHeight() - 115,
            behavior: 'smooth'
          });
        if(type_discipline.primary_choosed <= 0){
            $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
        }
        if(cell_left_number.type == '20h') {
            if(type_discipline.primary_choosed >= 8) {                
            } else {
                $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
            }
        } else {
            if(user_is_fgfcc == 'True') {
                if(type_discipline.primary_choosed >= 8) {
                } else {
                    $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
                }
            } else {
                if(type_discipline.primary_choosed >= 12) {
                } else {
                    $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
                }
            }            
        }
        $('h4.primary-item').css({'display': ''})
        $('h4.secondary-item').css({'display': 'none'})
        cell_left_number.time = 21 - type_discipline.primary_choosed
        $('#cel-hour').text(cell_left_number.time)
    } else {       
        if(type_discipline.primary_choosed > 0) {
            if(cell_left_number.type == '20h') {
                if(type_discipline.primary_choosed >= 8) {                
                } else {
                    if(lang == 'pt-br' || lang == '') {
                        $("#warning-alert-message").text("Falta "+ (8 - type_discipline.primary_choosed) +" de células primárias minímas para continuar.");
                    } else {
                        $("#warning-alert-message").text("Missing "+ (8 - type_discipline.primary_choosed) +" minimum primary cells to continue.");
                    }
                    
                    $("#warning-alert").show();
                    window.scrollTo({
                        top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                        behavior: "smooth",
                    });
                    return false
                }
            } else {
                if(user_is_fgfcc == 'True') {
                    if(type_discipline.primary_choosed >= 8) {
                    } else {
                        if(lang == 'pt-br' || lang == '') {
                            $("#warning-alert-message").text("Falta "+ (8 - type_discipline.primary_choosed) +" de células primárias minímas para continuar.");
                        } else {
                            $("#warning-alert-message").text("Missing "+ (8 - type_discipline.primary_choosed) +" minimum primary cells to continue.");
                        }
                        
                        $("#warning-alert").show();
                        window.scrollTo({
                            top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                            behavior: "smooth",
                        });
                        return false
                    }
                } else {
                    if(type_discipline.primary_choosed >= 12) {
                    } else {
                        if(lang == 'pt-br' || lang == '') {
                            $("#warning-alert-message").text("Falta "+ (12 - type_discipline.primary_choosed) +" de células primárias minímas para continuar.");
                        } else {
                            $("#warning-alert-message").text("Missing "+ (12 - type_discipline.primary_choosed) +" minimum primary cells to continue.");
                        }
                        
                        $("#warning-alert").show();
                        window.scrollTo({
                            top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                            behavior: "smooth",
                        });
                        return false
                    }
                }
                
            }
            $('#secondary-timetable-courses').css({
            'display': ''
            });
            $('#primary-timetable-courses').css({
                'display': 'none'
            });
            $("div.secondary").css({
                "font-weight": "500",
                "background-color":  "#2f7363",
                "color": "white"
            });
            $("div.primary").css({
                "font-weight": "",
                "background-color":  "",
                "color": ""
            });
            window.scrollTo({
                top: $('#secondary-timetable-courses').offset().top - $('.navbar').outerHeight() - 115,
                behavior: 'smooth'
            });
            $('h4.primary-item').css({'display': 'none'})
            $('h4.secondary-item').css({'display': ''})
            cell_left_number.time = Math.floor(type_discipline.primary_choosed / 2)
            $('#cel-hour').text(cell_left_number.time)
        } else {
            if(cell_left_number.type == '20h') {
                if(lang == 'pt-br' || lang == '') {
                    $("#warning-alert-message").text("Insira a quantidade miníma de células primárias (8) antes de continuar.");
                } else {
                    $("#warning-alert-message").text("Enter the minimum number of primary cells (8) before continuing.");
                }
            } else {
                if(lang == 'pt-br' || lang == '') {
                    $("#warning-alert-message").text("Insira a quantidade miníma de células primárias (12) antes de continuar.");
                } else {
                    $("#warning-alert-message").text("Enter the minimum number of primary cells (12) before continuing.");
                }
            }
            
            $("#warning-alert").show();
            window.scrollTo({
                top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                behavior: "smooth",
            });
        }
        
    }
}

if(type_discipline.primary_choosed > 0){
    $('div.btn-priority.secondary').css({'color': '', 'background-color': '', 'border': '', 'font-weight': ''})
    $('i.secondary-item').css({'display': 'none'})
} else {
    $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
}


// Ao cliar no button
$("#primary-timetable-courses input, #secondary-timetable-courses input").on("click", function (event) {
    var data_id = $(this).closest("div[data-id]").data("id");
    $("#cel-position").text(data_id).css("visibility", "hidden");


    $("#area-filter").val("");
    $("#block-filter").val("");
    $("#course-filter").val("");

    area_options();
    timetables_options();
    block_options();
    $("#info-alert").hide();
    $("#error-alert").hide();
    $("#info-input-alert").hide();
    

    var updated_array = buttons_clicked.some(function (dict) {
        return dict.includes(data_id);
    });
    if (updated_array) {
        var filtered_timetables = timetable_choosed.filter(function (t) {
            return t.position.includes(data_id);
        });
        event.preventDefault();

        type_priority_choosed = 0

        filtered_timetables.forEach(function (timetable) {
            timetable.position.forEach(function (position) {
                $("#sub-" + position).text("+");
                $("#btn-" + position)
                    .attr("data-toggle", "modal")
                    .attr("data-target", "#add-course-modal");
                cell_left_number.time++;
                type_priority_choosed++;
            });
        });

        $('#cel-hour').text(cell_left_number.time)
        priority = filtered_timetables[0].position[0].substr(-3);
        if(priority == 'pri') {
            type_discipline.primary_choosed -= type_priority_choosed
        } else {
            type_discipline.secondary_choosed -= type_priority_choosed
        }

        buttons_clicked = buttons_clicked.filter(function (element) {
            return !filtered_timetables.some(function (timetable) {
              return timetable.position.includes(element);
            });
          });

        timetable_choosed = timetable_choosed.filter(function (t) {
            return !filtered_timetables.includes(t);
        });
        
        if(cell_left_number.type == '20h') {
            if(type_discipline.primary_choosed >= 8) {                
            } else {
                $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
                $('i.secondary-item').css({'display': ''})
            }
        } else {
            if(user_is_fgfcc == 'True') {
                if(type_discipline.primary_choosed >= 8) {
                } else {
                    $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
                    $('i.secondary-item').css({'display': ''})
                }
            } else {
                if(type_discipline.primary_choosed >= 12) {
                } else {
                    $('div.btn-priority.secondary').css({'color': 'grey', 'background-color': 'white', 'border': '1px solid grey', 'font-weight': '400'})
                    $('i.secondary-item').css({'display': ''})
                }
            }
        }

        obj = timetable_choosed_objects.filter(timetable => timetable.id == filtered_timetables[0].id_timetable)
        user_timetables.push(obj[0])
        timetable_choosed_objects = timetable_choosed_objects.filter(timetable => timetable.id !== filtered_timetables[0].id_timetable);

        return false;
    } else {
        $('.modal-backdrop').css({'display':''})
        $('#add-course-modal').modal('show');
    }
});

timatables_datalist_options = []


function block_options() {
    var block_datalist_options = document.getElementById("block-options");
    block_datalist_options.innerHTML = "";

    for (var i = 0; i < user_blocks.length; i++) {
        var block = user_blocks[i];
        var option = document.createElement("option");
        option.value = block.name;
        option.textContent = block.acronym + " - " + block.name;
        block_datalist_options.appendChild(option);
    }
}

function area_options() {
    var area_datalist_options = document.getElementById("area-options");
    area_datalist_options.innerHTML = "";

    for (var i = 0; i < user_areas.length; i++) {
        var area = user_areas[i];
        var option = document.createElement("option");
        option.value = area.name;
        option.textContent = area.acronym + " - " + area.name;
        area_datalist_options.appendChild(option);
    }
}

function timetables_options() {
    var span_value = $("#cel-position").text();

    var filtered_element = user_disponibility.find(function (element) {
        return element.id === span_value;
    });

    var filtered_timetables = user_timetables.filter(function (timetable) {
        var day_combos = timetable.day_combo;

<<<<<<< HEAD
        for (var i = 0; i < day_combos.length; i++) {
            var day_combo = day_combos[i];
            var timeslot_day = day_combo.day.substring(0, 3);
            var timeslots = day_combo.timeslots;

            for (var j = 0; j < timeslots.length; j++) {
                var timeslot = timeslots[j];
                var timeslot_hour = timeslot.timeslot_begin_hour;
                if (timeslot_hour === filtered_element.timeslot_begin_hour && timeslot_day === filtered_element.day) {
=======
        for (var i = 0; i < dayCombos.length; i++) {
            var dayCombo = dayCombos[i];
            var timeslotDay = dayCombo.day.substring(0, 3);
            var timeslots = dayCombo.timeslots;

            for (var j = 0; j < timeslots.length; j++) {
                var timeslot = timeslots[j];
                var timeslotHour = timeslot.timeslot_begin_hour;
                if (timeslotHour === filteredElement.timeslot_begin_hour && timeslotDay === filteredElement.dia) {
>>>>>>> f197f8f429b843c1556acf6d4394a3e6522a4f9f
                    return true;
                }
            }
        }

        return false;
    });

<<<<<<< HEAD
    timatables_datalist_options = filtered_timetables;
=======
    console.log(filteredTimetables);

    timatables_options = filteredTimetables;

    // filteredTimetables = timetables_array_obj
    // Criar a lista de options para datalist com base nos disciplinas filtrados
    var timetableOptionsDatalist = document.getElementById("course-options");
    timetableOptionsDatalist.innerHTML = "";
>>>>>>> f197f8f429b843c1556acf6d4394a3e6522a4f9f

    // Criar a lista de options para datalist com base nos disciplinas filtrados
    var timetable_datalist_options = document.getElementById("course-options");
    timetable_datalist_options.innerHTML = "";

    if (filtered_timetables.length == 0) {
        $("#course-filter").val("Nenhuma disciplina disponível neste horário.");
        $("#course-filter").prop("disabled", true);
    }

    for (var i = 0; i < filtered_timetables.length; i++) {
        $("#course-filter").prop("disabled", false);
        var timetable = filtered_timetables[i];
        var option = document.createElement("option");
        option.value = timetable.course_name;
        option.textContent = timetable.course_acronym + " - " + timetable.course_name;
        timetable_datalist_options.appendChild(option);
    }
}

$("#block-filter").on("input", function() {
    var block_value = $(this).val();
    var block_id = user_blocks.find(block => block.name === block_value)?.id;

    $("#area-filter").val("");
    $("#course-filter").val("");

    area_options();
    timetables_options();
    $("#info-alert").hide();
    $("#error-alert").hide();
    $("#info-input-alert").hide();
    
    if(block_id) {
        if (block_value == "") {
        } else {
            var filtered_areas = user_areas.filter(function (element) {
                return element.blocks.includes(block_id);
            });
    
            var area_datalist_options = document.getElementById("area-options");
            area_datalist_options.innerHTML = "";
    
            for (var i = 0; i < filtered_areas.length; i++) {
                var area = filtered_areas[i];
    
                var option = document.createElement("option");
                option.value = area.name;
                option.textContent = area.acronym + " - " + area.name;
                area_datalist_options.appendChild(option);
            }
    
            var filtered_timetables = timatables_datalist_options.filter(function (timetable) {
                return user_courses.some(function (course) {
                    return course.block === block_id && course.id === timetable.course_id;
                });
            });
    
            var course_datalist_options = document.getElementById("course-options");
            course_datalist_options.innerHTML = "";
    
            for (var i = 0; i < filtered_timetables.length; i++) {
                $("#course-filter").prop("disabled", false);
                var timetable = filtered_timetables[i];
                var option = document.createElement("option");
                option.value = timetable.course_name;
                option.textContent = timetable.course_acronym + " - " + timetable.course_name;
                course_datalist_options.appendChild(option);
            }
    
            if (filtered_timetables.length == 0) {
                if(lang == 'pt-br' || lang == '') {
                    $("#course-filter").val("Nenhuma disciplina disponível neste horário.");
                } else {
                    $("#course-filter").val("No courses available at this time.");
                }
                $("#course-filter").prop("disabled", true);
            }
        }
        this.style.borderColor = "";
    } else {
        this.style.borderColor = "red";
        
    }
});

$("#block-filter").on("blur", function() {
    isInputSelected = false;
    
    if ($(this).val() === "") {
        this.style.borderColor = "";
    }
});

$("#area-filter").on("blur", function() {
    isInputSelected = false;
    
    if ($(this).val() === "") {
        this.style.borderColor = "";
    }
});

$("#course-filter").on("blur", function() {
    isInputSelected = false;

    if ($(this).val() === "") {
        this.style.borderColor = "";
    }
});

$("#area-filter").on("input", function() {
    var area_value = $(this).val();
    var block_value = $("#block-filter").val();

    $("#info-alert").hide();
    $("#error-alert").hide();
    $("#info-input-alert").hide();

    var area_id = user_areas.find(area => area.name === area_value)?.id;
    var block_id = user_blocks.find(block => block.name === block_value)?.id;
    $("#course-filter").val("");

    block_options();
    timetables_options();

    if(area_id) {
        if (area_value == "") {
        } else {
            if (block_value == "") {
                var filtered_timetables = timatables_datalist_options.filter(function (timetable) {
                    return user_courses.some(function (course) {
                        return course.area === area_id && course.id === timetable.course_id;
                    });
                });

                var area_obj = user_areas.filter(function (element) {
                    return element.id == area_id;
                });

                var block_to_area = user_blocks.filter(function (element) {
                    return area_obj[0].blocks.includes(element.id);
                });

                var course_datalist_options = document.getElementById("course-options");
                course_datalist_options.innerHTML = "";
    
                for (var i = 0; i < filtered_timetables.length; i++) {
                    $("#course-filter").prop("disabled", false);
                    var timetable = filtered_timetables[i];
                    var option = document.createElement("option");
                    option.value = timetable.course_name;
                    option.textContent = timetable.course_acronym + " - " + timetable.course_name;
                    course_datalist_options.appendChild(option);
                }
    
                if (filtered_timetables.length == 0) {
                    if(lang == 'pt-br' || lang == '') {
                        $("#course-filter").val("Nenhuma disciplina disponível neste horário.");
                    } else {
                        $("#course-filter").val("No courses available at this time.");
                    }
                    $("#course-filter").prop("disabled", true);
                }
    
                var block_datalist_options = document.getElementById("block-options");
                block_datalist_options.innerHTML = "";
    
                for (var i = 0; i < block_to_area.length; i++) {
                    var block = block_to_area[i];
                    var option = document.createElement("option");
                    option.value = block.name;
                    option.textContent = block.acronym + " - " + block.name;
                    block_datalist_options.appendChild(option);
                }
            } else {
                var filtered_timetables = timatables_datalist_options.filter(function (timetable) {
                    return user_courses.some(function (course) {
                        return course.block === block_id && course.area === area_id && course.id === timetable.course_id;
                    });
                });
    
                var course_datalist_options = document.getElementById("course-options");
                course_datalist_options.innerHTML = "";
    
                for (var i = 0; i < filtered_timetables.length; i++) {
                    $("#course-filter").prop("disabled", false);
                    var timetable = filtered_timetables[i];
                    var option = document.createElement("option");
                    option.value = timetable.course_name;
                    option.textContent = timetable.course_acronym + " - " + timetable.course_name;
                    course_datalist_options.appendChild(option);
                }
    
                if (filtered_timetables.length == 0) {
                    if(lang == 'pt-br' || lang == '') {
                        $("#course-filter").val("Nenhuma disciplina disponível neste horário.");
                    } else {
                        $("#course-filter").val("No courses available at this time.");
                    }
                    $("#course-filter").prop("disabled", true);
                }
            }
        } 
        this.style.borderColor = "";
    } else {
        this.style.borderColor = "red";
    }
});

$("#course-filter").on("input", function() {
    var course_value = $(this).val();
    var course_id = timatables_datalist_options.find(timetable => timetable.course_name === course_value)?.id;
    $("#info-alert").hide();
    $("#error-alert").hide();
    $("#info-input-alert").hide();

    if(course_id) {
        var filtered_timetable = timatables_datalist_options.filter(function(timetable) {
            return timetable.id == course_id;
          });
      
          var discipline_name;
          var classs;
          var day;
          var timeslot_begin_hour;
          var timeslot_end_hour;
      
          filtered_timetable.forEach(function(timetable) {
              discipline_name = timetable.course_acronym
              classs = timetable.classs
              timetable.day_combo.forEach(function(day_combo) {
                  day = get_all_day(get_full_day_of_week(day_combo.day));
                  var timeslots = day_combo.timeslots;
                  var day_combo_size = timeslots.length
                  var count = 0
          
                  timeslots.forEach(function(timeslot) {
                      if(count == 0) {
                          timeslot_begin_hour = timeslot.timeslot_begin_hour;
                      } else if(count == day_combo_size - 1) {
                          timeslot_end_hour = timeslot.timeslot_end_hour;
                      }
                      count += 1;
                  });
                  if(!timeslot_end_hour) {
                    timeslots.forEach(function(timeslot) {
                        timeslot_end_hour = timeslot.timeslot_end_hour;

                    });
                  }
              });
          });

          
      
          $(".info-displine").text(discipline_name);
          $(".info-day").text(day);
          $(".info-start-hour").text(timeslot_begin_hour.slice(0, -3));
          $(".info-end-hour").text(timeslot_end_hour.slice(0, -3));
          $(".info-class").text(classs);
        
          $("#info-alert").show();
          if (isNaN(course_id) || course_value == '') {
              $("#info-alert").hide();
            }
        this.style.borderColor = "";
    } else {
        this.style.borderColor = "red";
    }

});

// Mapea na grade


$(document).ready(function () {
    $("#add-course-button").on("click", function () {
        var timetable_acronym = $("#course-filter").val();
        var timetable_id = timatables_datalist_options.find(timetable => timetable.course_name === timetable_acronym)?.id;
        var grade_position = $("#cel-position").text(); //mon-mor-1 mon-mor-2 mon-mor-3
        var priority = grade_position.substr(-3);

        var filtered_timetable = user_timetables.filter(function (timetable_item) {
            return timetable_item.id === timetable_id;
        });

        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        if (typeof timetable_id === "number" && !isNaN(timetable_id) && timetable_id !== "") {
            $.ajax({
                url: "/",
                type: "POST",
                data: {
                    timetable: filtered_timetable,
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (response) {
                    var day_combo_data = filtered_timetable[0].day_combo;
                    var is_repetead = false;
                    var id_array = [];           
                    var ids_repetead = [];
                    var is_missing = false;
                    var missing_courses = [];
                    var max_cel = false;
                    var length_ids = 0;
                    var type_priority_choosed = 0                    
                    
                    function format_id(id) {
                        var split_parts = id.split("-");
                        var class_number = split_parts[2];
                        var day_of_week = get_all_day(split_parts[0]);
                        if(lang == 'pt-br' || lang == '') {
                            var period = split_parts[1] == "mor" ? "Matutino" : split_parts[1] == "aft" ? "Vespertino" : "Noturno";
                        } else {
                            var period = split_parts[1] == "mor" ? "Morning" : split_parts[1] == "aft" ? "Afternoon" : "Nocturnal";
                        }
                

                        if(lang == 'pt-br' || lang == '') {
                            return class_number + "º aula " + day_of_week + ", " + period;
                        } else {
                            return class_number + "º timeslot " + day_of_week + ", " + period;
                        }
                    }

                    for (var i = 0; i < day_combo_data.length; i++) {
                        var day_combo = day_combo_data[i];
                        var day = day_combo.day;
                        var timeslots = day_combo.timeslots;

                        timeslots.forEach(function(timeslot) {
                            var timeslot_begin_hour = timeslot.timeslot_begin_hour;
                        
                            var filtered_disponibility = user_disponibility.filter(function(disponibility) {
                              return disponibility.day === get_full_day_of_week(day) && disponibility.timeslot_begin_hour === timeslot_begin_hour && priority == disponibility.priority;
                            });
                        
                            var ids = filtered_disponibility.map(function(disponibility) {
                              return disponibility.id;
                            });

                            ids.forEach(function(id) {
                                length_ids ++;
                                type_priority_choosed++;
                                if (buttons_clicked.includes(id)) {
                                  is_repetead = true;
                                  ids_repetead.push(format_id(id));
                                }
                              });

                            if(ids[0] == null) {
                                is_missing = true;
                                if (!missing_courses.includes(filtered_timetable[0].course_acronym)) {
                                    missing_courses.push(filtered_timetable[0].course_acronym);
                                }
                                missing_courses = [...new Set(missing_courses)];
                            }                       
                            
                        });
                    }

                    var will_zero_or_negative = (cell_left_number.time - length_ids) < 0;

                    if(will_zero_or_negative) {
                        max_cel = true
                        if(lang == 'pt-br' || lang == '') {
                            $("#error-message-form").text("Você atingiu o máximo de células.");
                        } else {
                            $("#error-message-form").text("You have reached the maximum number of cells.");
                        }
                        $("#error-alert-form").show();
                        window.scrollTo({
                            top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                            behavior: "smooth",
                        });
                    }

                    for (var i = 0; i < day_combo_data.length; i++) {
                        var day_combo = day_combo_data[i];
                        var day = day_combo.day;
                        var timeslots = day_combo.timeslots;

                        timeslots.forEach(function (timeslot) {
                            var timeslot_begin_hour = timeslot.timeslot_begin_hour;

                            var filtered_disponibility = user_disponibility.filter(function (disponibility) {
                                return disponibility.day === get_full_day_of_week(day) && disponibility.timeslot_begin_hour === timeslot_begin_hour && priority == disponibility.priority;
                            });

                            var ids = filtered_disponibility.map(function (disponibility) {
                                return disponibility.id;
                            });

                            if (!is_repetead && !is_missing && !max_cel) {
                                ids.forEach(function (id) {
                                    if (!buttons_clicked.includes(id)) {
                                        $("#sub-" + id).text(filtered_timetable[0].course_acronym);                                        
                                        id_array.push(id);
                                        $("#btn-" + id)
                                            .attr("data-toggle", "none")
                                            .attr("data-target", "#");
                                        buttons_clicked.push(id);
                                    }
                                });
                            }                            
                        });
                    }
                    
                    $("#modal-" + grade_position)
                        .attr("data-toggle", "none")
                        .attr("data-target", "#");

                    global = {
                        id_timetable: filtered_timetable[0].id,
                        position: id_array,
                    };
                    if (!is_repetead && !is_missing && !max_cel) {
                        if(priority == 'pri') {
                            type_discipline.primary_choosed += type_priority_choosed 
                        } else {
                            type_discipline.secondary_choosed += type_priority_choosed
                        }
                        timetable_choosed.push(global);
                        cell_left_number.time -= id_array.length
                        $('#cel-hour').text(cell_left_number.time)
                        timetable_choosed_objects.push(filtered_timetable[0])
                        user_timetables = user_timetables.filter(timetable => timetable.id !== filtered_timetable[0].id);
                        $("#warning-alert").hide();
                    }

                    $("#course-filter").val("");
                    $("#error-alert").hide();
                    $("#warning-alert").hide();
                    if (ids_repetead.length > 0) {                        
                        var lists_repetead = ids_repetead.map(function(id) {
                          return "<li>" + id + "</li>";
                        }).join("");

                        $("#warning-list-message").empty();
                        $("#warning-list-message").html("<ul>" + lists_repetead + "</ul>");
                        if(lang == 'pt-br' || lang == '') {
                            $("#warning-alert-message").text("Os seguintes períodos já estão ocupados por outras matérias já escolhidas:");
                        } else {
                            $("#warning-alert-message").text("The following periods are already occupied by other subjects already chosen:");
                        }
                        
                        $("#warning-alert").show();
                        window.scrollTo({
                            top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                            behavior: "smooth",
                        });
                    }
                    
                    if (missing_courses.length > 0) {
                        var lists_courses = missing_courses.map(function(id) {
                            return "<li>" + id + "</li>";
                          }).join("");
                          $("#warning-list-message").html("<ul>" + lists_courses + "</ul>");
                          if(lang == 'pt-br' || lang == '') {
                                $("#warning-alert-message").text("As seguintes disciplinas estão ultrapassando o escolhido na disponibilidade geral:");
                            } else {
                                $("#warning-alert-message").text("The following disciplines are surpassing the chosen one in general availability:");
                            }
                          $("#warning-alert").show();
                          window.scrollTo({
                            top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                            behavior: "smooth",
                        });
                    }

                    if(type_discipline.primary_choosed > 0){
                        if(cell_left_number.type == '20h') {
                            if(type_discipline.primary_choosed >= 8) {                
                            } else {
                                return false
                            }
                        } else {
                            if(user_is_fgfcc == 'True') {
                                if(type_discipline.primary_choosed >= 8) {
                                } else {
                                    return false
                                }
                            } else {
                                if(type_discipline.primary_choosed >= 12) {
                                } else {
                                    return false
                                }
                            }
                        }
                        if(priority == 'pri') {
                            $('div.btn-priority.secondary').css({'color': '', 'background-color': '', 'border': '', 'font-weight': ''})
                            $('i.secondary-item').css({'display': 'none'})
                        } else {
                            $("div.secondary").css({
                                "font-weight": "500",
                                "background-color":  "#2f7363",
                                "color": "white"
                            });
                        }                        
                    }

                    $("#info-alert").hide();
                    $('.modal-backdrop').css({'display':'none'})
                    // $('#add-course-modal').modal('hide');
                },
                error: function (xhr, textStatus, errorThrown) {
                    if(lang == 'pt-br' || lang == '') {
                        $("#error-message-form").text("Erro ao tentar suas preferências de disciplinas.");
                    } else {
                        $("#error-message-form").text("Error trying your subject preferences.");
                    }
                    $("#error-alert-form").show();
                    window.scrollTo({
                        top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                        behavior: "smooth",
                    });
                },
            });
        } else {
            if(lang == 'pt-br' || lang == '') {
                $("#error-message-form").text("Por favor, selecione a disciplina no modal.");
            } else {
                $("#error-message-form").text("Please select your subject in the modal.");
            }
            $("#error-alert-form").show();
            window.scrollTo({
                top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                behavior: "smooth",
            });
        }
    });
    $("#send-courses").on("click", function () {
        let csrftoken = get_cookie("csrftoken");
        var json_data = JSON.stringify(timetable_choosed);

        if (timetable_choosed.length != 0) {
            if(type_discipline.secondary_choosed == 0) {
                if(lang == 'pt-br' || lang == '') {
                    $("#warning-alert-message").text("Você não selecionou nenhuma disciplina secundária. Conforme o escolhido, você deve inserir " + Math.floor(type_discipline.primary_choosed/2) + " células secundárias.");
                } else {
                    $("#warning-alert-message").text("You have not selected any secondary disciplines. As chosen, you must insert " + Math.floor(type_discipline.primary_choosed/2) + " secondary cells.");
                }
                
                $("#warning-alert").show();                
                show_table(2)
                window.scrollTo({
                    top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                    behavior: "smooth",
                });
                return false;
            }
            if(cell_left_number.type == '20h' || user_is_fgfcc == 'True') {
                if(type_discipline.primary_choosed >= 8) {
                    $.ajax({
                        type: "post",
                        url: "/" + lang + "/professor/preferencia-atribuicao/",
                        data: {
                            timetable: json_data,
                        },
                        headers: {
                            "X-CSRFToken": csrftoken,
                        },
                        success: function (response) {
                            $("#course-filter-form").val("");
                            $("#error-alert-form").hide();
                            window.location.href = "/" + lang + "/professor/preferencia-atribuicao/";
                        },
                        error: function (xhr, textStatus, errorThrown) {
                            if(lang == 'pt-br' || lang == '') {
                                $("#error-message-form").text("Erro ao tentar suas preferências de disciplinas.");
                            } else {
                                $("#error-message-form").text("Error trying your subject preferences.");
                            }
                            $("#error-alert-form").show();
                            window.scrollTo({
                                top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                                behavior: "smooth",
                            });
                        },
                    });
                } else {
                    if(lang == 'pt-br' || lang == '') {
                        $("#error-message-form").text("Quantidade de células minímas para seu FPA segundo seu regime é 8 células.");
                    } else {
                        $("#error-message-form").text("Minimum amount of cells for your FPA according to your regime is 8 cells.");
                    }
                    $("#error-alert-form").show();
                    window.scrollTo({
                        top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                        behavior: "smooth",
                    });
                }
            } else {
                if(type_discipline.primary_choosed >= 12) {
                    $.ajax({
                        type: "post",
                        url: "/" + lang + "/professor/preferencia-atribuicao/",
                        data: {
                            timetable: json_data,
                        },
                        headers: {
                            "X-CSRFToken": csrftoken,
                        },
                        success: function (response) {
                            $("#course-filter-form").val("");
                            $("#error-alert-form").hide();
                            window.location.href = "/" + lang + "/professor/preferencia-atribuicao/";
                        },
                        error: function (xhr, textStatus, errorThrown) {
                            if(lang == 'pt-br' || lang == '') {
                                $("#error-message-form").text("Erro ao tentar suas preferências de disciplinas.");
                            } else {
                                $("#error-message-form").text("Error trying your subject preferences.");
                            }
                            $("#error-alert-form").show();
                            window.scrollTo({
                                top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                                behavior: "smooth",
                            });
                        },
                    });
                } else {
                    if(lang == 'pt-br' || lang == '') {
                        $("#error-message-form").text("Quantidade de células minímas para seu FPA segundo seu regime é 12 células.");
                    } else {
                        $("#error-message-form").text("Minimum cell count for your FPA according to your regimen is 12 cells.");
                    }
                    $("#error-alert-form").show();
                    window.scrollTo({
                        top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                        behavior: "smooth",
                    });
                }
            }
        } else {
            if(lang == 'pt-br' || lang == '') {
                $("#error-message-form").text("Por favor, selecione suas disciplinas.");
            } else {
                $("#error-message-form").text("Please select your subjects.");
            }
            $("#error-alert-form").show();
            window.scrollTo({
                top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                behavior: "smooth",
            });
        }
    });

    function get_cookie(name) {
        var cookie_value = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookie_value;
    }
});

function get_full_day_of_week(short_day) {
    const day_mappings = {
        monday: "mon",
        tuesday: "tue",
        wednesday: "wed",
        thursday: "thu",
        friday: "fri",
        saturday: "sat",
    };

    return day_mappings[short_day] || "Nenhum day correspondente";
}

function get_all_day(abreviation_day) {
    if(lang == 'pt-br' || lang == '') {
        var days = {
            mon: "Segunda-feira",
            tue: "Terça-feira",
            wed: "Quarta-feira",
            thu: "Quinta-feira",
            fri: "Sexta-feira",
            sat: "Sábado",
          };
    } else {
        var days = {
            mon: "Monday",
            tue: "Tuesday",
            wed: "Wednesday",
            thu: "Thursday",
            fri: "Friday",
            sat: "Saturday",
          };
    }

    if(lang == 'pt-br' || lang == '') {
        return days[abreviation_day] || "Nenhum dia correspondente";
    } else {
        return days[abreviation_day] || "Any day corresponding";
    }
}

function info_button(value) {
    var infoMessage = $("#info-input-message").text();

    $("#info-input-message").empty();
    if (value === 'block') {
        var word_to_search = 'Bloco';
        if(lang == 'pt-br' || lang == '') {
            $("#info-input-message").text("O filtro de Bloco serve para filtrar todas as disciplinas disponíveis apenas aquelas com o mesmo bloco pedido. Exemplo: Técnico - Aulas do técnico apenas.");
        } else {
            $("#info-input-message").text("The Block filter is used to filter all available disciplines, only those with the same requested block. Example: Technician - Technician classes only.");
        }
        
    } else if (value === 'area') {
        var word_to_search = 'Área';
        if(lang == 'pt-br' || lang == '') {
            $("#info-input-message").text("O filtro de Área serve para filtrar todas as disciplinas disponíveis apenas aquelas com a mesma área pedida. Exemplo: ADS - Aulas de análise e desenvolvimento de sistemas apenas.");
        } else {
            $("#info-input-message").text("The Area filter is used to filter all available disciplines only those with the same requested area. Example: ADS - Systems analysis and development classes only."); 
        }
        
    }

    if ($("#info-input-alert").css("display") === "block" && infoMessage.indexOf(word_to_search) !== -1) {
        $("#info-input-alert").hide();
    } else {
        $("#info-input-alert").show();
    }
}



