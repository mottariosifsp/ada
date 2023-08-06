$(document).ready(function(){
    $(".btn").click(function(){
        var url = $(this).attr('url');
        redirect(url);
    });
});
    
function redirect(url){
    window.location.href = url;
}