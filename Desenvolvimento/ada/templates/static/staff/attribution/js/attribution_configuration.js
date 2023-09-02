// $("document").ready(function () {

    // $("#submit-button").click(function () {
    //     $("#error-alert-form").hide();
    //     $("#form").off("submit");
    //     let startFPA = $("#startFPADeadline").val();
    //     let endFPA = $("#endFPADeadline").val();
    //     let startAssignment = $("#startAssignmentDeadline").val();
    //     let endAssignment = $("#endAssignmentDeadline").val();

    //     if (startFPA >= endFPA) {
    //         error_message("O início da submissão de FPA não pode ocorrer após o término de seu prazo.");
    //     }
    //     if (startAssignment >= endAssignment) {
    //         error_message("O início das atribuições não pode ocorrer após o término de seu prazo.")
    //     }
    //     if (startFPA >= startAssignment) {
    //         error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
    //     }
    //     if (endFPA >= endAssignment) {
    //         error_message("O prazo de submissão de FPA deve acabar antes do prazo de atribuições começar.");
    //     }
    //     if (startFPA == "" || endFPA == "" || startAssignment == "" || endAssignment == "") {
    //         error_message("Todos os campos devem ser preenchidos.");
    //     }
    // });

//      // Salvar os valores dos campos de entrada no localStorage ao sair da página
//      $("#edit-queue-button").click(function () {
//         // Salvar os valores dos campos "startFPADeadline" e "endFPADeadline" no localStorage
//         var startFPADeadlineValue = document.getElementById('startFPADeadline').value;
//         localStorage.setItem('startFPADeadline', startFPADeadlineValue);

//         var endFPADeadlineValue = document.getElementById('endFPADeadline').value;
//         localStorage.setItem('endFPADeadline', endFPADeadlineValue);

//         // Salvar os valores dos campos "startAssignmentDeadline" e "endAssignmentDeadline" no localStorage
//         var startAssignmentDeadlineValue = document.getElementById('startAssignmentDeadline').value;
//         localStorage.setItem('startAssignmentDeadline', startAssignmentDeadlineValue);

//         var endAssignmentDeadlineValue = document.getElementById('endAssignmentDeadline').value;
//         localStorage.setItem('endAssignmentDeadline', endAssignmentDeadlineValue);
//     });

//     $("#submit-button").click(function () {
//         localStorage.clear();
//     });
// });

// function error_message(message) {
//     $("#error-message-form").text(message);
//     $("#error-alert-form").show();
//     window.scrollTo({
//         top: $("#error-alert-form").offset().top - $(".navbar").outerHeight() - 30,
//         behavior: "smooth",
//     });
//     $("#form").on("submit", function (e) {
//         e.preventDefault();
//     });   
// }

// // Recuperar os valores dos campos de entrada do localStorage ao carregar a página
// window.addEventListener('load', function () {

//     // Recuperar os valores dos campos "startFPADeadline" e "endFPADeadline" do localStorage
//     var startFPADeadlineValue = localStorage.getItem('startFPADeadline');
//     if (startFPADeadlineValue) {
//         document.getElementById('startFPADeadline').value = startFPADeadlineValue;
//     }

//     var endFPADeadlineValue = localStorage.getItem('endFPADeadline');
//     if (endFPADeadlineValue) {
//         document.getElementById('endFPADeadline').value = endFPADeadlineValue;
//     }

//     // Recuperar os valores dos campos "startAssignmentDeadline" e "endAssignmentDeadline" do localStorage
//     var startAssignmentDeadlineValue = localStorage.getItem('startAssignmentDeadline');
//     if (startAssignmentDeadlineValue) {
//         document.getElementById('startAssignmentDeadline').value = startAssignmentDeadlineValue;
//     }

//     var endAssignmentDeadlineValue = localStorage.getItem('endAssignmentDeadline');
//     if (endAssignmentDeadlineValue) {
//         document.getElementById('endAssignmentDeadline').value = endAssignmentDeadlineValue;
//     }
// });

$("document").ready(function () {
    var blockName = $(".block-card").data("block-name");
    console.log(blockName);
    $("#blockName").text(blockName);
});