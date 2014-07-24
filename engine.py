# Use x, y coords for unit positions
# (97, 56) ... (104, 56)
#    ...          ...
# (97, 49) ... (104, 49)
#
# Algebraic notation for a position is:
# algebraic_pos = chr(x) + chr(y)

# Accept algebraic as input; ultimately return algebraic
# Use coordinates internally
# Refer to coordinate position as 'coord'
# Refer to algebraic position as 'a1'

MIN_X, MAX_X = 97, 104
MIN_Y, MAX_Y = 49, 56
_coord_to_a1 = dict(
    [((x, y), chr(x) + chr(y)) for x in xrange(MIN_X, MAX_X + 1) for y in xrange(MIN_Y, MAX_Y + 1)]
    )
_a1_to_coord = dict(
    [(chr(x) + chr(y), (x, y)) for x in xrange(MIN_X, MAX_X + 1) for y in xrange(MIN_Y, MAX_Y + 1)]
    )
POSITIONS = [(x, y) for y in xrange(MAX_Y, MIN_Y - 1, -1) for x in xrange(MIN_X, MAX_X + 1)]

# Elements of visualization
pieces = u''.join(unichr(9812 + x) for x in range(12))
pieces = u' ' + pieces[:6][::-1] + pieces[6:]
allbox = u''.join(unichr(9472 + x) for x in range(200))
box = [allbox[i] for i in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60)]
(vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus) = box
h3 = hbar * 3
topline = ul + (h3 + nt) * 7 + h3 + ur
midline = wt + (h3 + plus) * 7 + h3 + et
botline = ll + (h3 + st) * 7 + h3 + lr
tpl = u' {0} ' + vbar


def _is_coord_on_board(coord):
    u"""Return True if coordinate is on the board."""


class Piece(object):
    """Parent class for chess pieces."""
    def __init__(self, coord, color):
        """Instantiate a piece at a coordinate position."""
        super(Piece, self).__init__()
        if isinstance(coord, str):
            self.x, self.y = _a1_to_coord[coord]
        else:
            self.x, self.y = coord
        self.color = color

    def move(self, coord, board):
            board[coord], board[(self.x, self.y)] = self, None
            self.x, self.y = coord
        return board


class SimpleUnit(Piece):
    """Returns a SimpleUnit to test position/movement basics."""
    def __init__(self, coord, color):
        super(SimpleUnit, self).__init__(coord, color)
        if color == 'white':
            self.moves = [(0, 1)]
            self.viz = 1
        else:
            self.moves = [(0, -1)]
            self.viz = -1

    def possible_moves(self, board):
        valid_moves = []
        for move in self.moves:
            dx, dy = move
            new_coord = (self.x + dx, self.y + dy)
            if _is_coord_on_board(new_coord):
                if not board[new_coord] or (board[new_coord].color != self.color):
                    valid_moves.append(new_coord)
        return valid_moves

    def __repr__(self):
        if self.color == 'black':
            return 'Sb:({},{})'.format(self.x, self.y)
        else:
            return 'Sw:({},{})'.format(self.x, self.y)


class Pawn(Piece):
    """docstring for Pawn"""
    def __init__(self, coord, color):
        super(Pawn, self).__init__(coord, color)
        if color == 'black':
            self.viz = -1
        else:
            self.viz = 1

    def __repr__(self):
        if self.color == 'black':
            return 'p'
        else:
            return 'P'


class Knight(Piece):
    """docstring for Knight"""
    def __init__(self, coord, color):
        super(Knight, self).__init__(coord, color)
        if color == 'black':
            self.viz = -2
        else:
            self.viz = 2
        self.moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

    def __repr__(self):
        if self.color == 'black':
            return 'n'
        else:
            return 'N'


class Bishop(Piece):
    """docstring for Bishop"""
    def __init__(self, coord, color):
        super(Bishop, self).__init__(coord, color)
        if color == 'black':
            self.viz = -3
        else:
            self.viz = 3
        self.moves = [(x, x) for x in xrange(1, 8)]
        self.moves += [(-x, -x) for x in xrange(1, 8)]

    def __repr__(self):
        if self.color == 'black':
            return 'b'
        else:
            return 'B'


class Rook(Piece):
    """docstring for Rook"""
    def __init__(self, coord, color):
        super(Rook, self).__init__(coord, color)
        if color == 'black':
            self.viz = -4
        else:
            self.viz = 4
        self.moves = [(x, 0) for x in xrange(1, 8)]
        self.moves += [(-x, 0) for x in xrange(1, 8)]
        self.moves += [(0, y) for y in xrange(1, 8)]
        self.moves += [(0, -y) for y in xrange(1, 8)]

    def __repr__(self):
        if self.color == 'black':
            return 'r'
        else:
            return 'R'


