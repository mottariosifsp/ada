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
    // Capturar evento de clique no botão "Salvar Alterações"
    $('#saveUpdate').click(function() {
        // Valores dos campos do formulário no modal
        var birth = $('#birth').val();
        var date_career = $('#date_career').val();
        var date_campus = $('#date_campus').val();
        var date_professor = $('#date_professor').val();
        var date_area = $('#date_area').val();
        var date_institute = $('#date_institute').val();

        // Objeto com os dados a serem enviados para o servidor
        var data = {
            birth: birth,
            date_career: date_career,
            date_campus: date_campus,
            date_professor: date_professor,
            date_area: date_area,
            date_institute: date_institute
        };

        // Enviar dados para o servidor via requisição AJAX
        $.ajax({
            type: 'POST',
            url: '/update_save/', 
            data: data,
            success: function(response) {
                console.log(response);
                $('#editProfessorModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});
