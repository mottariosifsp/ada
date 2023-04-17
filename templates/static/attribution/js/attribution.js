var secondsLeft = document.currentScript.getAttribute('data-timeLeft');

$(document).ready(function() {

  
  var timerFormated = new Date(0);
  if(secondsLeft > 0){
    timerFormated.setSeconds(secondsLeft);
    var interval = setInterval(function () {
      timerFormated.setSeconds(timerFormated.getSeconds() - 1);
      $('#timer').html(timerFormated.toISOString().substr(11, 8));
      if(timerFormated.getSeconds() == 0){
        clearInterval(interval);
        let csrftoken = getCookie('csrftoken');
        $("#form").submit();
      }
    }, 1000);	
  } else {

  }
  
  
  
});

function get_data() {
  fetch('/attribution/')
      .then(response => response.json())
      .then(data => {
          alert(data.update);
      });
}

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