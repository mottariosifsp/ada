function backToTop() {
    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
}

function closeErrorAlert(id) {
    $("#"+ id).hide();
  }