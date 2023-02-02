from load_xml import fetch_webpbn
import pylab as plt
import time
from solver import solve_full


def main():
    board = fetch_webpbn(21683)
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

    board = solve_full(board, painter)

    end = time.time()
    print("time", end - start)
    painter(board, True)
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()
