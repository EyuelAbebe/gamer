

  $(function () {
    $('#myTab a:first').tab('show');
  })


  function highlight(tag){
      $(tag).addClass("active");
  }

$('#edit_personal_info').hide();
$('#edit_button').on('click', function(){
    $('#personal_info').hide();
    $('#edit_personal_info').show();

})

$('#personal_info_cancel').on('click', function(){
    $('#personal_info').show();
    $('#edit_personal_info').hide();

})

$('#save_personal_info').on('submit', function(event){
    event.preventDefault();


})