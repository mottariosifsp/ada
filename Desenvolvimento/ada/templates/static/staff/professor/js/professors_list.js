$(document).ready(function () {
    let table = new DataTable('#professors_list', {
        responsive: true
    });

    var allacademicDegrees = [];
    var academicDegreesList = $("#currentAcademicDegreesList");

  function addAcademicDegreeField() {
        var field = `
    <li class="list-group-item">
        <input type="text" class="form-control academic-degree-name mb-2" placeholder="Nome do diploma">
        <input type="number" class="form-control academic-degree-punctuation mb-2" placeholder="Pontuação">
        <button type="button" class="btn btn-danger deleteClassBtn btn-remove-academic-degree"><i class="bi bi-trash"></i></button>
    </li>
    `;

        $("#currentAcademicDegreesList").append(field);
        updateAcademicDegreesData();
    }

    function updateAcademicDegreesData() {
        var academicDegrees = [];

        $("#currentAcademicDegreesList li").each(function () {
            var degreeName = $(this).find(".academic-degree-name").val();
            var degreePunctuation = $(this).find(".academic-degree-punctuation").val();

            if (degreeName !== undefined && degreeName.trim() !== "" &&
                degreePunctuation !== undefined && degreePunctuation.trim() !== "") {
                academicDegrees.push({name: degreeName, punctuation: degreePunctuation});
            }
        });

        allacademicDegrees = JSON.stringify(academicDegrees);
    }

    $(document).on("click", ".btn-remove-academic-degree", function () {
        $(this).closest("li").remove();
        updateAcademicDegreesData();
    });


    $("#currentAcademicDegreesList li").each(function () {
        var degreeName = $(this).find(".btn-edit-academic-degree").data("name");
        var degreePunctuation = $(this).find(".btn-edit-academic-degree").data("punctuation");
        $(this).find(".btn-edit-academic-degree").click(function () {
        });
        $(this).find(".btn-remove-academic-degree").click(function () {
            $(this).closest("li").remove();
            updateAcademicDegreesData();
        });
    });


    $("#addAcademicDegreeBtn").on("click", function () {
        addAcademicDegreeField();

    });

    function addClassesNotAllowedField() {
        var field = `
        <li class="list-group-item">
            <input type="text" class="form-control class-name mb-2" placeholder="Nome da classe">
            <input type="number" class="form-control class-level mb-2" placeholder="Nível da classe">
            <button type="button" class="btn btn-danger deleteClassBtn btn-remove-class"><i class="bi bi-trash"></i></button>
        </li>
        `;
    
        $("#currentClassesNotAllowedList").append(field);
        updateClassesNotAllowedData();
    }
    
    function updateClassesNotAllowedData() {
        var classesNotAllowed = [];
    
        $("#currentClassesNotAllowedList li").each(function () {
            var className = $(this).find(".class-name").val();
            var classLevel = $(this).find(".class-level").val();
    
            if (className !== undefined && className.trim() !== "" &&
                classLevel !== undefined && classLevel.trim() !== "") {
                classesNotAllowed.push({ name: className, level: classLevel });
            }
        });
    
        allClassesNotAllowed = JSON.stringify(classesNotAllowed);
    }
    
    $(document).on("click", ".btn-remove-class", function () {
        $(this).closest("li").remove();
        updateClassesNotAllowedData();
    });
    
    $("#addNotAllowedClassBtn").on("click", function () {
        addClassesNotAllowedField();
    });
    

    $('.btn-warning').click(function () {
        var row = $(this).closest('tr');
        var professorData = {
            registration_id: row.find('td:eq(0)').text(),
            first_name: row.find('td:eq(1)').text(),
            birth: row.find('td:eq(2)').text(),
            date_career: row.find('td:eq(3)').text(),
            date_campus: row.find('td:eq(4)').text(),
            date_professor: row.find('td:eq(5)').text(),
            date_area: row.find('td:eq(6)').text(),
            date_institute: row.find('td:eq(7)').text(),
            academic_degrees: []
        };

        row.find('td:eq(8)').find('span').each(function () {
            var degreeId = $(this).data('degree-id')
            var degreeName = $(this).data('degree-name');
            var degreePunctuation = $(this).data('degree-punctuation');
            var degree = {
                degreeid: degreeId, name: degreeName, punctuation: degreePunctuation
            };
            professorData.academic_degrees.push(degree);
        });

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

        $("#currentAcademicDegreesList").empty();

        // adiciona os diplomas do professor no modal
        for (var i = 0; i < professorData.academic_degrees.length; i++) {
            var degree = professorData.academic_degrees[i];
            var listItem = $('<li class="list-group-item">' +
                '<input type="text" class="form-control academic-degree-name mb-2" value="' + degree.name + '" placeholder="Nome do diploma">' +
                '<input type="number" class="form-control academic-degree-punctuation mb-2" value="' + degree.punctuation + '" placeholder="Pontuação">' +
                '<button type="button" class="btn btn-danger deleteClassBtn btn-remove-academic-degree"><i class="bi bi-trash"></i></button>' +
                '</li>');

            academicDegreesList.append(listItem);
        }
    }

    $("#saveUpdateBtn").click(function () {
        updateAcademicDegreesData();

        var academicDegrees = [];
        $("#currentAcademicDegreesList li").each(function () {
            var degreeName = $(this).find(".academic-degree-name").text();
            var degreePunctuation = $(this).find(".academic-degree-punctuation").text();

            if (degreeName !== undefined && degreeName.trim() !== "" &&
                degreePunctuation !== undefined && degreePunctuation.trim() !== "") {
                academicDegrees.push({name: degreeName, punctuation: degreePunctuation});
            }
        });

        updateAcademicDegreesData(academicDegrees);

        var registration_id = $('#registration_id').val();
        var birth = $('#birth').val();
        var date_career = $('#date_career').val();
        var date_campus = $('#date_campus').val();
        var date_professor = $('#date_professor').val();
        var date_area = $('#date_area').val();
        var date_institute = $('#date_institute').val();
        var academic_degrees = allacademicDegrees;

        var data = {
            registration_id: registration_id,
            birth: birth,
            date_career: date_career,
            date_campus: date_campus,
            date_professor: date_professor,
            date_area: date_area,
            date_institute: date_institute,
            academic_degrees: academic_degrees
        };

        let csrftoken = getCookie('csrftoken');

        $.ajax({
            method: 'POST', url: '/staff/alteracoes-salvas/', data: data, headers: {
                'X-CSRFToken': csrftoken
            }, success: function (response) {
                location.reload();
                console.log(response);
                $('#editProfessorModal').modal('hide');
            }, error: function (xhr, status, error) {
                console.log(error);
            }
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
