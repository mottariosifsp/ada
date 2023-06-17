

function countdown(elementId, timeString) {
    let totalSeconds = getTotalSeconds(timeString);
    const element = document.getElementById(elementId);
  
    const intervalId = setInterval(() => {
      if (totalSeconds <= 0) {
        clearInterval(intervalId);
        window.location.reload();
        return;
      }
  
      const hours = Math.floor(totalSeconds / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;
      element.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  
      totalSeconds--;
    
    }, 1000);
  }
  
function getTotalSeconds(timeString) {
    const [hours, minutes, seconds] = timeString.split(':').map(Number);
    return (hours * 3600) + (minutes * 60) + seconds;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
  

var time_left = document.currentScript.getAttribute('time-left');

$(document).ready(function(){
    countdown('time-left', time_left);
     

});