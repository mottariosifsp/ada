var courses = [];

$(document).ready(function() {
  function addCourseToTable(course) { // adiciona na parte do html uma linha com cada course
    var row = '<tr>' +
                '<td class="text-center">' + course.sigla + '</td>' +
                '<td class="text-center">' + course.nome + '</td>' +
                '<td class="text-center">' + course.numAulas + '</td>' +
                '<td class="text-center">' + course.turno + '</td>' +
                '<td class="text-center">' + course.prioridade + '</td>' +
                '<td class="text-center">' +
                  '<button class="btn btn-danger btn-delete" data-course-index="'+ (courses.length - 1) +'">Deletar</button>' +
                '</td>' +
              '</tr>';
    $('#course-table-body').append(row);
  }

  function updateDataAttribute() { // atualiza a tabela com a lista de courses (a global)
    $('#course-preference-list').data('courses', courses);
  }

  $('#addCourseButton').click(function() {
    var courseName = $('#courseName').find(':selected').val();
    var numClasses = $('#numClasses').val();
    var priority = $('input[name="priority"]:checked').val();
    var period = $('#period').val();

    // verifica se todos os campos foram preenchidos
    if (courseName && numClasses && priority && period) {
      var course = {
        sigla: courseName,
        nome: courseName,
        numAulas: numClasses,
        turno: period,
        prioridade: priority
      };

      // Verifica se o curso já existe na lista
      var isCourseExists = courses.some(function(existingCourse) {
        return existingCourse.sigla === course.sigla && existingCourse.nome === course.nome;
      });

      var isCoursePropertiesExists = courses.some(function(existingCourse) {
        return existingCourse.turno === course.turno;
      });

      if (isCourseExists) {
        if (!isCoursePropertiesExists) {
          var csrftoken = $('[name=csrfmiddlewaretoken]').val();

          $.ajax({
            type: 'POST',
            url: '/preferencia-atribuicao/',
            data: course,
            beforeSend: function(xhr) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
              courses.push(course);
              addCourseToTable(course);
              updateDataAttribute();
              $('#courseName').val('');
              $('#numClasses').val('');
              $('input[name="priority"]').prop('checked', false);
              $('#period').val('');
              $('#error-alert').hide();
            },
            error: function(xhr, status, error) {
              $('#error-message').text('Ocorreu um erro ao adicionar o curso.');
              $('#error-alert').show();
            }
          });
        } else {
          $('#error-message').text('O curso já existe no mesmo turno.');
        $('#error-alert').show();
        }
      } else {
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
          type: 'POST',
          url: '/preferencia-atribuicao/',
          data: course,
          beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          },
          success: function(response) {
            courses.push(course);
            addCourseToTable(course);
            updateDataAttribute();
            $('#courseName').val('');
            $('#numClasses').val('');
            $('input[name="priority"]').prop('checked', false);
            $('#period').val('');
            $('#error-alert').hide();
          },
          error: function(xhr, status, error) {
            $('#error-message').text('Ocorreu um erro ao adicionar o curso.');
            $('#error-alert').show();
          }
        });
      }
    } else {
      $('#error-message').text('Por favor, preencha todos os campos.');
      $('#error-alert').show();
    }
  });

  function deleteCourseFromTable(courseIndex) {
    courses.splice(courseIndex, 1);
    updateDataAttribute();
    $('#course-table-body').empty();
    courses.forEach(function(course) {
      addCourseToTable(course);
    });
  }

  $(document).on('click', '.btn-delete', function() {
    var courseIndex = $(this).data('course-index');
    deleteCourseFromTable(courseIndex);
  });

  $(document).on('click', '[data-dismiss="modal"]', function() {
    $('#courseName').val('');
    $('#numClasses').val('');
    $('input[name="priority"]').prop('checked', false);
    $('#period').val('');
    $('#error-alert').hide();
  });
});

$(document).ready(function() {
  $('#addCourseButton').click(function() {

  })
});
