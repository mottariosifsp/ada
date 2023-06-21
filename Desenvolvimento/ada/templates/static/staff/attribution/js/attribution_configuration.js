$("document").ready(function(){

    $("#submit-button").click(function(){
        $("#error-alert-form").hide();
        $("#form").off("submit");
        let startFPA = $("#startFPADeadline").val();
        let endFPA = $("#endFPADeadline").val();
        let startAssignment = $("#startAssignmentDeadline").val();
        let endAssignment = $("#endAssignmentDeadline").val();

        if (startFPA >= endFPA) {
            error_message("O início da submissão de FPA não pode ocorrer após o término de seu prazo.");
        }
        if (startAssignment >= endAssignment) {
            error_message("O início das atribuições não pode ocorrer após o término de seu prazo.")
        }
        if (startFPA >= startAssignment) {
            error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
        }
        if (endFPA >= endAssignment) {
            error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
        }
        if (startFPA == "" || endFPA == "" || startAssignment == "" || endAssignment == "") {
            error_message("Todos os campos devem ser preenchidos.");
        }
    });
});
function error_message(message) {
    $("#error-message-form").text(message);
    $("#error-alert-form").show();
    window.scrollTo({
        top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
        behavior: "smooth",
    });
    $("#form").on("submit", function(e){
        e.preventDefault();
    });
}
    