var lang = document.currentScript.getAttribute('data-lang');

var texto
var table
var tabelaData

var urlLang = 'pt-BR'
  // if(lang == 'en') {
  //   urlLang = 'en-BG'
  // } else {
  //   urlLang = 'pt-BR'
  // }

$(document).ready(function() {
  table = $('#queue').DataTable(
    {
        columnDefs: [
            { targets: [1], orderable: false}],
      rowReorder: true,
      language: {
        url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-BR.json'
      },
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

$('#enviar-tabela').click(function() {
    if (confirm('Deseja realmente enviar a tabela?')) {
  var tabelaData =  $('#queue').DataTable().data().toArray();
  var blockk_id = $('#blockk-id').attr('value');
  alert(blockk_id);
  console.log(tabelaData);
  var csrftoken = getCookie('csrftoken');

  $.ajax({
    url: '/attribution/queueSetup/',
    method: 'POST',
    data: {
      'tabela_data': JSON.stringify(tabelaData),
      'blockk_id': blockk_id,
    },
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: function(response) {
      location.reload();
    },
    error: function(xhr, status, error) {
      console.error(error);
    }
  });
    } else {
  }
});


// $('.submit-btn').click(function() {
//   var selectedArea = $('.area-select').val();
//   console.log("caiu");
//
//   var redirectURL = '/attribution/queueSetup/?area=' + selectedArea;
//
//   window.location.href = redirectURL;
// });

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
