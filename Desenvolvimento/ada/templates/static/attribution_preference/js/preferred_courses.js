var lang = document.currentScript.getAttribute("data-lang");
var disponibility = document.currentScript.getAttribute("disponibility");
var timetables = document.currentScript.getAttribute("timetables");
var courses = document.currentScript.getAttribute("courses");
var blocks = document.currentScript.getAttribute("blocks");
var areas = document.currentScript.getAttribute("areas");

var timetable_global = [];
var btn_checked_global = [];

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
        hour: horaString, // 7:45:00
    };

    disponibility_array_obj.push(novo_objeto);
}

var timetables_array_obj = [];

for (var i = 0; i < timetables_array.length; i++) {
    var timetable_object = timetables_array[i];
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
                hour_start: timeslot.hour_start,
                hour_end: timeslot.hour_end,
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
        acronym: acronym,
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
        blocks: blocks,
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
        block: block,
    };

    courses_array_obj.push(novo_objeto);
}

$("#timetable-courses input").on("click", function () {
    console.log(btn_checked_global)
    var dataId = $(this).closest("div[data-id]").data("id");
    $("#cel-position").text(dataId).css("visibility", "hidden");

    $("#area-filter").val("");
    $("#block-filter").val("");
    $("#course-filter").val("");

    area_options();
    block_options();
    timetables_options();

    var updated_array = btn_checked_global.some(function (dict) {
        return dict.includes(dataId);
    });
    if (updated_array) {
        var filteredTimetables = timetable_global.filter(function (t) {
            return t.position.includes(dataId);
        });

        filteredTimetables.forEach(function (timetable) {
            timetable.position.forEach(function (position) {
                $("#sub-" + position).text("+");
                $("#btn-" + position)
                    .attr("data-toggle", "modal")
                    .attr("data-target", "#addCourseModal");
            });
        });

        btn_checked_global = btn_checked_global.filter(function (element) {
            return !filteredTimetables.some(function (timetable) {
              return timetable.position.includes(element);
            });
          });

        timetable_global = timetable_global.filter(function (t) {
            return !filteredTimetables.includes(t);
        });
    }
    console.log("RERTOUE")
        console.log(timetable_global)
        console.log(btn_checked_global)
});

function area_options() {
    var areaOptionsDatalist = document.getElementById("area-options");
    areaOptionsDatalist.innerHTML = "";

    for (var i = 0; i < areas_array_obj.length; i++) {
        var area = areas_array_obj[i];
        var option = document.createElement("option");
        option.value = area.id;
        option.textContent = "Área: " + area.acronym + " | " + area.name_area;
        areaOptionsDatalist.appendChild(option);
    }
}

function block_options() {
    var blockOptionsDatalist = document.getElementById("block-options");
    blockOptionsDatalist.innerHTML = "";

    for (var i = 0; i < blocks_array_obj.length; i++) {
        var block = blocks_array_obj[i];
        var option = document.createElement("option");
        option.value = block.id;
        option.textContent = "Bloco: " + block.acronym + " | " + block.name_block;
        blockOptionsDatalist.appendChild(option);
    }
}

