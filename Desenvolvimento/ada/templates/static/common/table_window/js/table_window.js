
//  $("#cel-"+value.cord).closest('.content_collapsible').prev('.collapsible').addClass("default-open");

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {

  var content = coll[i].nextElementSibling;

  if (coll[i].classList.contains("default-open")) {
    content.style.maxHeight = content.scrollHeight + "px";
  }

  coll[i].addEventListener("click", function() {
    this.classList.toggle("active_collapse");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}