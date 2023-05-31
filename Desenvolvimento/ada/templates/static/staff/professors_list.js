
$(document).ready(function() {
    let table = new DataTable('#professors_list', {
        responsive: true
    });
    $('.btn-warning').click(function() {
        var row = $(this).closest('tr');
        var professorData = {
            registration_id: row.find('td:eq(0)').text(),
            first_name: row.find('td:eq(1)').text(),
            birth: row.find('td:eq(2)').text(),
            date_career: row.find('td:eq(3)').text(),
            date_campus: row.find('td:eq(4)').text(),
            date_professor: row.find('td:eq(5)').text(),
            date_area: row.find('td:eq(6)').text(),
            date_institute: row.find('td:eq(7)').text()
        };
    
        populateModal(professorData);
        $('#editProfessorModal').modal('show');
    });

    function populateModal(professorData) {
        $('#editProfessorModal').find('#registration_id').val(professorData.registration_id);
        $('#editProfessorModal').find('#first_name').val(professorData.first_name);
        $('#editProfessorModal').find('#birth').val(professorData.birth);
        $('#editProfessorModal').find('#date_career').val(professorData.date_career);
        $('#editProfessorModal').find('#date_campus').val(professorData.date_campus);
        $('#editProfessorModal').find('#date_professor').val(professorData.date_professor);
        $('#editProfessorModal').find('#date_area').val(professorData.date_area);
        $('#editProfessorModal').find('#date_institute').val(professorData.date_institute);
    }

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
