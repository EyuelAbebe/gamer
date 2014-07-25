var match_id = $('#progress_board').attr('data-value');

var progress_board = new ChessBoard('progress_board', {
  draggable: false,
  dropOffBoard: 'trash',
  sparePieces: false,

});

var longPoll = function() {
    return $.ajax({
        type: "GET",
        url: "/read_match/",
        data: {'match_id': match_id, 'position':progress_board.position},
        async: true,
        cache: false,
        timeout: 10000,
        success: function(data) {
            if (data.move !== progress_board.position){
                progress_board.position(data.moves);
            }
          return longPoll();
        },
        dataType: 'json'
  });
};

longPoll();





