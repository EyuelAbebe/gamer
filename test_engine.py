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
        print coord
        assert engine._coord_to_a1.get(coord, False) is False
