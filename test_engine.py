import engine


VALID_COORDS = [(x, y) for x in xrange(97, 105) for y in xrange(49, 57)]
INVALID_COORDS = [
    (0, 0), (-1, -1),
    (96, 49), (96, 48),
    (105, 49), (104, 48),
    (96, 56), (97, 57),
    (105, 56), (104, 57)
    ]
VALID_A1 = [chr(x) + chr(y) for x in xrange(97, 105) for y in xrange(49, 57)]
INVALID_A1 = ['a0', 'a9', 'h0', 'h9', 'z1', 'z8']
EMPTY_BOARD = dict([((x, y), None) for x in xrange(97, 105) for y in xrange(49, 57)])


def test_coord_to_a1():
    u"""Assert the coord-to-a1 dictionary has only the desired keypairs."""
    for coord in VALID_COORDS:
        assert engine._coord_to_a1.get(coord, False) is not False
    for coord in INVALID_COORDS:
        assert engine._coord_to_a1.get(coord, False) is False


def test_a1_to_coord():
    u"""Assert the a1-to-coord dictionary has only the desired keypairs."""
    for a1 in VALID_A1:
        assert engine._a1_to_coord.get(a1, False) is not False
    for a1 in INVALID_A1:
        assert engine._a1_to_coord.get(a1, False) is False


def test_is_coord_on_board():
    u"""Assert that only valid coords are considered in the board."""
    for coord in VALID_COORDS:
        assert engine._is_coord_on_board(coord) is True
    for coord in INVALID_COORDS:
        assert engine._is_coord_on_board(coord) is False


def test_instantiate_Piece():
    u"""Assert an instance of Piece has the expected attributes."""
    for coord in VALID_COORDS:
        p = engine.Piece(coord)
        assert isinstance(p, engine.Piece)
        assert p.x, p.y == coord


def test_instantiate_SimpleUnit():
    u"""Assert an instance of SimpleUnit has the expected attributes."""
    for color in ['white', 'black']:
        for coord in VALID_COORDS:
            p = engine.SimpleUnit(coord, color)
            assert isinstance(p, engine.SimpleUnit)
            assert p.x, p.y == coord
            assert p.color == color


def test_SimpleUnit_possible_moves_empty_space():
    u"""Assert only valid moves are returned."""
    p = engine.SimpleUnit(VALID_COORDS[0], 'white')
    board = EMPTY_BOARD.copy()
    board[(p.x, p.y)] = p
    assert p.possible_moves(board) == [(p.x, p.y + 1)]


def test_SimpleUnit_possible_moves_into_ally():
    u"""Assert moves into allied units are not in returned move list."""
    p = engine.SimpleUnit(VALID_COORDS[0], 'white')
    q = engine.SimpleUnit(VALID_COORDS[1], 'white')
    board = EMPTY_BOARD.copy()
    board[(p.x, p.y)] = p
    board[(q.x, q.y)] = q
    assert p.possible_moves(board) == []


def test_SimpleUnit_possible_moves_off_board():
    u"""Assert that moves off the board are not in returned move list."""
    p = engine.SimpleUnit(VALID_COORDS[-1], 'white')
    board = EMPTY_BOARD.copy()
    board[(p.x, p.y)] = p
    assert p.possible_moves(board) == []


def test_SimpleUnit_possible_moves_into_enemy():
    u"""Assert that moves into an enemy unit is in the returned move list."""
    p = engine.SimpleUnit(VALID_COORDS[0], 'white')
    q = engine.SimpleUnit(VALID_COORDS[1], 'black')
    board = EMPTY_BOARD.copy()
    board[(p.x, p.y)] = p
    board[(q.x, q.y)] = q
    assert p.possible_moves(board) == [(p.x, p.y + 1)]