$(document).ready(function() {

  var selectedOption

  $('.dropdown-item').click(function() {
    selectedOption = $(this).text();
    $(this).closest('.dropdown-menu').prev('.btn.dropdown-toggle').text(selectedOption);
    console.log($(this).parent().closest('.dropdown-toggle').text())
  });

  $('#searchInput').on('input', function() {
    var value = $(this).val().toLowerCase();
    selectedOption.parent().filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });  
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}