var lang = document.currentScript.getAttribute('data-lang');
var time_left = 0.0
var hour = 0
var minute = 0

$(document).ready(function() {
    var campoInputBlock = document.getElementById("campoInputBlock");
    campoInputBlock.value = document.querySelector("#opcoes option:first-child").value;
    campoInputBlock.addEventListener("input", function() {
        campoInputBlock.setCustomValidity("");
    });
    campoInputBlock.addEventListener("invalid", function() {
        if (campoInputBlock.value === "") {
        campoInputBlock.setCustomValidity("Selecione uma opção da lista.");
        }
    });
});

    