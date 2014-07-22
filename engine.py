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
