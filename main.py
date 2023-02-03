from load_json import load_json
from load_xml import fetch_webpbn
import pylab as plt
import time
from solver import solve_full


def main():
    try:
        # here you give a webpbn.com puzzle number:
        board = fetch_webpbn(31015)

        # uncomment these 2 lines to load the puzzle from a json http://a.teall.info/nonogram/
        # json = {"ver":[[2,2],[3,4],[3,6],[3,7],[3,5],[3,3],[1,4],[2,3],[8],[4,3],[4,6],[4,4],[3,1,2],[3,2,2],[2,1,1]],"hor":[[2,2],[3,4],[3,6],[3,7],[3,5],[3,3],[1,4],[2,3],[8],[4,3],[4,6],[4,2,1],[3,3],[3,4],[2,1,2]]}
        # board = load_json(json)

        solve_board(board, paint=True)
    except:
        raise


def solve_board(board, paint=True):
    plt.ion()
    fig, ax = plt.subplots()
    img = board.image()
    axim = ax.imshow(img)
    start = time.time()
    last = start

    def no_painter(brd, force=False):
        pass

    def painter(brd, force=False):
        nonlocal last
        if not brd:
            return
        now = time.time()
        if force or now - last >= int(now - start > 60):
            last = now
            axim.set_data(brd.image())
            plt.draw()
            fig.canvas.flush_events()

    board = solve_full(board, painter if paint else no_painter)

    end = time.time()
    print("time", end - start)
    painter(board, True)
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()
