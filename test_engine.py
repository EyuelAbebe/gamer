import engine
import pytest


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
MIN_X, MAX_X = 97, 104
MIN_Y, MAX_Y = 49, 56


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


def test_assert_SimpleUnit_moving_into_empty_space():
    u"""Assert moving into empty space returns a board with unit moved."""
    p = engine.SimpleUnit(VALID_COORDS[0], 'white')
    board = EMPTY_BOARD.copy()
    new_board = p.move(VALID_COORDS[1], board)
    assert new_board[VALID_COORDS[0]] is None
    assert new_board[VALID_COORDS[1]] is p


def test_SimpleUnit_moving_into_ally():
    u"""Assert moving into allied units do not return a board."""
    p = engine.SimpleUnit(VALID_COORDS[0], 'white')
    q = engine.SimpleUnit(VALID_COORDS[1], 'white')
    board = EMPTY_BOARD.copy()
    board[(p.x, p.y)] = p
    board[(q.x, q.y)] = q
    new_board = p.move(VALID_COORDS[1], board)
    assert new_board == board


def test_SimpleUnit_moving_off_board():
    u"""Assert moving off the board do not return a board."""
    p = engine.SimpleUnit(VALID_COORDS[-1], 'white')
    board = EMPTY_BOARD.copy()
    board[(p.x, p.y)] = p
    new_board = p.move((105, 56), board)
    assert new_board == board


def test_SimpleUnit_moving_into_enemy():
    u"""Assert moving into an enemy unit returns a board with unit moved."""
    p = engine.SimpleUnit(VALID_COORDS[0], 'white')
    q = engine.SimpleUnit(VALID_COORDS[1], 'black')
    board = EMPTY_BOARD.copy()
    board[(p.x, p.y)] = p
    board[(q.x, q.y)] = q
    new_board = p.move(VALID_COORDS[1], board)
    assert new_board[VALID_COORDS[0]] is None
    assert new_board[VALID_COORDS[1]] is p


def test_instantiate_Match():
    u"""Assert an instance of Match has the expected attributes."""
    m = engine.Match()
    assert isinstance(m, engine.Match)
    assert m.board == dict([((x, y), None) for x in xrange(97, 105) for y in xrange(49, 57)])


def test_add_simple_units_to_Match():
    u"""Assert simple units are added to only the top and bottom two rows."""
    m = engine.Match()
    m._add_simple_units()
    for coord in [(x, y) for x in xrange(97, 105) for y in xrange(55, 57)]:
        assert isinstance(m.board[coord], engine.SimpleUnit)
        assert m.board[coord].color == 'black'
    for coord in [(x, y) for x in xrange(97, 105) for y in xrange(49, 51)]:
        assert isinstance(m.board[coord], engine.SimpleUnit)
        assert m.board[coord].color == 'white'
    for coord in [(x, y) for x in xrange(97, 105) for y in xrange(51, 55)]:
        assert m.board[coord] is None


def test_move_unit_in_Match_to_valid_a1():
    u"""Assert moving via Match to a valid pos maintains proper board state."""
    m = engine.Match()
    m._add_simple_units()
    p = m.board[VALID_COORDS[1]]
    m.move('a2', 'a3')
    assert m.board[VALID_COORDS[1]] is None
    assert m.board[VALID_COORDS[2]] is p


def test_move_unit_in_Match_no_unit_at_start_a1():
    u"""Assert moving a unit from an empty location raises LookupError."""
    m = engine.Match()
    m._add_simple_units()
    with pytest.raises(LookupError):
        m.move('a4', 'a5')


def test_move_unit_in_Match_to_enemy_a1():
    u"""Assert moving to an enemy unit maintains proper board state."""
    m = engine.Match()
    m._add_simple_units()
    q = engine.SimpleUnit((97, 51), 'black')
    m.board[(97, 51)] = q
    p = m.board[VALID_COORDS[1]]
    assert q in m.board.values()
    m.move('a2', 'a3')
    assert m.board[VALID_COORDS[1]] is None
    assert m.board[VALID_COORDS[2]] is p
    assert q not in m.board.values()


def test_move_unit_via_Match_into_ally_a1():
    u"""Assert moving via Match to an ally pos does not update board state."""
    m = engine.Match()
    m._add_simple_units()
    p = m.board[VALID_COORDS[0]]
    q = m.board[VALID_COORDS[1]]
    m.move('a1', 'a2')
    assert m.board[VALID_COORDS[0]] is p
    assert m.board[VALID_COORDS[1]] is q
