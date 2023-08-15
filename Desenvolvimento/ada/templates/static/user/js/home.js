$(document).ready(function(){
    $(".btn").click(function(){
        var url = $(this).attr('url');
        redirect(url);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.hover-button');

    var buttonCount = buttons.length;

    buttons.forEach(function(button) {
        var parentDiv = button.parentElement; // Obtém a div pai do botão

        if (buttonCount == 2) {
            parentDiv.classList.add('col-lg-6');
        } else if (buttonCount == 3) {
            parentDiv.classList.add('col-md-4');
        }
    });
});
    
function redirect(url){
    window.location.href = url;
}