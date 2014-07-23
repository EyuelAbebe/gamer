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


def test_coord_to_a1():
    for coord in VALID_COORDS:
        assert engine._coord_to_a1.get(coord, False) is not False
    for coord in INVALID_COORDS:
        assert engine._coord_to_a1.get(coord, False) is False


def test_a1_to_coord():
    for a1 in VALID_A1:
        assert engine._a1_to_coord.get(a1, False) is not False
    for a1 in INVALID_A1:
        assert engine._a1_to_coord.get(a1, False) is False


def test_is_coord_on_board():
    for coord in VALID_COORDS:
        assert engine._is_coord_on_board(coord) is True
    for coord in INVALID_COORDS:
        assert engine._is_coord_on_board(coord) is False


def test_instantiate_Piece():
    for coord in VALID_COORDS:
        p = engine.Piece(coord)
        assert isinstance(p, engine.Piece)
        assert p.x, p.y == coord


def test_instantiate_SimpleUnit():
    for color in ['white', 'black']:
        for coord in VALID_COORDS:
            p = engine.SimpleUnit(coord, color)
            assert isinstance(p, engine.SimpleUnit)
            assert p.x, p.y == coord
            assert p.color == color
