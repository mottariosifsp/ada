$(document).ready(function() {
    let table = new DataTable('#blocks_list', {
        responsive: true
    });

    $('.editCourseBtn').click(function() {
        var row = $(this).closest('tr');
        var courseData = {
            id: row.find('td:eq(0)').text(),
            registration_course_id: row.find('td:eq(1)').text(),
            name_course: row.find('td:eq(2)').text(),
            acronym: row.find('td:eq(3)').text(),
        };

        populateModal(courseData);
        $('#editCourseModal').modal('show');
    });

    $('.deleteCourseBtn').click(function(event) {
        event.preventDefault();
        var courseId = $(this).data('course-id');
        var deleteUrl = '/staff/detalhes-bloco/deletar-materia';

        if (confirm("Tem certeza que deseja deletar o curso?")) {
            let csrftoken = getCookie('csrftoken');

            $.ajax({
                method: 'POST',
                url: deleteUrl,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'id': courseId
                },
                success: function(response) {
                    location.reload();
                },
                error: function(xhr, status, error) {
                    alert("Erro ao deletar o curso.");
                    console.error(error);
                }
            });
        }
    });

    $('#saveUpdateBtn').click(function() {
        var id = $('#id').val();
        var registration_course_id = $('#registration_course_id').val();
        var name_course = $('#name_course').val();
        var acronym = $('#acronym').val();

        var data = {
            id: id,
            registration_course_id: registration_course_id,
            name_course: name_course,
            acronym: acronym,
        };

        let csrftoken = getCookie('csrftoken');

        // Enviar dados para o servidor via requisição AJAX
        $.ajax({
            method: 'POST',
            url: '/staff/detalhes-bloco/atualizar-bloco',
            data: data,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                location.reload();
                console.log(response);
                $('#editCourseModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    function populateModal(courseData) {
        $('#editCourseModal #id').val(courseData.id);
        $('#editCourseModal #registration_course_id').val(courseData.registration_course_id);
        $('#editCourseModal #name_course').val(courseData.name_course);
        $('#editCourseModal #acronym').val(courseData.acronym);
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
