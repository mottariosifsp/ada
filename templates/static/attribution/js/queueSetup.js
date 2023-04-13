console.log('queueSetup.js loaded');

var texsto

$(document).ready(function() {
  $('#queue').DataTable();    
});

$(document).on('click', '.editable', function() {
  console.log('click');
  var cell = $(this);
  text = cell.text();
  var input = $('<input class="form-control" type="number" value="' + text + '"/>');
  cell.html(input);
  input.focus();
});

$(document).on('blur', '.editable input', function() {
  var input = $(this);
  var cell = input.parent();
  var oldText = input.val();
  text = input.val()-1;
  cell.text(text);
    
  row = cell.parent();
  oldRowIndex = $('table tbody tr').index(row)+1;
  $('#queue').DataTable().rows().invalidate().draw();
  newRowIndex = $('table tbody tr').index(row)+1;
  
  // console.log('new: '+(text+1)+' old: '+oldText);
  console.log('New: '+newRowIndex+' Old: '+oldRowIndex);
  if(text == oldText){

  } else if(parseInt(text) < parseInt(oldText)){
    console.log('subindo')
    for (let index = newRowIndex; index <= oldRowIndex; index++) {
      newPosition = parseInt($('table tbody tr:nth-child('+index+') td:nth-child(1)').text()) + 1;
      $('table tbody tr:nth-child('+index+') td:nth-child(1)').text(newPosition);    
    }
  } else {
    console.log('descendo')
   
    for (let index = newRowIndex+2; index < oldRowIndex; index--) {
      console.log('Index: ' + index)
      newPosition = parseInt($('table tbody tr:nth-child('+index+') td:nth-child(1)').text()) - 1;
      $('table tbody tr:nth-child('+index+') td:nth-child(1)').text(newPosition);  
    }
  } 
  // console.log('New: '+newRowIndex+' Old: '+oldRowIndex);
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
