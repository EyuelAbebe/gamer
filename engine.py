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
