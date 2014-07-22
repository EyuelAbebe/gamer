# Use x, y coords for unit positions
# (97, 56) ... (104, 56)
#    ...          ...
# (97, 49) ... (104, 49)
#
# Algebraic notation for a position is:
# algebraic_pos = chr(x) + chr(y)

# Accept algebraic as input; ultimately return algebraic
# Use coordinates internally

_coord_to_a1 = dict(
    [((x, y), chr(x) + chr(y)) for x in xrange(97, 105) for y in xrange(49, 57)]
    )
_a1_to_coord = dict(
    [(chr(x) + chr(y), (x, y)) for x in xrange(97, 105) for y in xrange(49, 57)]
    )


def _is_pos_on_board(coord):
    u"""Return True if coordinate is on the board."""
    x, y = coord
    if _coord_to_a1.get((x, y), False):
        return True
    else:
        return False


class Piece(object):
    """Parent class for chess pieces."""
    def __init__(self, pos):
        """Instantiate a piece at a coordinate position."""
        super(Piece, self).__init__()
        if isinstance(pos, str):
            self.x, self.y = _a1_to_coord[pos]
        else:
            self.x, self.y = pos

    def move(self, pos, board):
        if pos in self.possible_moves(board):
            dx, dy = pos
            self.x += dx
            self.y += dy
            board[_coord_to_a1[(self.x, self.y)]]
            return board


class SimpleUnit(Piece):
    """Returns a SimpleUnit to test position/movement basics."""
    def __init__(self, pos, color):
        super(SimpleUnit, self).__init__(pos)
        self.color = color
        self.moves = [(0, 1)]

    def possible_moves(self, board):
        valid_moves = []
        for move in self.moves:
            dx, dy = move
            new_pos = (self.x + dx, self.y + dy)
            if _is_pos_on_board(new_pos):
                alg = _coord_to_a1[new_pos]
                if not board[alg] or (board[alg].color != self.color):
                    valid_moves.append(new_pos)
        return valid_moves

    def __repr__(self):
        if self.color == 'black':
            return 'Sb'
        else:
            return 'Sw'


def _create_blank_board():
    board = dict([(_coord_to_a1[(x, y)], None) for x in xrange(97, 105) for y in xrange(49, 57)])
    return board


def _add_simple_units(board=_create_blank_board()):
    black = [_coord_to_a1[(x, y)] for x in xrange(97, 105) for y in xrange(55, 57)]
    white = [_coord_to_a1[(x, y)] for x in xrange(97, 105) for y in xrange(49, 51)]
    for i in black:
        board[i] = SimpleUnit(i, 'black')
    for i in white:
        board[i] = SimpleUnit(i, 'white')
    return board

start_board = _add_simple_units()


def move():
    """Return a board with the piece moved.

    Accepts algebraic notation.
    """
    pass
