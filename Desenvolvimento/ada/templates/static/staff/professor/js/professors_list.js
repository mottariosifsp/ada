$(document).ready(function () { 
    
    $('.phone-input').on('input', function() {
        $(this).val(celphoneMask($(this).val()));
    });
    
    function celphoneMask(phone) {
        return phone.replace(/\D/g, '')
                    .replace(/^(\d)/, '($1')
                    .replace(/^(\(\d{2})(\d)/, '$1)$2')
                    .replace(/(\d{5})(\d{1,4})/, '$1-$2')
                    .replace(/(-\d{4})\d+?$/, '$1');
    }

    $('.telephone-input').on('input', function() {
        $(this).val(telephoneMask($(this).val()));
    });
    
    function telephoneMask(phone) {
        return phone.replace(/\D/g, '')
                    .replace(/^(\d)/, '($1')
                    .replace(/^(\(\d{2})(\d)/, '$1)$2')
                    .replace(/(\d{4})(\d{1,4})/, '$1-$2')
                    .replace(/(-\d{4})\d+?$/, '$1');
    }

    $('#professors_list').DataTable({
        "paging": false,
        "scrollY": "400px",
        "scrollCollapse": true,
        "scrollX": true,
        columnDefs: [
            {
                targets: [6,7,8,9,10,11,12],
                render: DataTable.render.datetime('DD/MM/YYYY')
            }
        ],
        
    });

    const tabela = document.getElementById("professors_list");
    const linhas = tabela.getElementsByTagName("tr");

    for (let i = 1; i < linhas.length; i++) {
        const primeiraCelula = linhas[i].getElementsByTagName("td")[0];
        primeiraCelula.classList.add("coluna-fixada");
    }
    

    var allblocks = [];

    // Adiciona um diploma à lista de diplomas do professor

    $(".addBlockBtn").on("click", function () {
        var parent = $(this).closest(".d-flex");
        if(parent.find(".blockInput").val() === "" || parent.find(".blockInput").val === undefined) {
            return;
        }
        block_name = parent.find(".blockInput").val();
        addBlockToList(block_name);

        $(".blockInput").val("");
        console.log(allblocks);
    });

    function addBlockToList(block_name) {   
        $(".currentBlocksList").append(
            "<li class='list-group-item d-flex align-items-center'><span class='block-name'>" +
            block_name + "</span><button type='button' class='btn btn-danger deleteClassBtn btn-remove-block ml-auto'><i class='bi bi-trash'></i></button></li>"
        );
        removeOption(block_name);
        allblocks.push(block_name);
    }

    $(document).on("click", ".btn-remove-block", function () {
        $(this).closest("li").remove();
        let block_deleted = $(this).closest("li").find(".block-name").text();
        addOption(block_deleted);
        allblocks.pop(block_deleted);
    });

    function addOption(name_blockk){
        $(".blocks-datalist").append("<option value='"+name_blockk+"'></option>");
    }

    function removeOption(name_blockk){
        $(".blocks-datalist option").each(function(){
            if($(this).val() == name_blockk){
                $(this).remove();
            }
        });
    }

    $('#createProfessorModal').on('hidden.bs.modal', function () {
        $(".currentBlocksList").empty();
        $(".blockInput").val("");
        for (let i = 0; i < allblocks.length; i++) {
            addOption(allblocks[i]);
        }
        allblocks = [];
                
    });
    $('#editProfessorModal').on('hidden.bs.modal', function () {
        $(".currentBlocksList").empty();
        $(".blockInput").val("");
        for (let i = 0; i < allblocks.length; i++) {
            addOption(allblocks[i]);
        }
        allblocks = [];
    });

    var allacademicDegrees = [];

    // Adiciona um diploma à lista de diplomas do professor

    $(".addCertificateBtn").on("click", function () {
        var parent = $(this).closest(".d-flex");
        if(parent.find(".degreeInput").val() === "" || 
            parent.find(".degreeInput").attr("score") === "" ||
            parent.find(".degreeInput").attr("score") === undefined ||
            parent.find(".degreeInput").val() === undefined) {
            return;
        }
        degree_name = parent.find(".degreeInput").val();
        degree_score = parent.find(".degreeInput").attr("score");
        addDegreeToList(degree_name, degree_score);

        $(".degreeInput").val("");
        $(".degreeInput").attr("score", "");
        console.log(allacademicDegrees);
    });

    function addDegreeToList(degree_name, degree_score) {   
        $(".currentAcademicDegreesList").append(
            "<li class='list-group-item d-flex align-items-center'><span class='academic-degree-name'>" +
            degree_name + "</span><span class='ml-auto'><small>Pontuação: <span class='academic-degree-punctuation'>" + degree_score +
            "</span></small></span><button type='button' class='btn btn-danger deleteClassBtn btn-remove-academic-degree ml-2'><i class='bi bi-trash'></i></button></li>"
        );
        allacademicDegrees.push(degree_name);
    }

    $(document).on("click", ".btn-remove-academic-degree", function () {
        $(this).closest("li").remove();
        let degree_deleted = $(this).closest("li").find(".academic-degree-name").text();
        allacademicDegrees.pop(degree_deleted);
    });

    // Limpa os campos do modal quando ele é fechado

    $('#createProfessorModal').on('hidden.bs.modal', function () {
        $(".currentAcademicDegreesList").empty();
        $(".degreeInput").val("");
        $(".degreeInput").attr("score", "");
        allacademicDegrees = [];
    });
    $('#editProfessorModal').on('hidden.bs.modal', function () {
        $(".currentAcademicDegreesList").empty();
        $(".degreeInput").val("");
        $(".degreeInput").attr("score", "");
        allacademicDegrees = [];
    });

    // adiciona um novo professor
    
    $("#add-professor").click(function () {
        $("#createProfessorModal").modal("show");
    });

    $("#saveNewProfessorBtn").click(function () {
        var registration_id = $('#add_registration_id').val();
        var first_name = $('#add_first_name').val();
        var last_name = $('#add_last_name').val();
        var email = $('#add_email').val();
        var telephone = $('#add_telephone').val();
        var celphone = $('#add_celphone').val();
        var birth = $('#add_birth').val();
        var date_career = $('#add_date_career').val();
        var date_campus = $('#add_date_campus').val();
        var date_professor = $('#add_date_professor').val();
        var date_area = $('#add_date_area').val();
        var date_institute = $('#add_date_institute').val();
        var job = $('#add_job').val();
        var blocks = JSON.stringify(allblocks);
        var academic_degrees = JSON.stringify(allacademicDegrees);
        var is_professor = $('#add_isProfessor').is(':checked');
        var is_staff = $('#add_isStaff').is(':checked');
        var is_fgfcc = $('#add_isFGFCC').is(':checked');
        
        var data = {
            add_registration_id: registration_id,
            add_first_name: first_name,
            add_last_name: last_name,
            add_email: email,
            add_telephone: telephone,
            add_celphone: celphone,
            add_birth: birth,
            add_date_career: date_career,
            add_date_campus: date_campus,
            add_date_professor: date_professor,
            add_date_area: date_area,
            add_date_institute: date_institute,
            add_job: job,
            add_academic_degrees: academic_degrees,
            add_blocks: blocks,
            add_is_professor: is_professor,
            add_is_staff: is_staff,
            add_is_fgfcc: is_fgfcc
        };

        let csrftoken = getCookie('csrftoken');

        $.ajax({
            method: 'POST', url: '/staff/professor-adiciondo/', data: data, headers: {
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

    // abre modal de edição de professor

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
            first_name: row.find('td:eq(0)').text(),
            last_name: row.find('td:eq(1)').text(),
            registration_id: row.find('td:eq(2)').text(),
            email: row.find('td:eq(3)').text(),
            telephone: row.find('td:eq(4)').text(),
            celphone: row.find('td:eq(5)').text(),
            birth: fomatDate(row.find('td:eq(6)').text()),
            date_career: fomatDate(row.find('td:eq(7)').text()),
            date_campus: fomatDate(row.find('td:eq(8)').text()),
            date_professor: fomatDate(row.find('td:eq(9)').text()),
            date_area: fomatDate(row.find('td:eq(10)').text()),
            date_institute: fomatDate(row.find('td:eq(11)').text()),
            job: row.find('td:eq(12)').text(),
            blocks: [],
            academic_degrees: [],
            is_professor: false,
            is_staff: false,
            is_fgfcc: false
        };
        row.find('td:eq(13)').find('span').each(function () {
            var blockId = $(this).attr('block-id');
            var blockName = $(this).attr('block-name');
            console.log(blockName);
            var block = {
                blockId: blockId, blockName: blockName 
            };
            professorData.blocks.push(block);
        });
        row.find('td:eq(14)').find('span').each(function () {
            var degreeId = $(this).data('degree-id')
            var degreeName = $(this).data('degree-name');
            var degreePunctuation = $(this).data('degree-punctuation');
            var degree = {
                degreeid: degreeId, name: degreeName, punctuation: degreePunctuation
            };
            professorData.academic_degrees.push(degree);
        });

        row.find('td:eq(15)').find('i').each(function () {
            var isProfessor = $(this).attr('is') === 'true';

            if (isProfessor) {
                professorData.is_professor = true;
            }
        });
        row.find('td:eq(16)').find('i').each(function () {
            var isStaff = $(this).attr('is') === 'true';

            if (isStaff) {
                professorData.is_staff = true;
            }
        });	
        row.find('td:eq(17)').find('i').each(function () {
            var isFGFCC = $(this).attr('is') === 'true';

            if (isFGFCC) {
                professorData.is_fgfcc = true;
            }
        });

        populateModal(professorData);
        $('#editProfessorModal').modal('show');
    });

    function fomatDate(date) {
        var parts = date.split('/');
        var formattedDate = parts[2] + '-' + parts[1] + '-' + parts[0];
        return formattedDate;
    }

    function populateModal(professorData) {
        $('#editProfessorModal').find('#registration_id').val(professorData.registration_id);
        $('#editProfessorModal').find('#first_name').val(professorData.first_name);
        $('#editProfessorModal').find('#last_name').val(professorData.last_name);
        $('#editProfessorModal').find('#email').val(professorData.email);
        if (professorData.telephone == "None" || professorData.telephone == "null" || professorData.telephone == "undefined" || professorData.telephone == "") {
            $('#editProfessorModal').find('#telephone').val('');
        }else{
            $('#editProfessorModal').find('#telephone').val(professorData.telephone.replace(/\s/g, ""));
        }
        if (professorData.celphone == "None" || professorData.celphone == "null" || professorData.celphone == "undefined" || professorData.celphone == "") {
            $('#editProfessorModal').find('#celphone').val('');
        }else{
            $('#editProfessorModal').find('#celphone').val(professorData.celphone.replace(/\s/g, ""));
        }
        $('#editProfessorModal').find('#birth').val(professorData.birth);
        $('#editProfessorModal').find('#date_career').val(professorData.date_career);
        $('#editProfessorModal').find('#date_campus').val(professorData.date_campus);
        $('#editProfessorModal').find('#date_professor').val(professorData.date_professor);
        $('#editProfessorModal').find('#date_area').val(professorData.date_area);
        $('#editProfessorModal').find('#date_institute').val(professorData.date_area);

        if(professorData.job == "None"){
            $('#editProfessorModal').find('#job').val("");
        }else if(professorData.job == "Substituto"){
            $('#editProfessorModal').find('#job').val("SUBSTITUTE");
        }else if(professorData.job == "Temporário"){
            $('#editProfessorModal').find('#job').val("TEMPORARY");
        }else if(professorData.job == "40 Horas"){
            $('#editProfessorModal').find('#job').val("FORTY_HOURS");
        }else if(professorData.job == "20 Horas"){
            $('#editProfessorModal' ).find('#job').val("TWENTY_HOURS");
        }else if(professorData.job == "RDE"){
            $('#editProfessorModal').find('#job').val("RDE");
        }else

        $('#editProfessorModal').find('#date_institute').val(professorData.date_institute);
        $(".currentBlocksList").empty();
        $(".currentAcademicDegreesList").empty();

        for (var i = 0; i < professorData.blocks.length; i++) {
            var block = professorData.blocks[i];
            addBlockToList(block.blockName);
            console.log(block.blockName);
        }

        // adiciona os diplomas do professor no modal
        for (var i = 0; i < professorData.academic_degrees.length; i++) {
            var degree = professorData.academic_degrees[i];
            addDegreeToList(degree.name, degree.punctuation);
            console.log(professorData.academic_degrees[i].name);
        }

        if (professorData.is_professor) {
            $('#editProfessorModal').find('#isProfessor').prop('checked', true);
        } else {
            $('#editProfessorModal').find('#isProfessor').prop('checked', false);
        }

        if (professorData.is_staff) {
            $('#editProfessorModal').find('#isStaff').prop('checked', true);
        } else {
            $('#editProfessorModal').find('#isStaff').prop('checked', false);
        }

        if (professorData.is_fgfcc) {
            $('#editProfessorModal').find('#isFGFCC').prop('checked', true);
        } else {
            $('#editProfessorModal').find('#isFGFCC').prop('checked', false);
        }

    }

    $("#saveUpdateBtn").click(function () {

        var academicDegrees = [];
        $("#currentAcademicDegreesList li").each(function () {
            var degreeName = $(this).find(".academic-degree-name").text();
            var degreePunctuation = $(this).find(".academic-degree-punctuation").text();

            if (degreeName !== undefined && degreeName.trim() !== "" &&
                degreePunctuation !== undefined && degreePunctuation.trim() !== "") {
                academicDegrees.push({name: degreeName, punctuation: degreePunctuation});
            }
        });


        var select = document.getElementById("courseDropdown");
        var blockedCourses = [];
        
        for (var i = 0; i < select.options.length; i++) {
            var option = select.options[i];
            if (option.selected) {
                blockedCourses.push(option.value);
            }
        }

        var first_name = $('#first_name').val();
        var last_name = $('#last_name').val();
        var registration_id = $('#registration_id').val();
        var email = $('#email').val();
        var telephone = $('#telephone').val();
        var celphone = $('#celphone').val();
        var birth = $('#birth').val();
        var date_career = $('#date_career').val();
        var date_campus = $('#date_campus').val();
        var date_professor = $('#date_professor').val();
        var date_area = $('#date_area').val();
        var date_institute = $('#date_institute').val();
        var job = $('#job').val();
        var blocks = JSON.stringify(allblocks);
        var academic_degrees = JSON.stringify(allacademicDegrees);
        var is_professor = $('#isProfessor').is(':checked');
        var is_staff = $('#isStaff').is(':checked');
        var is_fgfcc = $('#isFGFCC').is(':checked');
        var blocked_courses = blockedCourses;

        var data = {
            first_name: first_name,
            last_name: last_name,
            registration_id: registration_id,
            email: email,
            telephone: telephone,
            celphone: celphone,
            birth: birth,
            date_career: date_career,
            date_campus: date_campus,
            date_professor: date_professor,
            date_area: date_area,
            date_institute: date_institute,
            job: job,
            blocks: blocks,
            academic_degrees: academic_degrees,
            blocked_courses: blocked_courses,
            is_professor: is_professor,
            is_staff: is_staff,
            is_fgfcc: is_fgfcc
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
        academic_degrees = [];
    });

    $('.degreeInput').on('input', function() {
        const selectedOption = $(`#degrees option[value="${$(this).val()}"]`);
        if (selectedOption.length > 0) {
            const score = selectedOption.attr('score');
            $(this).attr('score', score);
        } else {
            $(this).removeAttr('score');
        }
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
