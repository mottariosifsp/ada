
$(document).ready(function() {
    let table = new DataTable('#classes_list', {
        responsive: true
    });
    $('.btn-warning').click(function() {
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
        $('#editClassModal').find('#registration_class_id').val(classData.registration_class_id);
        $('#editClassModal').find('#period').val(classData.period);
        $('#editClassModal').find('#semester').val(classData.semester);
        $('#editClassModal').find('#area').val(classData.area);
    }

    $('#saveUpdateClassBtn').click(function() {
        var registration_class_id = $('#registration_class_id').val();
        var period = $('#period').val();
        var semester = $('#semester').val();
        var area = $('#area').val();
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