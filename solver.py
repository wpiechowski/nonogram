from board import Board
from line import Line


def solve_single(board: Board, rc: Line):
    hints = rc.fit()
    if not hints[0]:
        return -1
    ret = 0
    for n, val in enumerate(hints):
        if rc.ident[0] == 0:    # row
            y, x = rc.ident[1], n
        else:
            y, x = n, rc.ident[1]
        r = board.set_mask(y, x, val)
        if r == -1:
            return -1
        else:
            ret += r
    return ret


def solve_simple(board: Board, painter):
    for rc in board.next_dirty():
        s = solve_single(board, rc)
        if s == -1:
            return -1
        rc.dirty = False
        if s:
            painter(board)
    return board.calc_dof()


def solve_full(board: Board, painter, trace=None):
    if not trace:
        trace = ""
    print(len(Line.cache), "solve", trace)
    if len(Line.cache) > 2000000:
        Line.cache = {}
    dof = solve_simple(board, painter)
    if board.is_solved(dof):
        return board
    y, x = board.find_split_point()
    brds = []
    for color in board.colors.values():
        val = 1 << color["id"]
        if board.data[y, x] & val:
            b = board.copy()
            b.set_mask(y, x, val)
            dof = solve_simple(b, painter)
            if b.is_solved(dof):
                return b
            if dof > 0:
                brds.append((dof, b, color["id"]))
    brds.sort(key=lambda z: z[0], reverse=False)
    for n, (_, brd, col) in enumerate(brds):
        s = solve_full(brd, painter, trace + str(n))
        if s:
            return s
    return None
