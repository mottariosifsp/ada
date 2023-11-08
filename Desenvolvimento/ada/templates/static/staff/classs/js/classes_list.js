
$(document).ready(function() {
    $(".alert-danger").hide();

    let table = new DataTable('#classes_list', {
        responsive: true,
        "paging": false,
        "scrollY": "400px",
    });

    // Criar turma

    let classEditing = null;

    $('.createClassBtn').click(function() {
        $('#createClassModal').modal('show');
        $(".alert-danger").hide();
    });
    
    $('#saveCreateBtn').click(function() {
        $(".alert-danger").hide();

        var registration_class_id = $('#registration_class_id_create').val();
        var period = $('#period_create').val();
        var semester = $('#semester_create').val();
        var area = $('#area_create').val();
        
        if(isEmpty(registration_class_id, period, semester, area)){
            $(".alert-danger").show();
            $(".alert-danger").text("Todos os campos devem ser preenchidos.");
            return;
        }

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
            }, error: function (xhr, status, error) {
                $(".alert-danger").show();
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    $(".alert-danger").text(xhr.responseJSON.error);
                } else {
                    $(".alert-danger").text("An error occurred.");
                }
            }
        });
    });

    

    // Editar turma

    $('.editClassBtn').click(function() {
        $(".alert-danger").hide();

        var row = $(this).closest('tr');
        var rowData = table.row(row).data(); // Obtenha os dados da linha usando DataTables

        console.log(rowData);

        var classData = {
            registration_class_id: rowData[0],
            period: rowData[1],
            semester: rowData[2],
            area: rowData[3]
        };

        console.log(classData);

        populateModal(classData);
        $('#editClassModal').modal('show');
    });

    function populateModal(classData) {
        classEditing = classData.registration_class_id;
        $('#editClassModal').find('#registration_class_id_edit').val(classData.registration_class_id);
        $('#editClassModal').find('#registration_class_id_edit').data('old-registration-class-id', classData.registration_class_id);
        $('#editClassModal').find('#period_edit').val(classData.period);
        $('#editClassModal').find('#semester_edit').val(classData.semester);

        var select = null;
        var selectedOption = $('#area_edit option').filter(function() {
            let str = $(this).text().replace(/\s/g, '').toUpperCase();
            let area = classData.area.replace(/\s/g, '').toUpperCase();
            console.log(str,'-' ,area)
            if (str === area){
                select = $(this).val(); 
            }
        });

        $('#editClassModal').find('#area_edit').val(select);
    }

    function change_val(){
        
    }

    $('#saveUpdateClassBtn').click(function() {
        var registration_class_id = $('#registration_class_id_edit').val();
        var old_registration_class_id = $('#registration_class_id_edit').data('old-registration-class-id');
        var period = $('#period_edit').val();
        var semester = $('#semester_edit').val();
        var area = $('#area_edit').val();
        
        if(isEmpty(registration_class_id, period, semester, area)){
            $(".alert-danger").show();
            $(".alert-danger").text("Todos os campos devem ser preenchidos.");
            return;
        }

        var data = {
            old_registration_class_id: old_registration_class_id,
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
            }, error: function (xhr, status, error) {
                $(".alert-danger").show();
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    $(".alert-danger").text(xhr.responseJSON.error);
                } else {
                    $(".alert-danger").text("An error occurred.");
                }
            }
        });
        console.log("funcionou o ajax")
        classEditing = null;
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
    
        // Exclusão
        $('#confirmDeleteClassBtn').click(function() {
            let csrftoken = getCookie('csrftoken');
    
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

function isEmpty(...str) {

    for(let i = 0; i < str.length; i++) {
        str[i] = str[i].replace(/\s/g, '');
        if (!str[i] || 0 === str[i].length) {
            return true;
        }
    }

    return (!str || 0 === str.length);
}