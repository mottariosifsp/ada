console.log('queueSetup.js loaded');

var texto
var table
var tabelaData


$(document).ready(function() {
  table = $('#queue').DataTable(
    {
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


// $(document).on('click', '.editable', function() {
//   console.log('click');
//   var cell = $(this);
//   cell.removeClass('editable');
//   cell.addClass('editing');
//   text = cell.text();
//   var input = $('<input class="form-control" type="number" value="' + text + '"/>');
//   cell.html(input);
//   input.focus();
// });

// $(document).on('blur', '.editing input', function() {
//   var input = $(this);
//   var cell = input.parent();
//   var oldText = text;
//   text = input.val();

//   tabelaData = table.data().toArray();
//   tabelaData[oldText-1][0] = text-1;

//   cell.removeClass('editing');
//   cell.addClass('editable');  
  
//   if(text == oldText){
//     cell.html(parseInt(text));
//   } else if(parseInt(text) < parseInt(oldText)){

//     var professor = table.row(oldText);
//     table.row.add(professor,2).draw();


//     // tabela.cell(oldText-1, 0).data(parseInt(text)-1);
//     // tabela.rows().invalidate().draw();
//     // for (let index = parseInt(text); index <= parseInt(oldText); index++) {
//     //   tabela.cell(index-1, 0).data(parseInt(tabelaData[index-1][0])+1);
//     // }
    
//   } else {
//     table.cell(oldText-1, 0).data(parseInt(text)+1);
//     table.rows().invalidate().draw();
//     for (let index = parseInt(oldText); index <= text; index++) {
//       table.cell(index-1, 0).data(parseInt(tabelaData[index-1][0])-1);
//     }
//   }  
//   table.order( [ 1, 'asc' ]).draw();
  
//   // tabela.rows().invalidate().draw();
// });

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
        window.location.href = '.';
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

    