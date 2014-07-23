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
        if color == 'white':
            self.moves = [(0, 1)]
        else:
            self.moves = [(0, -1)]

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
        if color == 'black':
            self.viz = -1
        else:
            self.viz = 1

    def __repr__(self):
        if self.color == 'black':
            return 'Pb:({},{})'.format(self.x, self.y)
        else:
            return 'Pw:({},{})'.format(self.x, self.y)


class Knight(SimpleUnit):
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
            return 'Kb:({},{})'.format(self.x, self.y)
        else:
            return 'Kw:({},{})'.format(self.x, self.y)


class Bishop(SimpleUnit):
    """docstring for Bishop"""
    def __init__(self, coord, color):
        super(Bishop, self).__init__(coord, color)
        if color == 'black':
            self.viz = -3
        else:
            self.viz = 3

    def __repr__(self):
        if self.color == 'black':
            return 'Bb:({},{})'.format(self.x, self.y)
        else:
            return 'Bw:({},{})'.format(self.x, self.y)


class Rook(SimpleUnit):
    """docstring for Rook"""
    def __init__(self, coord, color):
        super(Rook, self).__init__(coord, color)
        if color == 'black':
            self.viz = -4
        else:
            self.viz = 4

    def __repr__(self):
        if self.color == 'black':
            return 'Rb:({},{})'.format(self.x, self.y)
        else:
            return 'Rw:({},{})'.format(self.x, self.y)


class Queen(SimpleUnit):
    """docstring for Queen"""
    def __init__(self, coord, color):
        super(Queen, self).__init__(coord, color)
        if color == 'black':
            self.viz = -5
        else:
            self.viz = 5

    def __repr__(self):
        if self.color == 'black':
            return 'Qb:({},{})'.format(self.x, self.y)
        else:
            return 'Qw:({},{})'.format(self.x, self.y)


class King(SimpleUnit):
    """docstring for King"""
    def __init__(self, coord, color):
        super(King, self).__init__(coord, color)
        if color == 'black':
            self.viz = -6
        else:
            self.viz = 6

    def __repr__(self):
        if self.color == 'black':
            return 'Kb:({},{})'.format(self.x, self.y)
        else:
            return 'Kw:({},{})'.format(self.x, self.y)


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

    def _make_square(self):
        positions = [(x, y) for y in xrange(56, 48, -1) for x in xrange(97, 105)]
        square = [[] for i in xrange(8)]
        current_line = 0
        line_count = 0
        for pos in positions:
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


if __name__ == "__main__":
    m = Match()
    m._add_starting_units()
    m.view()
    m.play_in_terminal()
