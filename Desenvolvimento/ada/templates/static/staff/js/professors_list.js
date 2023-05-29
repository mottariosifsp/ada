$(document).ready( function () {
    $('#professors_list').DataTable();
} );
let table = new DataTable('#professors_list', {
    responsive: true
});