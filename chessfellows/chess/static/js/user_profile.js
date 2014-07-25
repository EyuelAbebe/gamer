

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

    $.ajax(("/updateUserInfo/"),{
        type: 'POST',
        data: formData,
        context: personal_form,
        success: function(result){
            $('#edit_personal_info').hide();
            $('#personal_info').show();
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

    $.ajax(("/updatePlayerInfo/"),{
        type: 'POST',
        data: formData,
        context: personal_form,
        success: function(result){
            $('#edit_player_info').hide();
            $('#player_info').show();
        }

    })

})




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
            data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
            label: "Blitz",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90]
        },
        {
            label: "Bullet",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [21, 21, 4, 11, 82, 21, 11]
        }

    ]
};

//var ctx = $("#myChart").get(0).getContext("2d");

//var myLineChart = new Chart(ctx).Line(data);


var set_myLineChart =  function(){
    var ctx, chart ,LineChart;
    chart = $("#myChart");
    if (chart.length > 0){
        ctx = chart.get(0).getContext("2d");
        LineChart =  new Chart(ctx).Line(data);
    }
    if (LineChart !== undefined){
        return LineChart;

    }
    else{
        return null;
    }

}
  var myLineChart = set_myLineChart();

$(document).ready(function () {
$('form input').tooltip({
  placement: 'top',
  trigger: 'focus',
  title: function (){
    return $(this).attr('placeholder');
  }
});
});