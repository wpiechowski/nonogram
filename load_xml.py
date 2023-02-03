import requests
import xml.etree.ElementTree as ET

from board import Board, fix_defs


def parse_line(root, colors, default_color, ident=None) -> list:
    defs = []
    for item in root.iter("count"):
        color = item.attrib.get("color", default_color)
        count = int(item.text)
        defs.append((colors[color]["id"], count))
    defs = fix_defs(defs)
    return defs


def parse_color(text):
    r = int(text[:2], 16)
    g = int(text[2:4], 16)
    b = int(text[4:], 16)
    return r, g, b


def parse_puzzle(root):
    colors = {}
    default_color = root.attrib["defaultcolor"]
    color_id = 1
    for color in root.iter("color"):
        ch = color.attrib["char"]
        c = {
            "name": color.attrib["name"],
            "char": ch,
            "val": parse_color(color.text),
            "id": 0 if ch == "." else color_id,
        }
        if ch != ".":
            color_id += 1
        colors[c["name"]] = c
    rows = []
    cols = []
    for clue in root.iter("clues"):
        row_col = clue.attrib["type"] == "columns"
        target = cols if row_col else rows
        for line in clue.iter("line"):
            ident = row_col, len(target)
            l = parse_line(line, colors, default_color, ident)
            target.append(tuple(l))
    return Board(rows, cols, colors)


def parse_xml(text):
    root = ET.fromstring(text)
    for p in root.iter("puzzleset"):
        for pp in p.iter("puzzle"):
            return parse_puzzle(pp)


def fetch_webpbn(num):
    data = {"go": 1, "id": num, "xml_clue": "on", "fmt": "xml", "xml_soln": "on"}
    url = "https://webpbn.com/export.cgi/webpbn%06i.sgriddler" % num
    text = requests.post(url, data).text
    print(url, data)
    # print(text)
    try:
        print("fetched")
        return parse_xml(text)
    except:
        print(text)
        raise


if __name__ == "__main__":
    fetch_webpbn(19427)
