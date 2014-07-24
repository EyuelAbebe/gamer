var x = 'rnbqkbnr/pppppppp/11111111/11111111/11111111/11111111/PPPPPPPP/RNBQKBNR';
var board = new ChessBoard('board', {
  draggable: true,
  dropOffBoard: 'trash',
  sparePieces: false
});
$('#startBtn').on('click', function() {
    board.position(x)
});
$('#clearBtn').on('click', board.clear);

var onDrop = function(source, target, piece, newPos, oldPos, orientation) {
  var moves = '',
      oldPosString = '';
  moves = source + '-' + target;
  oldPosString = ChessBoard.objToFen(oldPos);
  console.log("Moves: " + moves);
  console.log("Old position: " + oldPosString);
  console.log("Draggable: " + (board.draggable));
  $.ajax("/game/move/", {
    type: 'POST',
    data: {move: moves, position: oldPosString},
    dataType: 'json'
  }).done(function(data) {
    board.position(data.moves)
  });
};

var cfg = {
  draggable: true,
  onDrop: onDrop,
  sparePieces: false
};

var board = new ChessBoard('board', cfg);
