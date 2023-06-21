var url = document.currentScript.getAttribute("url");

$(document).ready(function() {
    
    if(url != null || url != "") {
        $("#return-button").click(function() {
            window.location.href = url;
        });
    }else {
        $("#return-button").click(function() {
            window.location.href = "/";
        });
    }
    
});