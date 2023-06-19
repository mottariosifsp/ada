var timeslots = []
var lang = document.currentScript.getAttribute('data-lang');
var cel_left = 0
var type_cel = 0
var cel_final = "not_checked"
var hour = 0
var minute = 0
var user_blocks = document.currentScript.getAttribute('blocks');
var user_timetables = document.currentScript.getAttribute('timetables');
var max_quantidade_celulas = document.currentScript.getAttribute('max_quantidade_celulas');
var timeslot_minutes = document.currentScript.getAttribute('diferenca_minutos');
var controlEightHours = false;
var checkboxes = [
    [], [], [], [], [], []
];

$(document).ready(function () {

    // Mudar horas restantes
    $('input[name="regime"]').click(function () {
        $('#cel-regime').val('');
        var valor = $(this).val();
        if (valor == 'rde' || valor == '40') {
            var this_duracao = 24 * 60 / timeslot_minutes;
            $('#cel-regime').text(this_duracao);
            cel_left = this_duracao
            type_cel = 40;
            cel_final = "not_checked"
            $('.checkbox input[type="checkbox"]').prop('checked', false);
            $('label.checkbox').removeClass('active');
            timeslots = []
        } else {
            var this_duracao = 12 * 60 / timeslot_minutes;
            $('#cel-regime').text(this_duracao);
            cel_left = this_duracao
            type_cel = 20;
            cel_final = "not_checked"
            $('.checkbox input[type="checkbox"]').prop('checked', false);
            $('label.checkbox').removeClass('active');
            timeslots = []
            //console.log(timeslots)
        }

        if ($('#error-alert-form').is(':visible')) {
            $('#error-alert-form').hide();
            $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').add('label[for^="sat-"]').removeClass('disabled').removeAttr('aria-disabled');
            $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').add('input[type="checkbox"][id^="sat-"]').prop('disabled', false);
        }
    });

    // Limpar formulário inteiro
    $('#cleanFPA').click(function () {
        $('input[name="regime"]').prop('checked', false);
        $('.checkbox input[type="checkbox"]').prop('checked', false);
        $('label.checkbox').removeClass('active');
        $('#cel-regime').text("--");
        $('#error-alert-form').hide();

        window.scrollTo({
            top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
            behavior: 'smooth'
        });

        timeslots.length = 0;
        cel_left = 0;
    });

    // Pegar dados dos checkboxes
    $('.checkbox').click(function () {

        //   checkboxes[0].sort(function(a, b) {
        //   var idA = parseInt(a.id.split('-').pop()); // Obtém o último elemento do ID de a e converte para número
        //   var idB = parseInt(b.id.split('-').pop()); // Obtém o último elemento do ID de b e converte para número
        //
        //   var typeA = a.id.split('-')[1]; // Obtém a parte do tipo de a (mat, vesp, not)
        //   var typeB = b.id.split('-')[1]; // Obtém a parte do tipo de b (mat, vesp, not)
        //
        //   // Define a ordem de prioridade dos tipos (mat > vesp > not)
        //   var order = { 'mat': 0, 'ves': 1, 'not': 2 };
        //
        //   // Realiza a comparação dos tipos
        //   if (order[typeA] < order[typeB]) {
        //     return -1;
        //   } else if (order[typeA] > order[typeB]) {
        //     return 1;
        //   }
        //
        //   // Realiza a comparação dos IDs numéricos
        //   if (idA < idB) {
        //     return -1;
        //   } else if (idA > idB) {
        //     return 1;
        //   } else {
        //     return 0;
        //   }
        // });
        //
        // checkboxes[1].sort(function(a, b) {
        //   var idA = parseInt(a.id.split('-').pop()); // Obtém o último elemento do ID de a e converte para número
        //   var idB = parseInt(b.id.split('-').pop()); // Obtém o último elemento do ID de b e converte para número
        //
        //   var typeA = a.id.split('-')[1]; // Obtém a parte do tipo de a (mat, vesp, not)
        //   var typeB = b.id.split('-')[1]; // Obtém a parte do tipo de b (mat, vesp, not)
        //
        //   // Define a ordem de prioridade dos tipos (mat > vesp > not)
        //   var order = { 'mat': 0, 'ves': 1, 'not': 2 };
        //
        //   // Realiza a comparação dos tipos
        //   if (order[typeA] < order[typeB]) {
        //     return -1;
        //   } else if (order[typeA] > order[typeB]) {
        //     return 1;
        //   }
        //
        //   // Realiza a comparação dos IDs numéricos
        //   if (idA < idB) {
        //     return -1;
        //   } else if (idA > idB) {
        //     return 1;
        //   } else {
        //     return 0;
        //   }
        // });
        //
        //   // Imprime os inputs ordenados
        //   for (var i = 0; i < checkboxes[1].length; i++) {
        //     console.log(checkboxes[1][i].id);
        //   }
        //   console.log(checkboxes);
        //
        //   var checkboxValor1 = checkboxes[0][checkboxes[0].length - 1].value;
        //   var ultimoHorario = checkboxValor1.split(',')[0].split('-').pop().trim();
        //   console.log(checkboxValor1);
        //   console.log("ultimo horario", ultimoHorario);
        //
        //   var ultimoHorario1 = moment(ultimoHorario, 'HH:mm');
        //   var ultimoHorarioMinutos = ultimoHorario1.hours() * 60 + ultimoHorario1.minutes();
        //   console.log("ultimo horario minutos", ultimoHorarioMinutos);
        //
        //   var checkboxValor2 = checkboxes[1][0].value;
        //   var primeiroHorario = checkboxValor2.split(',')[0].split('-').shift().trim();
        //   console.log("primeiro horario", primeiroHorario);
        //
        //   var primeiroHorario1 = moment(primeiroHorario, 'HH:mm');
        //   var primeiroHorarioMinutos = primeiroHorario1.hours() * 60 + primeiroHorario1.minutes();
        //   console.log("primeiro horario minutos", primeiroHorarioMinutos);


        if (cel_left == 0 && type_cel == 0) {
            $('#cel-regime').text("--");
            $('label[for^="mon-"]').add('label[for^="tue-"]').add('label[for^="wed-"]').add('label[for^="thu-"]').add('label[for^="fri-"]').add('label[for^="sat-"]').addClass('disabled').attr('aria-disabled', 'true');
            $('input[type="checkbox"][id^="mon-"]').add('input[type="checkbox"][id^="tue-"]').add('input[type="checkbox"][id^="wed-"]').add('input[type="checkbox"][id^="thu-"]').add('input[type="checkbox"][id^="fri-"]').add('input[type="checkbox"][id^="sat-"]').prop('disabled', true);

            $('#error-message-form').text('Insira o regime de trabalho antes de continuar.');
            $('#error-alert-form').show();
            window.scrollTo({
                top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
                behavior: 'smooth'
            });
        } else {
            var input_id = $(this).attr('for');
            var input_val = $('#' + input_id).val();
            var is_checked = $('#' + input_id).prop('checked');
            var checkbox = document.getElementById(input_id);
            console.log("isChechked", is_checked);
            var checkboxExists = false;
            var positionDelete = -1;

            for (var j = 0; j < checkboxes.length; j++) {
                for (var i = 0; i < checkboxes[j].length; i++) {
                    if (checkboxes[j][i].id === checkbox.id) {
                        checkboxExists = true;
                        positionDelete = i;
                        break;
                    }
                }
            }

            if (is_checked) {
                cel_left += 1;
                var [objeto_elemento, dia_elemento] = input_val.split(',');
                var [inicio, fim] = objeto_elemento.split('-');

                if (cel_final == "checked") {
                    $('input[type="checkbox"][id^="mon-"], input[type="checkbox"][id^="tue-"], input[type="checkbox"][id^="wed-"], input[type="checkbox"][id^="thu-"], input[type="checkbox"][id^="fri-"], input[type="checkbox"][id^="sat-"]').each(function () {
                        if (!$(this).prop('checked')) {
                            $(this).prop('disabled', false);
                            $('label[for="' + $(this).attr('id') + '"]').removeClass('disabled').removeAttr('aria-disabled');
                        }
                    });
                    cel_final = "not_checked"
                    cel_left += 1

                    $('#error-alert-form').hide();
                }

                var index = timeslots.findIndex(function (aula) {
                    return aula.hora_comeco === inicio;
                });

                if (index !== -1) {
                    timeslots.splice(index, 1);
                    //console.log(timeslots);
                }

                $('#cel-regime').text(cel_left);


                // Se o checkbox existir, ele é deletado, pois foi desmarcado
                if (checkboxExists) {
                    deleteCheckbox(checkboxes, input_id, positionDelete);


                    console.log("desmarcado");
                    console.log("mon", checkboxes[0].length);
                    console.log("tue", checkboxes[1].length);
                    console.log("wed", checkboxes[2].length);
                    console.log("thu", checkboxes[3].length);
                    console.log("fri", checkboxes[4].length);
                    console.log("sat", checkboxes[5].length);
                }

            } else {
                if (cel_final != "checked") {
                    var controle = 0;

                    if (controle !== 1 && (cel_left - 1) != -1 && !(controlEightHours == true)) {
                        // Adicionar o checkbox apenas se não existir no array
                        if (!checkboxExists) {
                            if (checkbox.id.startsWith("mon")) {
                                checkboxes[0].push(checkbox);
                            } else if (checkbox.id.startsWith("tue")) {
                                checkboxes[1].push(checkbox);
                            } else if (checkbox.id.startsWith("wed")) {
                                checkboxes[2].push(checkbox);
                            } else if (checkbox.id.startsWith("thu")) {
                                checkboxes[3].push(checkbox);
                            } else if (checkbox.id.startsWith("fri")) {
                                checkboxes[4].push(checkbox);
                            } else if (checkbox.id.startsWith("sat")) {
                                checkboxes[5].push(checkbox);
                            }
                        }
                    }

                    for (var i = 0; i < checkboxes.length; i++) {
                        if (checkboxes[i].length > max_quantidade_celulas) {
                            //deleteCheckbox(checkboxes, input_id, positionDelete);
                            controlEightHours = true;
                            controle = 1;
                            $('#error-message-form').text('A seleção da disponibilidade de horário não pode ultrapassar 8 horas de trabalho diárias.');
                            $('#error-alert-form').show();
                            window.scrollTo({
                                top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
                                behavior: 'smooth'
                            });
                            break;
                        } else {
                            controlEightHours = false;
                        }
                    }

                    console.log("mon", checkboxes[0].length);
                    console.log("tue", checkboxes[1].length);
                    console.log("wed", checkboxes[2].length);
                    console.log("thu", checkboxes[3].length);
                    console.log("fri", checkboxes[4].length);
                    console.log("sat", checkboxes[5].length);
                    
                    if (!controlEightHours) {
                        atualizar_cel_left(is_checked);
                    }

                    if (cel_final != "checked") {
                        var [objeto_elemento, dia_elemento] = input_val.split(',');
                        var [inicio, fim] = objeto_elemento.split('-');
                        var aula = {
                            hora_comeco: inicio,
                            hora_fim: fim,
                            dia_semana: dia_elemento
                        };
                        timeslots.push(aula);

                    }
                }
            }
        }
    });

    // Area e disponibilidade

    // $('#campoInputBlock').on('input', function() {
    //   var valor_selecionado = $(this).val();
    //   $('.block').each(function() {
    //     var block = $(this).attr('id').replace('block-', '');
    //     $(this).hide();

    //     var opcoes = $('#opcoes option').map(function() {
    //       return $(this).val();
    //     }).get();

    //     for (var i = 0; i < opcoes.length; i++) {
    //       if (block === opcoes[i]) {
    //         $(this).hide();
    //         break;
    //       }
    //     }

    //     $('#block-none').hide();
    //   });

    //   if (valor_selecionado == '' || valor_selecionado == null || valor_selecionado.length < 3) {
    //     $('#block-none').show();
    //   }

    //   $('#block-' + valor_selecionado).show();
    // });

    // Enviar formulário inteiro
    $('#sendDisponibility').click(function () {
        var work_regime = $('input[name="regime"]:checked').val();
        var jsonData = JSON.stringify(timeslots);

        let csrftoken = getCookie('csrftoken');

        console.log("contro8horas", controlEightHours);
        console.log("check teste", checkboxes[0].length);
        if (work_regime && timeslots.length !== 0 &&
            checkboxes[0].length <= max_quantidade_celulas &&
            checkboxes[1].length <= max_quantidade_celulas &&
            checkboxes[2].length <= max_quantidade_celulas &&
            checkboxes[3].length <= max_quantidade_celulas &&
            checkboxes[4].length <= max_quantidade_celulas &&
            checkboxes[5].length <= max_quantidade_celulas) {
            console.log("contro8horasmm", controlEightHours);
            $.ajax({
                type: 'post',
                url: '/' + lang + '/professor/preferencia-atribuicao/criar-fpa/editar-cursos/',
                data: {
                    work_regime: work_regime,
                    work_timeslots: jsonData
                },
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (response) {
                    $('input[name="regime"]:checked').prop('checked', false);
                    $('#error-alert-form').hide();
                    window.location.href = '/' + lang + '/professor/preferencia-atribuicao/criar-fpa/editar-cursos/'
                },
                error: function (xhr, status, error) {
                    $('#error-message-form').text('Ocorreu um erro no envio de FPA.');
                    $('#error-alert-form').show();
                    window.scrollTo({
                        top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
                        behavior: 'smooth'
                    });
                }
            });
        } else {
            $('#error-message-form').text('Insira as informações pedidas em cada seção. Se certifique que a seleção de disponibilidade não ultrapassa 8 horas diárias de trabalho.');
            $('#error-alert-form').show();
            window.scrollTo({
                top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
                behavior: 'smooth'
            });
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

function atualizar_cel_left(is_checked) {
    if (!is_checked) {
        if (cel_final == "checked") {
            cel_left = 0;
            $('#cel-regime').text(cel_left);
        } else {
            cel_left -= 1;
            if (cel_left == -1) {
                $('input[type="checkbox"][id^="mon-"], input[type="checkbox"][id^="tue-"], input[type="checkbox"][id^="wed-"], input[type="checkbox"][id^="thu-"], input[type="checkbox"][id^="fri-"], input[type="checkbox"][id^="sat-"]').each(function () {
                    if (!$(this).prop('checked')) {
                        $(this).prop('disabled', true);
                        $('label[for="' + $(this).attr('id') + '"]').addClass('disabled').attr('aria-disabled', 'true');
                    }
                });
                $('#error-message-form').text('Você atingiu seu limite de disponibilidade.');
                $('#error-alert-form').show();
                window.scrollTo({
                    top: $('#error-alert-form').offset().top - $('.navbar').outerHeight() - 30,
                    behavior: 'smooth'
                });
                cel_final = "checked";
            } else {
                $('#cel-regime').text(cel_left);
            }
        }
    }
}

function deleteCheckbox(checkboxes, checkboxId, positionDelete) {
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxId.startsWith(getDayOfWeek(i))) {
            checkboxes[i].splice(positionDelete, 1);
            console.log("foi?");
            break;
        }
    }
}

function getDayOfWeek(index) {
    const daysOfWeek = ["mon", "tue", "wed", "thu", "fri", "sat"];
    return daysOfWeek[index];
}