function timetables_options() {
    var spanValue = $("#cel-position").text();

    var filteredElement = disponibility_array_obj.find(function (element) {
        return element.frase === spanValue;
    });

    var filteredTimetables = timetables_array_obj.filter(function (timetable) {
        var dayCombos = timetable.day_combo;

        for (var i = 0; i < dayCombos.length; i++) {
            var dayCombo = dayCombos[i];
            var timeslotDay = dayCombo.day.substring(0, 3);
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
    var timetableOptionsDatalist = document.getElementById("course-options");
    timetableOptionsDatalist.innerHTML = "";

    if (filteredTimetables.length == 0) {
        $("#course-filter").val("Nenhuma aula disponível neste horário.");
        $("#course-filter").prop("disabled", true);
    }

    for (var i = 0; i < filteredTimetables.length; i++) {
        $("#course-filter").prop("disabled", false);
        var timetable = filteredTimetables[i];
        var option = document.createElement("option");
        option.value = timetable.id;
        option.textContent = "Curso: " + timetable.course_name + " | " + timetable.classs;
        timetableOptionsDatalist.appendChild(option);
    }
}

function block_filter() {
    var block_value = $("#block-filter").val();
    $("#area-filter").val("");
    $("#course-filter").val("");

    area_options();
    timetables_options();

    if (block_value == "") {
    } else {
        var filtered_areas = areas_array_obj.filter(function (element) {
            return element.blocks.includes(block_value);
        });

        var areaOptionsDatalist = document.getElementById("area-options");
        areaOptionsDatalist.innerHTML = "";

        for (var i = 0; i < filtered_areas.length; i++) {
            var area = filtered_areas[i];

            var option = document.createElement("option");
            option.value = area.id;
            option.textContent = "Área: " + area.acronym + " | " + area.name_area;
            areaOptionsDatalist.appendChild(option);
        }

        var filtered_timetables = timetables_array_obj.filter(function (timetable) {
            return courses_array_obj.some(function (course) {
                return course.block === block_value && course.id === timetable.course_id;
            });
        });

        var courseOptionsDatalist = document.getElementById("course-options");
        courseOptionsDatalist.innerHTML = "";

        for (var i = 0; i < filtered_timetables.length; i++) {
            $("#course-filter").prop("disabled", false);
            var timetable = filtered_timetables[i];
            var option = document.createElement("option");
            option.value = timetable.id;
            option.textContent = "Curso: " + timetable.course_name + " | " + timetable.classs;
            courseOptionsDatalist.appendChild(option);
        }

        if (filtered_timetables.length == 0) {
            $("#course-filter").val("Nenhuma aula disponível neste horário.");
            $("#course-filter").prop("disabled", true);
        }
    }
}
function area_filter() {
    var area_value = $("#area-filter").val();
    var block_value = $("#block-filter").val();
    $("#course-filter").val("");

    block_options();
    timetables_options();

    if (area_value == "") {
    } else {
        if (block_value == "") {
            var filtered_timetables = timetables_array_obj.filter(function (timetable) {
                return courses_array_obj.some(function (course) {
                    return course.area === area_value && course.id === timetable.course_id;
                });
            });

            var courseOptionsDatalist = document.getElementById("course-options");
            courseOptionsDatalist.innerHTML = "";

            for (var i = 0; i < filtered_timetables.length; i++) {
                $("#course-filter").prop("disabled", false);
                var timetable = filtered_timetables[i];
                var option = document.createElement("option");
                option.value = timetable.id;
                option.textContent = "Curso: " + timetable.course_name + " | " + timetable.classs;
                courseOptionsDatalist.appendChild(option);
            }

            if (filtered_timetables.length == 0) {
                $("#course-filter").val("Nenhuma aula disponível neste horário.");
                $("#course-filter").prop("disabled", true);
            }
        } else {
            var filtered_timetables = timetables_array_obj.filter(function (timetable) {
                return courses_array_obj.some(function (course) {
                    return course.block === block_value && course.area === area_value && course.id === timetable.course_id;
                });
            });

            var courseOptionsDatalist = document.getElementById("course-options");
            courseOptionsDatalist.innerHTML = "";

            for (var i = 0; i < filtered_timetables.length; i++) {
                $("#course-filter").prop("disabled", false);
                var timetable = filtered_timetables[i];
                var option = document.createElement("option");
                option.value = timetable.id;
                option.textContent = "Curso: " + timetable.course_name + " | " + timetable.classs;
                courseOptionsDatalist.appendChild(option);
            }

            if (filtered_timetables.length == 0) {
                $("#course-filter").val("Nenhuma aula disponível neste horário.");
                $("#course-filter").prop("disabled", true);
            }
        }
    }
}

// Mapea na grade
for (var i = 0; i < disponibility_array_obj.length; i++) {
    var obj = disponibility_array_obj[i];
    var fraseId = obj.frase;
    $("label[for='" + fraseId + "']")
        .removeClass("disabled")
        .removeClass("btn-notchecked");
    $("label[for='" + fraseId + "']").css({
        "font-weight": "700",
        color: "white",
        "background-color": "#2f7363",
    });
    $("#" + fraseId).prop("disabled", false);
    $("#sub-" + fraseId).text("+");
    $("#btn-" + fraseId)
        .attr("data-toggle", "modal")
        .attr("data-target", "#addCourseModal");
}

$(document).ready(function () {
    $("#addCourseButton").on("click", function () {
        var timetable_id = parseInt($("#course-filter").val());
        var grade_position = $("#cel-position").text(); //mon-mat-1 mon-mat-2 mon-mat-3
        alert(grade_position)

        var filtered_timetable = timetables_array_obj.filter(function (timetable_item) {
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
                    var is_repetead = "False";
                    var frase_array = [];           
                    var frases_repetidas = [];

                    
                    function formatarFrase(frase) {
                        var partes = frase.split("-");
                        var numeroAula = partes[2];
                        var diaSemana = getDiaCompleto(partes[0]);
                        var periodo = partes[1] === "mat" ? "Matutino" : partes[1] === "ves" ? "Vespertino" : "Noturno";
                    
                        return numeroAula + "° aula " + diaSemana + ", " + periodo;
                    }

                    for (var i = 0; i < day_combo_data.length; i++) {
                        var day_combo = day_combo_data[i];
                        var day = day_combo.day;
                        var timeslots = day_combo.timeslots;

                        timeslots.forEach(function (timeslot) {
                            var hour_start = timeslot.hour_start;

                            // Filtra o disponibility_array_obj pelo mesmo dia e hour_start
                            var filtered_disponibility = disponibility_array_obj.filter(function (disponibility) {
                                return disponibility.dia === getFullDayOfWeek(day) && disponibility.hour === hour_start;
                            });

                            var frases = filtered_disponibility.map(function (disponibility) {
                                return disponibility.frase;
                            });

                            frases.forEach(function (frase) {
                                if (is_repetead == "True") {
                                } else {
                                    if (btn_checked_global.includes(frase)) {
                                        is_repetead = "True";
                                        frases_repetidas.push(formatarFrase(frase));
                                    } else {
                                        // A frase não está presente em btn_checked_global
                                        // Execute as ações desejadas aqui
                                        $("#sub-" + frase).text(filtered_timetable[0].course_acronym);
                                        frase_array.push(frase);
                                        $("#btn-" + frase)
                                            .attr("data-toggle", "none")
                                            .attr("data-target", "#");
                                        btn_checked_global.push(frase);
                                    }
                                }
                            });
                        });
                    }
                    $("#modal-" + grade_position)
                        .attr("data-toggle", "none")
                        .attr("data-target", "#");

                    global = {
                        id_timetable: filtered_timetable[0].id,
                        position: frase_array,
                    };
                    if (is_repetead == "False") {
                        timetable_global.push(global);
                    } 
                    

                    $("#course-filter").val("");
                    $("#error-alert").hide();
                    if (frases_repetidas.length > 0) {
                        var lista_repetidas = frases_repetidas.map(function(frase) {
                          return "<li>" + frase + "</li>";
                        }).join("");
                      
                        $("#warning-list-message").html("<ul>" + lista_repetidas + "</ul>");
                        $("#warning-alert-message").text("Erro: As seguintes aulas já estão adicionadas:");
                        $("#warning-alert").show();
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $("#error-message").text("Erro ao tentar adicionar uma aula.");
                    $("#error-alert").show();
                },
            });
        } else {
            $("#error-message").text("Selecione uma aula.");
            $("#error-alert").show();
        }
    });

    $("#sendCourses").on("click", function () {
        let csrftoken = getCookie("csrftoken");
        var jsonData = JSON.stringify(timetable_global);
        alert(jsonData);
        console.log(timetable_global);

        if (timetable_global.length != 0) {
            $.ajax({
                type: "post",
                url: "/" + lang + "/professor/preferencia-atribuicao/salvar-fpa/",
                data: {
                    timetable: jsonData,
                },
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                success: function (response) {
                    $("#course-filter-form").val("");
                    $("#error-alert-form").hide();
                    window.location.href = "/" + lang + "/professor/preferencia-atribuicao/salvar-fpa/";
                },
                error: function (xhr, textStatus, errorThrown) {
                    $("#error-message-form").text("Erro ao tentar suas preferências de cursos.");
                    $("#error-alert-form").show();
                    window.scrollTo({
                        top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                        behavior: "smooth",
                    });
                },
            });
        } else {
            $("#error-message-form").text("Selecione suas aulas.");
            $("#error-alert-form").show();
            window.scrollTo({
                top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
                behavior: "smooth",
            });
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

function getFullDayOfWeek(short_day) {
    const dayMappings = {
        monday: "mon",
        tuesday: "tue",
        wednesday: "wed",
        thursday: "thu",
        friday: "fri",
        saturday: "sat",
    };

    return dayMappings[short_day] || "Nenhum dia correspondente";
}

function getDiaCompleto(abreviacao_dia) {
    const dias = {
      mon: "Segunda-feira",
      tue: "Terça-feira",
      wed: "Quarta-feira",
      thu: "Quinta-feira",
      fri: "Sexta-feira",
      sat: "Sábado",
    };
  
    return dias[abreviacao_dia] || "Nenhum dia correspondente";
  }
