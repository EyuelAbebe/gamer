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
            board[coord], board[(self.x, self.y)] = self, None
            self.x, self.y = coord
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
            return 'Sb:({},{})'.format(self.x, self.y)
        else:
            return 'Sw:({},{})'.format(self.x, self.y)


class Pawn(SimpleUnit):
    """docstring for Pawn"""
    def __init__(self, coord, color):
        super(Pawn, self).__init__(coord, color)

    def __repr__(self):
        if self.color == 'black':
            return "-1"
        else:
            return "1"


class Knight(SimpleUnit):
    """docstring for Knight"""
    def __init__(self, coord, color):
        super(Knight, self).__init__(coord, color)

    def __repr__(self):
        if self.color == 'black':
            return "-2"
        else:
            return "2"


class Bishop(SimpleUnit):
    """docstring for Bishop"""
    def __init__(self, coord, color):
        super(Bishop, self).__init__(coord, color)

    def __repr__(self):
        if self.color == 'black':
            return "-3"
        else:
            return "3"


class Rook(SimpleUnit):
    """docstring for Rook"""
    def __init__(self, coord, color):
        super(Rook, self).__init__(coord, color)

    def __repr__(self):
        if self.color == 'black':
            return "-4"
        else:
            return "4"


class Queen(SimpleUnit):
    """docstring for Queen"""
    def __init__(self, coord, color):
        super(Queen, self).__init__(coord, color)

    def __repr__(self):
        if self.color == 'black':
            return "-5"
        else:
            return "5"


class King(SimpleUnit):
    """docstring for King"""
    def __init__(self, coord, color):
        super(King, self).__init__(coord, color)

    def __repr__(self):
        if self.color == 'black':
            return "-6"
        else:
            return "6"


class Match(object):
    def __init__(self):
        super(Match, self).__init__()
        self.board = self._create_blank_board()

    def move(self, start_a1, end_a1):
        """Update board with the moved piece if move is valid.

        Accepts algebraic notation.
        """
        start_coord, end_coord = _a1_to_coord[start_a1], _a1_to_coord[end_a1]
        if not self.board[start_coord]:
            raise LookupError("No piece at that location")
        piece = self.board[start_coord]
        self.board = piece.move(end_coord, self.board)

    def _create_blank_board(self):
        board = dict([((x, y), None) for x in xrange(97, 105) for y in xrange(49, 57)])
        return board

    def _add_simple_units(self):
        black = [(x, y) for x in xrange(97, 105) for y in xrange(55, 57)]
        white = [(x, y) for x in xrange(97, 105) for y in xrange(49, 51)]
        for i in black:
            self.board[i] = SimpleUnit(i, 'black')
        for i in white:
            self.board[i] = SimpleUnit(i, 'white')

    def _add_starting_units(self):
        black_units = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        white_units = black_units[::-1]
        for i, unit in enumerate(black_units):
            self.board[(97 + i, 56)] = unit((97 + i, 56), 'black')
            self.board[(97 + i, 55)] = Pawn((97 + i, 55), 'black')
        for i, unit in enumerate(white_units):
            self.board[(97 + i, 49)] = unit((97 + i, 49), 'white')
            self.board[(97 + i, 50)] = Pawn((97 + i, 50), 'white')

if __name__ == "__main__":
    m = Match()
    m._add_starting_units()
