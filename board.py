from itertools import chain, cycle

import numpy as np
from line import Line


class Board:
    def __init__(self, defs_rows, defs_cols, colors: dict, data=None):
        self.defs_rows = defs_rows
        self.defs_cols = defs_cols
        self.n_rows = len(defs_rows)
        self.n_cols = len(defs_cols)
        self.colors = colors
        if data is not None:
            self.data = data.copy()
        else:
            self.data = 0xffff * np.ones((self.n_rows, self.n_cols), dtype=int)
        self.rows = []
        self.cols = []
        for y, defs in enumerate(defs_rows):
            l = Line(defs, self.data[y, :], (0, y))
            self.rows.append(l)
        for x, defs in enumerate(defs_cols):
            l = Line(defs, self.data[:, x], (1, x))
            self.cols.append(l)

    def copy(self):
        b = Board(self.defs_rows, self.defs_cols, self.colors, self.data)
        for r1, r2 in zip(self.rows, b.rows):
            r2.dirty = r1.dirty
        for r1, r2 in zip(self.cols, b.cols):
            r2.dirty = r1.dirty
        return b

    def image(self):
        ret = np.zeros((self.n_rows, self.n_cols, 3))
        counts = np.zeros((self.n_rows, self.n_cols))
        for color in self.colors.values():
            mask = 0 != np.bitwise_and(self.data, 1 << color["id"])
            ret[mask, :] += color["val"]
            counts[mask] += 1
        counts *= 255
        ret[:, :, 0] /= counts
        ret[:, :, 1] /= counts
        ret[:, :, 2] /= counts
        return ret

    def calc_dof(self):
        ret = np.zeros((self.n_rows, self.n_cols), dtype=int)
        for color in self.colors.values():
            mask = 0 != np.bitwise_and(self.data, 1 << color["id"])
            ret[mask] += 1
        return sum(sum(ret)) - self.n_rows * self.n_cols

    def is_solved(self, dof):
        return dof == 0

    def set_mask(self, y, x, val):
        if (self.data[y, x] & val) == self.data[y, x]:
            return 0
        if self.data[y, x] & val == 0:
            return -1
        self.data[y, x] &= val
        self.rows[y].dirty = True
        self.cols[x].dirty = True
        return 1

    def next_dirty(self):
        cleans = 0
        lim = self.n_cols + self.n_rows
        for rc in cycle(chain(self.cols, self.rows)):
            if rc.dirty:
                cleans = 0
                yield rc
            else:
                cleans += 1
            if cleans >= lim:
                break

    def find_split_point(self):
        for y in (range(self.n_rows)):
            for x in (range(self.n_cols)):
                d = self.data[y, x]
                if d & (d - 1):
                    return y, x
