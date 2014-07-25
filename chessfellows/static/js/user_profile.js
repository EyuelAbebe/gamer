

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
    var personal_form = $(event.target);
    var formData = personal_form.serialize()

    $.ajax(("/accounts/updateUserInfo/"),{
        type: 'POST',
        data: formData,
        context: personal_form,
        success: function(result){
            $('#edit_personal_info').hide();
            $('#personal_info').show();
        }

    })

})



$('.gamer').on('click', function(event){
     event.preventDefault();
    var personal_form = $(event.target);
    var formData = personal_form.serialize()

    $.ajax(("/account/join_table"),{
        type: 'POST',
        data: formData,
        context: personal_form,
        success: function(result){

        }

    })

})

$('#edit_player_info').hide();
$('#edit_player_button').on('click', function(){
    $('#player_info').hide();
    $('#edit_player_info').show();

})

$('#profile_info_cancel').on('click', function(){
    $('#player_info').show();
    $('#edit_player_info').hide();

})
$('#save_photo_info').on('submit', function(event){
    event.preventDefault();
    var personal_form = $(event.target);
    var formData = personal_form.serialize()

    $.ajax(("/accounts/updatePlayerInfo/"),{
        type: 'POST',
        data: formData,
        context: personal_form,
        success: function(result){
            $('#edit_player_info').hide();
            $('#player_info').show();
        }

    })

})



$('#signup').on('submit', function(event){
    event.preventDefault();
    var personal_form = $(event.target);
    var formData = personal_form.serialize()

    $.ajax(("/accounts/signUp/"),{
        type: 'POST',
        data: formData,
        context: personal_form,
        success: function(result){

        }

    })

})




var request_game =  function(item){
    alert(item.tagName);

}

$('.player').on('click', request_game);


var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    datasets: [
        {
            label: "Regular",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [2501, 1129, 801, 281, 516, 535, 1120,165, 1129, 1110, 1121, 1116, 1355, 3120]
        },
        {
            label: "Blitz",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [2218, 2118, 2230, 1129, 216, 2127, 2190, 1265, 1259, 2280, 1181, 561, 535, 1232]
        },
        {
            label: "Bullet",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [2100, 2100, 400, 1011, 822, 2111, 1001, 2191, 2311, 400, 1111, 112, 2311, 1001]
        }

    ]
};

var ctx = $("#myChart").get(0).getContext("2d");
var myLineChart = new Chart(ctx).Line(data);


$(document).ready(function () {
$('form input').tooltip({
  placement: 'top',
  trigger: 'focus',
  title: function (){
    return $(this).attr('placeholder');
  }
});
});