class Queen(Piece):
    """docstring for Queen"""
    def __init__(self, coord, color):
        super(Queen, self).__init__(coord, color)
        if color == 'black':
            self.viz = -5
        else:
            self.viz = 5
        self.moves = [(x, y) for x in xrange(1, 8) for y in xrange(1, 8)]
        self.moves += [(-x, -y) for x in xrange(1, 8) for y in xrange(1, 8)]

    def __repr__(self):
        if self.color == 'black':
            return 'q'
        else:
            return 'Q'


class King(Piece):
    """docstring for King"""
    def __init__(self, coord, color):
        super(King, self).__init__(coord, color)
        if color == 'black':
            self.viz = -6
        else:
            self.viz = 6
        self.moves = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]

    def __repr__(self):
        if self.color == 'black':
            return 'k'
        else:
            return 'K'


class Match(object):

    def __init__(self):
        super(Match, self).__init__()
        self.board = self._create_blank_board()
        self.pieces = self.board.viewvalues()

    def move(self, start_a1, end_a1):
        """Update board with the moved piece if move is valid.

        Accepts algebraic notation.
        """
        start_coord, end_coord = _a1_to_coord[start_a1], _a1_to_coord[end_a1]
        if not self.board[start_coord]:
            raise LookupError("No piece at that location")
        piece = self.board[start_coord]
        self.board = piece.move(end_coord, self.board)
        self.view()

    def _create_blank_board(self):
        board = dict([((x, y), None) for x in xrange(MIN_X, MAX_X + 1) for y in xrange(MIN_Y, MAX_Y + 1)])
        return board

    def _add_simple_units(self):
        black = [(x, y) for x in xrange(MIN_X, MAX_X + 1) for y in xrange(MAX_Y - 1, MAX_Y + 1)]
        white = [(x, y) for x in xrange(MIN_X, MAX_X + 1) for y in xrange(MIN_Y, MIN_Y + 2)]
        for i in black:
            self.board[i] = SimpleUnit(i, 'black')
        for i in white:
            self.board[i] = SimpleUnit(i, 'white')

    def _add_starting_units(self):
        black_units = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        white_units = black_units[::-1]
        for i, unit in enumerate(black_units):
            self.board[(MIN_X + i, MAX_Y)] = unit((MIN_X + i, MAX_Y), 'black')
            self.board[(MIN_X + i, MAX_Y - 1)] = Pawn((MIN_X + i, MAX_Y - 1), 'black')
        for i, unit in enumerate(white_units):
            self.board[(MIN_X + i, MIN_Y)] = unit((MIN_X + i, MIN_Y), 'white')
            self.board[(MIN_X + i, MIN_Y + 1)] = Pawn((MIN_X + i, MIN_Y + 1), 'white')

    def _make_square(self):
        square = [[] for i in xrange(8)]
        current_line = 0
        line_count = 0
        for pos in POSITIONS:
            if line_count == 8:
                current_line += 1
                line_count = 0
            if self.board[pos]:
                square[current_line].append(self.board[pos].viz)
            else:
                square[current_line].append(0)
            line_count += 1
        return square

    def _inter(self, *args):
        """Return a unicode string with a line of the chessboard.

        args are 8 integers with the values
            0 : empty square
            1, 2, 3, 4, 5, 6: white pawn, knight, bishop, rook, queen, king
            -1, -2, -3, -4, -5, -6: same black pieces
        """
        assert len(args) == 8
        return vbar + u''.join((tpl.format(pieces[a]) for a in args))

    def _view(self, position):
        yield topline
        yield self._inter(*position[0])
        for row in position[1:]:
            yield midline
            yield self._inter(*row)
        yield botline

    def view(self):
        print "\n".join(self._view(self._make_square()))

    def _match_won(self, color):
        u"""Return True if match has been won."""
        if color == "white":
            color = "black"
        else:
            color = "white"
        return self._checkmate(color)

    def play_in_terminal(self):
        white_move = True
        won = False
        while not won:
            if white_move:
                color = "white"
            else:
                color = "black"
            if self._in_check(color):
                print "{}'s king is in check!".format(color.title())
                piece = self._find_king()
                possible_moves = piece.possible_moves()
            else:
                piece, possible_moves = self._move_from(color)
            start_a1 = _coord_to_a1[(piece.x, piece.y)]
            end_a1 = _coord_to_a1[self._move_to(piece, possible_moves, color)]
            self.move(start_a1, end_a1)
            white_move = not white_move
            won = self._match_won(color)

    def _move_from(self, color):
        prompt = u"{}'s turn to move:\nFrom: ".format(color.title())
        start_coord = _a1_to_coord[raw_input(prompt)]
        while not self.board[start_coord]:
            prompt = u"No unit at that location. Pick again.\nFrom: "
            start_coord = _a1_to_coord[raw_input(prompt)]
        while self.board[start_coord].color != color:
            prompt = u"That's not your unit. Pick again. "
            start_coord = _a1_to_coord[raw_input(prompt)]
        piece = self.board[start_coord]
        possible_moves = piece.possible_moves(self.board)
        if possible_moves == []:
            print u"That peice does not have valid moves. Pick again. "
            return self._move_from(color)
        return piece, possible_moves

    def _move_to(self, piece, possible_moves, color):
        a1_moves = " ".join([_coord_to_a1[x] for x in possible_moves])
        prompt = u"Move {} to {}: ".format(piece, a1_moves)
        end_coord = _a1_to_coord[raw_input(prompt)]
        while end_coord not in possible_moves:
            prompt = [u"That's not a valid move for this unit."]
            prompt.append([u"Move {} to {}: ".format(piece, a1_moves)])
            prompt = "\n".join(prompt)
            end_coord = _a1_to_coord[raw_input(prompt)]
        return end_coord

    def _in_check(self, color):
        # Locate the king of the given color
        moves = set()
        for piece in self.pieces:
            if piece is not None:
                if piece.color != color:
                    for move in piece.possible_moves(self.board):
                        moves.add(move)
                if isinstance(piece, King) and (piece.color == color):
                    king_coord = (piece.x, piece.y)
        # If king's position is in the list of possible moves -> return True
        if king_coord in moves:
            return True
        else:
            return False

    def _checkmate(self, color):
        king = self._find_king(color)
        if self._in_check(color) and king.possible_moves == []:
            return True
        else:
            return False

    def _find_king(self, color):
        for piece in self.pieces:
            if piece is not None:
                if isinstance(piece, King) and (piece.color == color):
                    king = piece
                    break
        return king

    def _board_to_str(self):
        square = []
        for i, pos in enumerate(POSITIONS):
            if (i != 0) and (i % 8 == 0):
                square.append("/")
            if self.board[pos]:
                square.append(str(self.board[pos]))
            else:
                square.append('1')
        return "".join(square)

    def _str_to_board(self, str_):
        units = {
            'r': Rook,
            'n': Knight,
            'b': Bishop,
            'q': Queen,
            'k': King,
            'p': Pawn,
            '1': None
        }
        board = {}
        str_ = str_.replace("/", "")
        for i, pos in enumerate(POSITIONS):
            unit = units[str_[i].lower()]
            if unit is not None:
                if str_[i].isupper():
                    color = 'white'
                else:
                    color = 'black'
                board[pos] = units[str_[i].lower()](pos, color)
            else:
                board[pos] = None
        return board

    def _play_web(self, board, move, white_move):
        u"""Return a valid board state in string form.

        Inputs
        board: A 71 character string representing a board state.
        move: A 5 character string representing a from and to position.
        white_move: A boolean indicating if it's the white player's move.

        Return a 71 character string representing a board state. The initial
        board state will be returned if the move was invalid.
        """
        if white_move:
            color = "white"
        else:
            color = "black"
        self.board = self._str_to_board(board)
        move_from, move_to = _a1_to_coord[move[0:2]], _a1_to_coord[move[3:]]
        if self._validate_move_from(move_from, color):
            piece = board[move_from]
            if self._vaidate_move_to(piece, move_to):
                self.board = piece.move(move_to, self.board)
        return self._board_to_str(), self._match_won(color)

    def _validate_move_from(self, move_from, color):
        u"""Return True if a piece of the player's color is at move_from."""
        piece = self.board[move_from]
        if piece:
            if piece.color == color and piece.possible_moves(self.board):
                return True
        return False

    def _validate_move_to(self, piece, move_to):
        u"""Return True if the pice can move to the move_to position."""
        moves = piece.possible_moves(self.board)
        if move_to in moves:
            return True
        return False

if __name__ == "__main__":
    m = Match()
    m._add_starting_units()
    # m.view()
    # m.play_in_terminal()
    str_ = m._board_to_str()
    new_board = m._str_to_board(str_)
