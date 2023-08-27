$("document").ready(function () {
    $("#error-messages-form").hide();
    $("#submit-button").click(function (event) {
        event.preventDefault(); // Impede o envio padrão do formulário
        $("#error-messages-form").hide();
        
        let startFPA = $("#startFPADeadline").val();
        let endFPA = $("#endFPADeadline").val();
        let startAssignment = $("#startAssignmentDeadline").val();
        let endAssignment = $("#endAssignmentDeadline").val();

        if (startFPA == "" || endFPA == "" || startAssignment == "" || endAssignment == "") {
            error_message("Todos os campos devem ser preenchidos.");
        } else if (startFPA >= endFPA) {
            error_message("O início da submissão de FPA não pode ocorrer após o término de seu prazo.");
        } else if (startAssignment >= endAssignment) {
            error_message("O início das atribuições não pode ocorrer após o término de seu prazo.");
        } else if (startFPA >= startAssignment) {
            error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
        } else if (endFPA >= endAssignment) {
            error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
        } else {
            // Se não houver erros, você pode permitir o envio do formulário
            $("#form").submit();
        }
    });
});

function error_message(message) {
    $("#error-messages-form").text(message);
    $("#error-messages-form").show();
    window.scrollTo({
        top: $("#error-messages-form").offset().top,
        behavior: "smooth",
    });
}
