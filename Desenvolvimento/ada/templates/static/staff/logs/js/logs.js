$(document).ready(function() {
    table = $('#logs_list').DataTable({
        columnDefs: [
            {
                orderable: false,
                className: 'select-checkbox',
                targets: 0
            }
        ],
        select: {
            style: 'multi',
            selector: 'td:first-child'
        },
        order: [[1, 'asc']]
    });

    var selectedAll = false;

    $('#selectAllButton').on('click', function () {
        if (table.page.info().recordsDisplay > 0) {
            if (selectedAll) {
                table.rows().deselect();
                selectedAll = false;
            } else {
                table.rows({ search: 'applied' }).select();
                selectedAll = true;
            }
        }
    });

    $('#deleteSelectedButton').on('click', function () {
        var selectedData = table.rows({ selected: true }).data();
        var selectedIds = [];
        for (var i = 0; i < selectedData.length; i++) {
            selectedIds.push(selectedData[i][1]);
        }

        var data = {
            logs: selectedIds
        };

        data.logs = JSON.stringify(data.logs);

        var csrftoken = getCookie('csrftoken');
        $.ajax({
            method: 'POST', url: 'deletar-logs/', 
            data: data, 
            headers: {
                'X-CSRFToken': csrftoken
            }, success: function (response) {
                location.reload();
            }, error: function (xhr, status, error) {
                console.log(xhr.responseText);
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