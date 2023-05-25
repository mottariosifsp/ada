var lang = document.currentScript.getAttribute('data-lang');

console.log(5)
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

$(document).on('click', '#getData', function() {
  table.order( [ 1, 'asc' ]).draw();
  tabelaData =  table.data().toArray();
  console.log(tabelaData);
});