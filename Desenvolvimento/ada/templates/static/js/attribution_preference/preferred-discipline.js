$(document).ready(function() {
    // Capturar os valores do formulário e adicionar na lista e no banco de dados
    $('#addCourseButton').click(function() {
      var courseName = $('#courseName').val();
      var numClasses = $('#numClasses').val();
      var priority = $('input[name="priority"]:checked').val();
      var period = $('#period').val();
  
      // Realizar a ação de adicionar no banco de dados
      // ...
  
      // Adicionar na lista
      var newItem = '<li>' + courseName + '</li>';
      $('#courseList').append(newItem);
  
      // Fechar o modal
      $('#addCourseModal').modal('hide');
  
      // Limpar o formulário
      $('#addCourseForm')[0].reset();
    });
  });