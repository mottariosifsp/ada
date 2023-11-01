$(document).ready(function () {
    
});

function redirect(blockId, blockName) {
    localStorage.setItem('blockName', blockName);
    console.log(blockName);
    window.location.href = "../professores/lista/?blockk="+blockId;
}