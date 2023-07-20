var lang = document.currentScript.getAttribute("data-lang");
var user_regime = document.currentScript.getAttribute("user_user_regime");

var timetable_choosed = [];
var buttons_clicked = [];

var user_disponibility = JSON.parse(document.currentScript.getAttribute("user_disponibility").replace(/'/g, '"'));
var user_courses = JSON.parse(document.currentScript.getAttribute("user_courses").replace(/'/g, '"'));
var user_timetables = JSON.parse(document.currentScript.getAttribute("user_timetables").replace(/'/g, '"'));
var user_blocks = JSON.parse(document.currentScript.getAttribute("user_blocks").replace(/'/g, '"'));
var user_areas = JSON.parse(document.currentScript.getAttribute("user_areas").replace(/'/g, '"'));

var user_disponibility_obj = [];
for (var i = 0; i < user_disponibility.length; i++) {
    var elemento = user_disponibility[i];
    var id = elemento.id;
    var position = elemento.position;
    var type = elemento.type;
    var day = elemento.day;
    var timeslot_begin_hour = elemento.timeslot_begin_hour;

    var novo_objeto = {
        id: id, // mon-aft-3
        position: position,
        type: type,
        day: day,
        timeslot_begin_hour: timeslot_begin_hour, // 7:45:00
    };

    user_disponibility_obj.push(novo_objeto);
}

var user_timetables_obj = [];
for (var i = 0; i < user_timetables.length; i++) {
    var timetable_object = user_timetables[i];
    var timetable_id = timetable_object.id;
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
                timeslot_begin_hour: timeslot.timeslot_begin_hour,
                timeslot_end_hour: timeslot.timeslot_end_hour,
            });
        }
        day_combo_data.push({
            day: day,
            timeslots: timeslot_data,
        });
    }

    var timetable_item = {
        id: timetable_id,
        day_combo: day_combo_data,
        course_acronym: timetable_object.course_acronym,
        course_id: timetable_object.course_id,
        course_name: timetable_object.course_name,
        classs: timetable_object.classs,
    };
    user_timetables_obj.push(timetable_item);
}

var user_blocks_obj = [];
for (var i = 0; i < user_blocks.length; i++) {
    var elemento = user_blocks[i];
    var id = elemento.id;
    var name_block = elemento.name;
    var acronym = elemento.acronym;

    var novo_objeto = {
        id: id,
        name_block: name_block,
        acronym: acronym,
    };

    user_blocks_obj.push(novo_objeto);
}

var user_areas_obj = [];

for (var i = 0; i < user_areas.length; i++) {
    var elemento = user_areas[i];
    var id = elemento.id;
    var name_area = elemento.name;
    var acronym = elemento.acronym;
    var blocks = elemento.blocks;

    var novo_objeto = {
        id: id,
        name_area: name_area,
        acronym: acronym,
        blocks: blocks,
    };

    user_areas_obj.push(novo_objeto);
}

var user_courses_obj = [];

for (var i = 0; i < user_courses.length; i++) {
    var elemento = user_courses[i];
    var id = elemento.id;
    var course_name = elemento.name;
    var acronym = elemento.acronym;
    var area = elemento.area;
    var block = elemento.block;

    var novo_objeto = {
        id: id,
        course_name: course_name,
        acronym: acronym,
        area: area,
        block: block,
    };
    user_courses_obj.push(novo_objeto);
}

var cell_left_number = {
    time: 21,
    type: ''
}

if (user_regime == '20') {
    cell_left_number.type = '20h';
    $('#count-cel').css({
        'color': '#913f3f'
    })
} else if (user_regime == '40' || user_regime == 'rde') {
    cell_left_number.type = '40h';
    $('#count-cel').css({
        'color': '#913f3f'
    })
}
$('#cel-hour').text('21')

for (var i = 0; i < user_disponibility_obj.length; i++) {
    var obj = user_disponibility_obj[i];
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

// Ao cliar no button
$("#timetable-courses input").on("click", function () {
    var data_id = $(this).closest("div[data-id]").data("id");
    $("#cel-position").text(data_id).css("visibility", "hidden");

    $("#area-filter").val("");
    $("#block-filter").val("");
    $("#course-filter").val("");

    area_options();
    block_options();
    timetables_options();
    $("#info-alert").hide();
    

    var updated_array = buttons_clicked.some(function (dict) {
        return dict.includes(data_id);
    });
    if (updated_array) {
        var filtered_timetables = timetable_choosed.filter(function (t) {
            return t.position.includes(data_id);
        });

        filtered_timetables.forEach(function (timetable) {
            timetable.position.forEach(function (position) {
                $("#sub-" + position).text("+");
                $("#btn-" + position)
                    .attr("data-toggle", "modal")
                    .attr("data-target", "#add-course-modal");
                cell_left_number.time += 1;
            });
        });

        $('#cel-hour').text(cell_left_number.time)

        buttons_clicked = buttons_clicked.filter(function (element) {
            return !filtered_timetables.some(function (timetable) {
              return timetable.position.includes(element);
            });
          });

        timetable_choosed = timetable_choosed.filter(function (t) {
            return !filtered_timetables.includes(t);
        });
    }
});

timatables_datalist_options = []

function area_options() {
    var area_datalist_options = document.getElementById("area-options");
    area_datalist_options.innerHTML = "";

    for (var i = 0; i < user_areas_obj.length; i++) {
        var area = user_areas_obj[i];
        var option = document.createElement("option");
        option.value = area.acronym;
        option.textContent = area.acronym + " | " + area.name_area;
        area_datalist_options.appendChild(option);
    }
}

function block_options() {
    var block_datalist_options = document.getElementById("block-options");
    block_datalist_options.innerHTML = "";

    for (var i = 0; i < user_blocks_obj.length; i++) {
        var block = user_blocks_obj[i];
        var option = document.createElement("option");
        option.value = block.acronym;
        option.textContent = block.acronym + " | " + block.name_block;
        block_datalist_options.appendChild(option);
    }
}

function timetables_options() {
    var span_value = $("#cel-position").text();

    var filtered_element = user_disponibility_obj.find(function (element) {
        return element.id === span_value;
    });

    var filtered_timetables = user_timetables_obj.filter(function (timetable) {
        var day_combos = timetable.day_combo;

        for (var i = 0; i < day_combos.length; i++) {
            var day_combo = day_combos[i];
            var timeslot_day = day_combo.day.substring(0, 3);
            var timeslots = day_combo.timeslots;

            for (var j = 0; j < timeslots.length; j++) {
                var timeslot = timeslots[j];
                var timeslot_hour = timeslot.timeslot_begin_hour;
                if (timeslot_hour === filtered_element.timeslot_begin_hour && timeslot_day === filtered_element.day) {
                    return true;
                }
            }
        }

        return false;
    });

    timatables_datalist_options = filtered_timetables;

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
        option.value = timetable.course_acronym;
        option.textContent = timetable.course_name + " | " + timetable.classs;
        timetable_datalist_options.appendChild(option);
    }
}

function block_filter() {
    var block_value = $("#block-filter").val();
    var block_id = user_blocks_obj.find(block => block.acronym === block_value)?.id;

    $("#area-filter").val("");
    $("#course-filter").val("");

    area_options();
    timetables_options();
    $("#info-alert").hide();
    

    if (block_value == "") {
    } else {
        var filtered_areas = user_areas_obj.filter(function (element) {
            return element.blocks.includes(block_id);
        });

        var area_datalist_options = document.getElementById("area-options");
        area_datalist_options.innerHTML = "";

        for (var i = 0; i < filtered_areas.length; i++) {
            var area = filtered_areas[i];

            var option = document.createElement("option");
            option.value = area.acronym;
            option.textContent = area.acronym + " | " + area.name_area;
            area_datalist_options.appendChild(option);
        }

        var filtered_timetables = timatables_datalist_options.filter(function (timetable) {
            return user_courses_obj.some(function (course) {
                return course.block === block_id && course.id === timetable.course_id;
            });
        });

        var course_datalist_options = document.getElementById("course-options");
        course_datalist_options.innerHTML = "";

        for (var i = 0; i < filtered_timetables.length; i++) {
            $("#course-filter").prop("disabled", false);
            var timetable = filtered_timetables[i];
            var option = document.createElement("option");
            option.value = timetable.acronym;
            option.textContent = timetable.course_name + " | " + timetable.classs;
            course_datalist_options.appendChild(option);
        }

        if (filtered_timetables.length == 0) {
            $("#course-filter").val("Nenhuma disciplina disponível neste horário.");
            $("#course-filter").prop("disabled", true);
        }
    }
}
function area_filter() {
    var area_value = $("#area-filter").val();
    var block_value = $("#block-filter").val();

    var area_id = user_areas_obj.find(area => area.acronym === area_value)?.id;
    var block_id = user_blocks_obj.find(block => block.acronym === block_value)?.id;
    $("#course-filter").val("");

    block_options();
    timetables_options();
    $("#info-alert").hide();

    if (area_value == "") {
    } else {
        if (block_value == "") {
            var filtered_timetables = timatables_datalist_options.filter(function (timetable) {
                return user_courses_obj.some(function (course) {
                    return course.area === area_id && course.id === timetable.course_id;
                });
            });

            var course_datalist_options = document.getElementById("course-options");
            course_datalist_options.innerHTML = "";

            for (var i = 0; i < filtered_timetables.length; i++) {
                $("#course-filter").prop("disabled", false);
                var timetable = filtered_timetables[i];
                var option = document.createElement("option");
                option.value = timetable.course_name;
                option.textContent = timetable.course_name + " | " + timetable.classs;
                course_datalist_options.appendChild(option);
            }

            if (filtered_timetables.length == 0) {
                $("#course-filter").val("Nenhuma disciplina disponível neste horário.");
                $("#course-filter").prop("disabled", true);
            }

            var block_datalist_options = document.getElementById("block-options");
            block_datalist_options.innerHTML = "";

            for (var i = 0; i < user_blocks_obj.length; i++) {
                var block = user_blocks_obj[i];
                var option = document.createElement("option");
                option.value = block.name_block;
                option.textContent = block.acronym + " | " + block.name_block;
                block_datalist_options.appendChild(option);
            }
        } else {
            var filtered_timetables = timatables_datalist_options.filter(function (timetable) {
                return user_courses_obj.some(function (course) {
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
                option.textContent = timetable.course_name + " | " + timetable.classs;
                course_datalist_options.appendChild(option);
            }

            if (filtered_timetables.length == 0) {
                $("#course-filter").val("Nenhuma disciplina disponível neste horário.");
                $("#course-filter").prop("disabled", true);
            }
        }
    }
}

function course_apresentation() {
    
    var course_value = $("#course-filter").val();
    var course_id = timatables_datalist_options.find(timetable => timetable.course_acronym === course_value)?.id;
    $("#info-alert").hide();
  
    var filtered_timetable = timatables_datalist_options.filter(function(timetable) {
      return timetable.id == course_id;
    });

    var discipline_name;
    var classs;
    var day;
    var timeslot_begin_hour;
    var timeslot_end_hour;

    filtered_timetable.forEach(function(timetable) {
        discipline_name = timetable.course_name
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
        });
    });

    $(".info-displine").text(discipline_name);
    $(".info-day").text(day);
    $(".info-start-and-end-hour").text(timeslot_begin_hour + " até " + timeslot_end_hour);
    $(".info-class").text(classs);
  
    $("#info-alert").show();
    if (isNaN(course_id) || course_value == '') {
        $("#info-alert").hide();
      }
  }

// Mapea na grade


$(document).ready(function () {
    $("#add-course-button").on("click", function () {
        var timetable_acronym = $("#course-filter").val();
        var timetable_id = timatables_datalist_options.find(timetable => timetable.course_acronym === timetable_acronym)?.id;
        var grade_position = $("#cel-position").text(); //mon-mor-1 mon-mor-2 mon-mor-3

        var filtered_timetable = user_timetables_obj.filter(function (timetable_item) {
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

                    
                    function format_id(id) {
                        var split_parts = id.split("-");
                        var class_number = split_parts[2];
                        var day_of_week = get_all_day(split_parts[0]);
                        var period = split_parts[1] === "mat" ? "Matutino" : split_parts[1] === "ves" ? "Vespertino" : "Noturno";
                    
                        return class_number + "º disciplina " + day_of_week + ", " + period;
                    }

                    for (var i = 0; i < day_combo_data.length; i++) {
                        var day_combo = day_combo_data[i];
                        var day = day_combo.day;
                        var timeslots = day_combo.timeslots;

                        timeslots.forEach(function(timeslot) {
                            var timeslot_begin_hour = timeslot.timeslot_begin_hour;
                        
                            var filtered_disponibility = user_disponibility_obj.filter(function(disponibility) {
                              return disponibility.day === get_full_day_of_week(day) && disponibility.timeslot_begin_hour === timeslot_begin_hour;
                            });
                        
                            var ids = filtered_disponibility.map(function(disponibility) {
                              return disponibility.id;
                            });

                            ids.forEach(function(id) {
                                length_ids ++;
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
                        $("#error-message-form").text("Você atingiu o máximo de células.");
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

                            var filtered_disponibility = user_disponibility_obj.filter(function (disponibility) {
                                return disponibility.day === get_full_day_of_week(day) && disponibility.timeslot_begin_hour === timeslot_begin_hour;
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
                        timetable_choosed.push(global);
                        cell_left_number.time -= id_array.length
                        $('#cel-hour').text(cell_left_number.time)
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
                        $("#warning-alert-message").text("Erro: As seguintes disciplinas já estão adicionadas:");
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
  
                          $("#warning-list-message").empty();
                          $("#warning-list-message").html("<ul>" + lists_courses + "</ul>");
                          $("#warning-alert-message").text("Erro: os seguintes cursos não estão de acordo com a disponibilidade:");
                          $("#warning-alert").show();
                          window.scrollTo({
                            top: $("#warning-alert").offset().top - $(".navbar").outerHeight() - 30,
                            behavior: "smooth",
                        });
                    }
                    $("#info-alert").hide();
                    
                },
                error: function (xhr, textStatus, errorThrown) {
                    $("#error-message").text("Erro ao tentar adicionar uma disciplina.");
                    $("#error-alert").show();
                },
            });
        } else {
            $("#error-message").text("Selecione uma disciplina.");
            $("#error-alert").show();
        }
    });

    $("#send-courses").on("click", function () {
        let csrftoken = get_cookie("csrftoken");
        var json_data = JSON.stringify(timetable_choosed);

        if (timetable_choosed.length != 0) {
            if(cell_left_number.type == '20h') {
                if(cell_left_number.time <= 13) {
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
                            $("#error-message-form").text("Erro ao tentar suas preferências de disciplinas.");
                            $("#error-alert-form").show();
                            window.scrollTo({
                                top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                                behavior: "smooth",
                            });
                        },
                    });
                } else {
                    $("#error-message-form").text("Quantidade de células minímas para seu FPA segundo seu regim é 8 células.");
                    $("#error-alert-form").show();
                    window.scrollTo({
                        top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                        behavior: "smooth",
                    });
                }
            } else {
                if(cell_left_number.time <= 9) {
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
                            $("#error-message-form").text("Erro ao tentar suas preferências de disciplinas.");
                            $("#error-alert-form").show();
                            window.scrollTo({
                                top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                                behavior: "smooth",
                            });
                        },
                    });
                } else {
                    $("#error-message-form").text("Quantidade de células minímas para seu FPA segundo seu regim é 12 células.");
                    $("#error-alert-form").show();
                    window.scrollTo({
                        top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                        behavior: "smooth",
                    });
                }
            }
        } else {
            $("#error-message-form").text("Selecione suas disciplinas.");
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
    const days = {
      mon: "Segunda-feira",
      tue: "Terça-feira",
      wed: "Quarta-feira",
      thu: "Quinta-feira",
      fri: "Sexta-feira",
      sat: "Sábado",
    };
  
    return days[abreviation_day] || "Nenhum day correspondente";
}

function info_button(value) {
    var infoMessage = $("#info-input-message").text();

    $("#info-input-message").empty();
    if (value === 'block') {
        var word_to_search = 'Bloco';
        $("#info-input-message").text("O filtro de Bloco serve para filtrar todas as disciplinas disponíveis apenas aquelas com o mesmo bloco pedido. Exemplo: Técnico - Aulas do técnico apenas.");
    } else if (value === 'area') {
        var word_to_search = 'Área';
        $("#info-input-message").text("O filtro de Área serve para filtrar todas as disciplinas disponíveis apenas aquelas com a mesma área pedida. Exemplo: ADS - Aulas de análise e desenvolvimento de sistemas apenas.");
    }

    if ($("#info-input-alert").css("display") === "block" && infoMessage.indexOf(word_to_search) !== -1) {
        $("#info-input-alert").hide();
    } else {
        $("#info-input-alert").show();
    }
}

