$("document").ready(function () {

    $('#year').mask('0000');

    $("#error-message-form").hide();
    $("#submit-button").click(function (event) {
        event.preventDefault(); // Impede o envio padrão do formulário
        $("#error-message-form").hide();

        let semester = $("#semester").val();
        let startFPA = $("#startFPADeadline").val();
        let endFPA = $("#endFPADeadline").val();
        let startAssignment = $("#startAssignmentDeadline").val();
        let endAssignment = $("#endAssignmentDeadline").val();

        if (semester <= 0 || semester > 2) {
            error_message("O semestre deve ser 1 ou 2");
        } else
        if (startFPA == "" || endFPA == "" || startAssignment == "" || endAssignment == "" || $("#year").val() == "" || $("#semester").val() == "") {
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
    $("#error-message-form").text(message);
    $("#error-message-form").show();
    window.scrollTo({
        top: $("#error-message-form").offset().top,
        behavior: "smooth",
    });
}
