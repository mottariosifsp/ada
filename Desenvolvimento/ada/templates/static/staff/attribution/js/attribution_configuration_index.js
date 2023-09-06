$(document).ready(function () {
    
});

function redirect(blockId, blockName) {
    localStorage.setItem('blockName', blockName);
    console.log(blockName);
    window.location.href = "../atribuicao/configuracao/?blockk="+blockId;
}