var x = '1nbqkbnr/pppppppp/11111111/11111111/11111111/1111111r/PPPPPPPP/RNBQKBNR'
var board = new ChessBoard('board', {
  draggable: true,
  dropOffBoard: 'trash',
  sparePieces: false
});
$('#startBtn').on('click', function() {
    board.position(x)
});
$('#clearBtn').on('click', board.clear);

var moves = ''
var onDrop = function(source, target, piece, newPos, oldPos, orientation) {
  moves = source + '-' + target
  console.log("Source: " + source);
  console.log("Target: " + target);
  console.log("Moves: " + moves);
};
var cfg = {
  draggable: true,
  onDrop: onDrop,
  sparePieces: false
};
var board = new ChessBoard('board', cfg);
// $('#make_move').on('submit', function(event) {
//     event.preventDefault();
//     var my_move = $('#my_move').val();
//     console.log(my_move)
//     var move_data = my_move.serialize()
//     console.log(move_data)
//     $.ajax(("/accounts/home/"), {
//         type: 'POST',
//         data: move_data,
//         context: my_move,
//         success: function(result){
//         }
//     })
//     return false;
// })