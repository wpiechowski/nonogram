from board import Board, fix_defs


def load_dir(vals: list):
    ret = []
    for items in vals:
        temp = []
        for val in items:
            temp.append((1, val))
        temp = fix_defs(temp)
        ret.append(tuple(temp))
    return ret


def load_json(json: dict):
    rows = load_dir(json["ver"])
    cols = load_dir(json["hor"])
    colors = {
        "white": {
            "name": "white",
            "char": ".",
            "val": (255, 255, 255),
            "id": 0,
        },
        "black": {
            "name": "black",
            "char": "x",
            "val": (0, 0, 0),
            "id": 1,
        }
    }
    return Board(rows, cols, colors)
