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