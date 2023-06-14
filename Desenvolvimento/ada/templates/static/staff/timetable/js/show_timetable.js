window.addEventListener('pageshow', function(event) {
    hide_loading()
});
  
$(document).ready(function() {
    document.addEventListener("DOMContentLoaded", function() {
        var editButton = document.querySelector(".editTimetable");
        editButton.addEventListener("click", function() {
          var urlParams = new URLSearchParams(window.location.search);
          var classs = urlParams.get("classs");
          var editUrl = "/grade/editar/?classs=" + classs;
          window.location.href = editUrl;
        });
      });
});