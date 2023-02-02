import numpy as np


def can_fit_here(color: int, count: int, cells: np.array):
    if count > len(cells):
        return False
    val = 1 << color
    for n in range(count):
        if not (cells[n] & val):
            return False
    return True


def sum_positives(defs):
    s = 0
    for _, cnt in defs:
        if cnt > 0:
            s += cnt
    return s


class Line:
    cache = {}

    def __init__(self, defs: tuple, cells: np.array, ident=None):
        # defs: ((n_col, count or 0 for variable), no free spaces
        self.defs = defs
        self.cells = cells
        self.ident = ident
        self.calls = 0
        # self.cache = {}
        self.dirty = True

    def __str__(self):
        return str(self.ident)

    def find_certain(self, defs, cells):
        # cache
        # cells - open options
        self.calls += 1
        if not defs:
            return np.zeros((len(cells), ), dtype=int)
        key = defs, tuple(cells)
        if key in self.cache:
            return self.cache[key]
        color, count = defs[0]
        if count == 0:
            hi = len(cells) - sum_positives(defs)
            lo = 0 if len(defs) > 1 else hi
        else:
            hi = count
            lo = count
        ret = cells * 0
        color_val = 1 << color
        for n in range(lo, hi + 1):
            if not can_fit_here(color, n, cells):
                continue
            if n == len(cells):
                sub = color_val
            else:
                sub = self.find_certain(defs[1:], cells[n:])
                if not sub[0]:
                    continue
            ret[:n] = np.bitwise_or(ret[:n], color_val)
            ret[n:] = np.bitwise_or(ret[n:], sub)
        self.cache[key] = ret
        return ret

    def fit(self):
        self.calls = 0
        ret = self.find_certain(self.defs, self.cells)
        # self.cache = {}
        return ret


if __name__ == "__main__":
    defs = (
        (0, 0),
        (1, 0),
        (0, 0),
    )
    x = 255
    cells = np.array([
        2,
        x,
        x,
        x,
        x,
        x,
        2,
    ], dtype=int)
    l = Line(defs, cells)
    c = l.fit()
    print(c, l.calls)
