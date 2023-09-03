var timetables_user = document.currentScript.getAttribute("timetables-user");
var timetables_user = JSON.parse(timetables_user);
console.log("timetables_user", timetables_user);

var timeslots = document.currentScript.getAttribute("timeslots");

console.log("Timeslots", timeslots);

var json_data  = document.currentScript.getAttribute("jsonData");
console.log("Json data", json_data);
// var timetables_complete  = JSON.parse(timetables_complete);

// var jsonDataAttribute = document.currentScript.getAttribute("jsonData");
// var json_data = jsonDataAttribute;
//
//
$('.header-table').closest('table').find('.header-days').hide();
$('.header-table').closest('table').find('tbody').hide();

// $.each(timetables_user, function(index, value) {
//
//   let professor = value.professor;
//
//   $("#cel-"+value.cord).html("<strong>" + value.acronym + "</strong>" + "<br>" + professor);
//   $("#cel-"+value.cord).closest('table').find('.header-days').show();
//   $("#cel-"+value.cord).closest('table').find('tbody').show();
//   // console.log(value.cord);
//   // console.log(value.course);
// });

$('.header-table').closest('table').find('.header-days').hide();
$('.header-table').closest('table').find('tbody').hide();

$.each(timetables_user, function(index, value) {

  let professor = value.professor;

  $("#cel-"+value.cord).html("<strong>" + value.acronym + "</strong>" + "<br>" + professor);
  $("#cel-"+value.cord).closest('table').find('.header-days').show();
  $("#cel-"+value.cord).closest('table').find('tbody').show();
  // console.log(value.cord);
  // console.log(value.course);
});

$(document).ready(function() {
  // console.log(tametables_user)


  $('.header-table').click(function() {
    $(this).find('.icon-minimize').text('-');
    $(this).closest('table').find('.header-days').toggle();
    $(this).closest('table').find('tbody').toggle();
    if ( $(this).closest('table').find('.header-days').is(":visible")) {
      $('html, body').animate({
        scrollTop: $(this).closest('table').offset().top - 100
      }, 600);

    }else{
      $(this).find('.icon-minimize').text('+');
    }
  });
});
//     document.querySelectorAll('.rectangle').forEach(function(rectangle) {
//         rectangle.addEventListener('click', function() {
//             var registrationClassId = this.getAttribute('data-registration-class');
//
//             // Filtrar os registros com base no registration_class_id
//             var filteredData = json_data.filter(function(objeto) {
//                 return objeto.registration_class_id === registrationClassId;
//             });
//
//             // Exibir os resultados filtrados
//             var filteredResultsContainer = document.getElementById('filtered-results');
//             filteredResultsContainer.innerHTML = '';
//
//             filteredData.forEach(function(result) {
//                 var resultElement = document.createElement('div');
//                 resultElement.textContent = JSON.stringify(result);
//                 filteredResultsContainer.appendChild(resultElement);
//             });
//         });
//     });
// });
//
//
//   // function handleRectangleClick(value) {
//   //   // Parse o JSON do atributo jsonData
//   //
//   //
//   //   // Filtra os objetos do JSON com registration_class_id igual ao valor do retângulo clicado
//   //   var objetosFiltrados = jsonData.filter(function(objeto) {
//   //     return objeto.registration_class_id === value;
//   //   });
//   //
//   //   // Faça algo com os objetos filtrados, por exemplo, exibi-los em algum lugar
//   //   console.log(objetosFiltrados);
//   // }
//   //
//   // // Adicione um manipulador de clique aos elementos de retângulo
//   // var rectangles = document.querySelectorAll(".rectangle");
//   //
//   // rectangles.forEach(function(rectangle) {
//   //   rectangle.addEventListener("click", function() {
//   //     var valorDoRetangulo = this.textContent.trim(); // Obtém o valor do retângulo clicado
//   //     handleRectangleClick(valorDoRetangulo); // Chama a função para lidar com o clique
//   //   });
//   // });
//
// //   jsonData.forEach(function(objeto) {
// //     console.log(objeto.registration_class_id);
// // });
//


//
//
//
//     // const classSquares = document.querySelectorAll('.class-square');
//
//   // classSquares.forEach(square => {
//   //   square.addEventListener('click', function() {
//   //     const classId = this.getAttribute('data-class-id');
//   //
//   //     console.log(`Clicou na classe com ID ${classId}`);
//   //   });
//   // });

//
// var timePeriodFilter = 'morning';
//
// // Seu JSON com objetos fictícios
// var seuJSON = [
//     {
//         "id": 1,
//         "registration_class_id": "ClassA",
//         "time_period": "morning",
//         "semester_number": 2,
//         "area_code": 3,
//         "teacher_name": "Teacher Alpha"
//     },
//     {
//         "id": 2,
//         "registration_class_id": "ClassB",
//         "time_period": "morning",
//         "semester_number": 2,
//         "area_code": 3,
//         "teacher_name": "Teacher Beta"
//     },
//     {
//         "id": 3,
//         "registration_class_id": "ClassC",
//         "time_period": "afternoon",
//         "semester_number": 2,
//         "area_code": 3,
//         "teacher_name": "Teacher Gamma"
//     },
//     {
//         "id": 4,
//         "registration_class_id": "ClassD",
//         "time_period": "afternoon",
//         "semester_number": 2,
//         "area_code": 3,
//         "teacher_name": "Teacher Delta"
//     }
// ];
//
// // Use a função 'filter' para filtrar os objetos com base no 'time_period'.
// var objetosFiltrados = seuJSON.filter(function (objeto) {
//     return objeto.time_period === timePeriodFilter;
// });
//
// // 'objetosFiltrados' agora contém apenas os objetos com 'time_period' igual a 'morning'.
// console.log(objetosFiltrados);