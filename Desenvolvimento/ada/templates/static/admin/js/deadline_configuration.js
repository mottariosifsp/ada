var lang = document.currentScript.getAttribute("data-lang");

$("document").ready(function () {

    $("#feature3").on("click", function () {
        if ($(this).is(":checked")) {
            $("#checkbox-text").html(
                "<svg xmlns='http://www.w3.org/2000/svg' id='overwrite' width='30' height='30' style='padding-top:9px;' fill='currentColor' class='bi bi-check2-circle' viewBox='0 0 16 16'>" +
                "<path d='M2.5 8a5.5 5.5 0 0 1 8.25-4.764.5.5 0 0 0 .5-.866A6.5 6.5 0 1 0 14.5 8a.5.5 0 0 0-1 0 5.5 5.5 0 1 1-11 0z'/>" +
                "<path d='M15.354 3.354a.5.5 0 0 0-.708-.708L8 9.293 5.354 6.646a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l7-7z'/>" +
                "</svg>"
            );
        } else {
            $("#checkbox-text").html(
                "<svg xmlns='http://www.w3.org/2000/svg' id='overwrite' width='30' height='30' style='padding-top:9px;' fill='currentColor' class='bi bi-circle' viewBox='0 0 16 16'>" +
                "<path d='M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z'/>" +
                "</svg>"
            );
        }
    });

    $(".feature3").hide();
    $("#error-message-form").hide();
    $("#submit-button").click(function (event) {
        event.preventDefault(); // Impede o envio padrão do formulário
        $("#error-message-form").hide();
        $(".feature3").hide();

        let year = $("#year").val()
        let semester = $("input[name=semester]").val();
        let startFPA = $("#startFPADeadline").val();
        let endFPA = $("#endFPADeadline").val();
        let startAssignment = $("#startAssignmentDeadline").val();
        let endAssignment = $("#endAssignmentDeadline").val();
        let overwrite = $("#feature3").is(":checked");
        if (semester <= 0 || semester > 2) {
            error_message("O semestre deve ser 1 ou 2");
        } else
        if (startFPA == "" || endFPA == "" || startAssignment == "" || endAssignment == "" || year == "" || semester == "") {
            error_message("Todos os campos devem ser preenchidos.");
        } else if (startFPA >= endFPA) {
            error_message("O início da submissão de FPA não pode ocorrer após o término de seu prazo.");
        } else if (startAssignment >= endAssignment) {
            error_message("O início das atribuições não pode ocorrer após o término de seu prazo.");
        } else if (startFPA >= startAssignment) {
            error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
        } else if (endFPA >= endAssignment) {
            error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
        } else{
            let data = {
                'semester': semester,
                'startFPADeadline': startFPA,
                'endFPADeadline': endFPA,
                'startAssignmentDeadline': startAssignment,
                'endAssignmentDeadline': endAssignment,
                'overwrite': overwrite,
                'year': year,
                'semester': semester
            };
            
            let csrftoken = getCookie('csrftoken');

            $.ajax({
                method: 'POST', url: '/admin/prazo/confirmacao/', 
                data: data, 
                headers: {
                    'X-CSRFToken': csrftoken
                }, success: function (response) {
                    $(this).prop('disabled', true);
                    window.location.href = response.redirect;
                    // console.log(response);
                    // $('#editProfessorModal').modal('hide');
                    // $(".alert-danger").hide();
                }, error: function (xhr, status, error) {
                    $("#error-message-form").show();
                    if (lang == 'pt-br' || lang == '') {
                        $(".feature3").hide();
                        if (xhr.responseJSON.error == "Já houve uma atribuição para esse semetre neste ano.") {
                            $(".feature3").show();
                            error_message(`
                            Uma atribuição já foi feita no ano ${year} no semestre ${semester}. Para criar uma nova atribuição, selecione
                             outra data ou marque a opção ao lado para excluir a atribuição anterior e criar uma nova.`)
                        }
                    }
                    //     $("#error-message-form").text("An error occurred.");
                    // }

                }
            });
        }

    });
});

function error_message(message) {
    $("#error-message-form").text(message);
    $("#error-message-form").show();
    window.scrollTo({
        top: $("#error-message-form").offset().top,
        behavior: "smooth",
    });
}

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
