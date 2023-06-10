
$(document).ready(function() {
    let table = new DataTable('#classes_list', {
        responsive: true
    });

    // Criar turma

    $('.createClassBtn').click(function() {
        $('#createClassModal').modal('show');
    });
    
    $('#saveCreateBtn').click(function() {
        var registration_class_id = $('#registration_class_id_create').val();
        var period = $('#period_create').val();
        var semester = $('#semester_create').val();
        var area = $('#area_create').val();
    
        var data = {
            registration_class_id: registration_class_id,
            period: period,
            semester: semester,
            area: area
        };
    
        let csrftoken = getCookie('csrftoken');
    
        // Enviar dados para o servidor via requisição AJAX
        $.ajax({
            method: 'POST',
            url: '/staff/turmas/cadastrar/', 
            data: data,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                location.reload();
                console.log(response);
                $('#createClassModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });


    // Editar turma

    $('.editClassBtn').click(function() {
        var row = $(this).closest('tr');
        var classData = {
            registration_class_id: row.find('td:eq(0)').text(),
            period: row.find('td:eq(1)').text(),
            semester: row.find('td:eq(2)').text(),
            area: row.find('td:eq(3)').text()
        };
    
        populateModal(classData);
        $('#editClassModal').modal('show');
    });

    function populateModal(classData) {
        $('#editClassModal').find('#registration_class_id_edit').val(classData.registration_class_id);
        $('#editClassModal').find('#period_edit').val(classData.period);
        $('#editClassModal').find('#semester_edit').val(classData.semester);
        $('#editClassModal').find('#area_edit').val(classData.area);
    }

    $('#saveUpdateClassBtn').click(function() {
        var registration_class_id = $('#registration_class_id_edit').val();
        var period = $('#period_edit').val();
        var semester = $('#semester_edit').val();
        var area = $('#area_edit').val();
        console.log("funcionou o botão")
        
        var data = {
            registration_class_id: registration_class_id,
            period: period,
            semester: semester,
            area: area
        };
        console.log("funcionou o data")

        let csrftoken = getCookie('csrftoken');

        // Enviar dados para o servidor via requisição AJAX
        $.ajax({
            method: 'POST',
            url: '/staff/turmas/alteracoes-salvas/', 
            data: data,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                location.reload();
                console.log(response);
                $('#editClassModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
        console.log("funcionou o ajax")
    });

    // Deletar turma

    $('.deleteClassBtn').click(function(event) {
        event.preventDefault();
        var classId = $(this).data('class-id');
        var registrationClassId = $(this).data('registration-class-id');
        var deleteUrl = '/staff/turmas/deletar/';

        // Modal confirmação
        var row = $(this).closest('tr');
        var classData = {
            registration_class_id: row.find('td:eq(0)').text()
        };
        populateModal(classData);
        $('#confirmDeleteModal').modal('show');
        function populateModal(classData) {
            $('#registrationClassId').text(classData.registration_class_id);
        }


        $('#confirmDeleteModal').modal('show');
        $('#confirmDeleteModal').on('shown.bs.modal', function() {
            $('#registrationClassId').text(registrationClassId);
        });
        console.log("funcionou o modal")
    
        $('#confirmDeleteClassBtn').click(function() {
            let csrftoken = getCookie('csrftoken');
            console.log("funcionou antes do ajax")
    
            $.ajax({
                method: 'POST',
                url: deleteUrl,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'id': classId
                },
                success: function(response) {
                    location.reload();
                },
                error: function(xhr, status, error) {
                    alert("Erro ao deletar a turma.");
                    console.error(error);
                }
            });
    
            $('#confirmDeleteModal').modal('hide');
            console.log("funcionou o ajax")
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
