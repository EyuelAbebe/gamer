# Use x, y coords for unit positions
# (97, 56) ... (104, 56)
#    ...          ...
# (97, 49) ... (104, 49)
#
# Algebraic notation for a position is:
# algebraic_pos = chr(x) + chr(y)


def _coord_to_algebraic(coord):
    x, y = coord
    return chr(x) + chr(y)


def _algebraic_to_coord(algebraic):
    x, y = algebraic[0], algebraic[1]
    return ord(x), ord(y)


def _is_pos_on_board(coord):
    u"""Return True if coordinate is on the board."""
    x, y = coord
    if (97 <= x <= 104) and (49 <= y <= 56):
        return True
    else:
        return False


class Piece(object):
    """Parent class for chess pieces."""
    def __init__(self, pos):
        """Instantiate a piece at a coordinate position."""
        super(Piece, self).__init__()
        if isinstance(pos, str):
            self.x, self.y = _algebraic_to_coord(pos)
        else:
            self.x, self.y = pos

    def move(self, pos, board):
        if pos in self.possible_moves(board):
            dx, dy = pos
            self.x += dx
            self.y += dy
            board[_coord_to_algebraic((self.x, self.y))]
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
                if not board[new_pos] or (board[new_pos].color != self.color):
                    valid_moves.append(new_pos)
        return valid_moves
