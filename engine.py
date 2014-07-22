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

_coord_to_a1 = dict(
    [((x, y), chr(x) + chr(y)) for x in xrange(97, 105) for y in xrange(49, 57)]
    )
_a1_to_coord = dict(
    [(chr(x) + chr(y), (x, y)) for x in xrange(97, 105) for y in xrange(49, 57)]
    )


def _is_coord_on_board(coord):
    u"""Return True if coordinate is on the board."""
    x, y = coord
    if _coord_to_a1.get((x, y), False):
        return True
    else:
        return False


class Piece(object):
    """Parent class for chess pieces."""
    def __init__(self, coord):
        """Instantiate a piece at a coordinate position."""
        super(Piece, self).__init__()
        if isinstance(coord, str):
            self.x, self.y = _a1_to_coord[coord]
        else:
            self.x, self.y = coord

    def move(self, coord, board):
        if coord in self.possible_moves(board):
            self.x, self.y = coord
            board[coord] = self
            return board


class SimpleUnit(Piece):
    """Returns a SimpleUnit to test position/movement basics."""
    def __init__(self, coord, color):
        super(SimpleUnit, self).__init__(coord)
        self.color = color
        self.moves = [(0, 1)]

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
            return 'Sb'
        else:
            return 'Sw'


def _create_blank_board():
    board = dict([((x, y), None) for x in xrange(97, 105) for y in xrange(49, 57)])
    return board


def _add_simple_units(board=_create_blank_board()):
    black = [(x, y) for x in xrange(97, 105) for y in xrange(55, 57)]
    white = [(x, y) for x in xrange(97, 105) for y in xrange(49, 51)]
    for i in black:
        board[i] = SimpleUnit(i, 'black')
    for i in white:
        board[i] = SimpleUnit(i, 'white')
    return board


def move(board, start_a1, end_a1):
    """Return a board with the piece moved.

    Accepts algebraic notation.
    """
    start_coord, end_coord = _a1_to_coord[start_a1], _a1_to_coord[end_a1]
    if not board[start_coord]:
        raise LookupError("No piece at that location")
    piece = board[start_coord]
    return piece.move(end_coord, board)


if __name__ == "__main__":
    start_board = _add_simple_units()
