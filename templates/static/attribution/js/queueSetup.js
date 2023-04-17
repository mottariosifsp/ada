var lang = document.currentScript.getAttribute('data-lang');

var texto
var table
var tabelaData


$(document).ready(function() {
  table = $('#queue').DataTable(
    {
      searching: false,
      "paging": false,
      "bInfo" : false,
      rowReorder: true
    }
  ); 
  
  table.on('row-reorder', function(e, diff, edit) {
     var result = 'Reorder started on row: '+edit.triggerRow.data()[1]+'<br>';
 
        for ( var i=0, ien=diff.length ; i<ien ; i++ ) {
            var rowData = table.row( diff[i].node ).data();
 
            result += rowData[1]+' updated to be in position '+
            diff[i].newData+' (was '+diff[i].oldData+')<br>';
        }
 
        $('#result').html( 'Event result:<br>'+result );
  });
});

$(document).on('click', '#getData', function() {
  table.order( [ 1, 'asc' ]).draw();
  tabelaData =  table.data().toArray();
  console.log(tabelaData);
});

$('#enviar-tabela').click(function() {
    var tabelaData =  $('#queue').DataTable().data().toArray();
    console.log(tabelaData);
    let csrftoken = getCookie('csrftoken');
    $.ajax({
      url: '/attribution/',
      method: 'POST',
      data: {
        'tabela_data': JSON.stringify(tabelaData)
      },
      headers: {
        'X-CSRFToken': csrftoken
      },
      success: function(response) {
        window.location.href = '/' + lang + '/attribution/';
      },
      error: function(xhr, status, error) {
        alert('Erro ao enviar dados!');
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

    