// Carregar DataTable

$(document).ready( function () {
    $('#professors_list').DataTable();
} );
let table = new DataTable('#professors_list', {
    responsive: true
});

// Modal

$(document).on('click', '[data-dismiss="modal"]', function() {
    $('#courseName').val('');
    $('#numClasses').val('');
    $('input[name="priority"]').prop('checked', false);
    $('#period').val('');
    $('#error-alert').hide();
});

// Salvar alterações

$(document).ready(function() {
    $('#saveUpdateBtn').click(function() {
        var registration_id = $('#registration_id').val();
        var birth = $('#birth').val();
        var date_career = $('#date_career').val();
        var date_campus = $('#date_campus').val();
        var date_professor = $('#date_professor').val();
        var date_area = $('#date_area').val();
        var date_institute = $('#date_institute').val();
        console.log("funcionou o botão")
        
        var data = {
            registration_id: registration_id,
            birth: birth,
            date_career: date_career,
            date_campus: date_campus,
            date_professor: date_professor,
            date_area: date_area,
            date_institute: date_institute
        };
        console.log("funcionou o data")

        let csrftoken = getCookie('csrftoken');

        // Enviar dados para o servidor via requisição AJAX
        $.ajax({
            method: 'POST',
            url: '/staff/alteracoes-salvas/', 
            data: data,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                location.reload();
                console.log(response);
                $('#editProfessorModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
        console.log("funcionou o ajax")
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
