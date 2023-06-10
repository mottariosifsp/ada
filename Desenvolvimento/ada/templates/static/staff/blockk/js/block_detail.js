$(document).ready(function() {
    let table = new DataTable('#blocks_list', {
        responsive: true
    });

    $('#saveCreateBtn').click(function() {
        var registration_course_id = $('#registration_course_id_create').val();
        var name_course = $('#name_course_create').val();
        var acronym = $('#acronym_create').val();
        var areaId = $(this).data('area-id');
        var blockId = $(this).data('block-id');

        var data = {
            registration_course_id: registration_course_id,
            name_course: name_course,
            acronym: acronym,
            areaId: areaId,
            blockId: blockId
        };

        let csrftoken = getCookie('csrftoken');

        // Enviar dados para o servidor via requisição AJAX
        $.ajax({
            method: 'POST',
            url: '/staff/detalhes-bloco/criar-materia',
            data: data,

            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                location.reload();
                $('#createCourseModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    $('.editCourseBtn').click(function() {
        var row = $(this).closest('tr');
        var courseId = $(this).data('course-id');

        $('#editCourseModal').data('course-id', courseId);
        var courseData = {
            registration_course_id: row.find('td:eq(0)').text(),
            name_course: row.find('td:eq(1)').text(),
            acronym: row.find('td:eq(2)').text(),
        };


        populateModal(courseData);
        $('#editCourseModal').modal('show');
    });

    $('#saveUpdateBtn').click(function() {
        var courseId = $('#editCourseModal').data('course-id');
        var registration_course_id = $('#registration_course_id_update').val();
        var name_course = $('#name_course_update').val();
        var acronym = $('#acronym_update').val();

        var data = {
            id: courseId,
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
                $('#editCourseModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    function populateModal(courseData) {
        $('#editCourseModal #registration_course_id_update').val(courseData.registration_course_id);
        $('#editCourseModal #name_course_update').val(courseData.name_course);
        $('#editCourseModal #acronym_update').val(courseData.acronym);
    }

    // Deletar matéria

    $('.deleteCourseBtn').click(function(event) {
        event.preventDefault();
        var courseId = $(this).data('course-id');
        var registrationCourseId = $(this).data('registration-course-id');
        var deleteUrl = '/staff/detalhes-bloco/deletar-materia';

        // Modal confirmação
        var row = $(this).closest('tr');
        var classData = {
            registration_course_id: row.find('td:eq(0)').text()
        };

        populateModal(classData);
        $('#confirmDeleteCourseModal').modal('show');

        function populateModal(classData) {
            $('#registrationCourseId').text(classData.registration_course_id);
        }

        $('#confirmDeleteCourseModal').modal('show');
        $('#confirmDeleteCourseModal').on('shown.bs.modal', function() {
            $('#registrationCourseId').text(registrationCourseId);
        });
    
        // Exclusão
        $('#confirmDeleteCourseBtn').click(function() {
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
                    alert("Erro ao deletar a disciplina.");
                    console.error(error);
                }
            });
    
            $('#confirmDeleteCourseModal').modal('hide');
        });
    });

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
