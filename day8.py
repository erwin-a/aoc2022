import math
from utils import Board, lines

def scenic(val, path):
    if not path:
        return 0
    for score, tree in enumerate(path):
        if tree >= val:
            break
    return 1 + score


def main():
    board = Board.from_rows(lines(8), int)
    visible = score = 0

    for x, y, cell, row, col in board.iterrc():
        # reverse paths to the left and up for the scenic value
        paths = [row[:x][::-1], row[x + 1:], col[:y][::-1], col[y + 1:]]
        score = max(score, math.prod(scenic(cell, path) for path in paths))
        if any(max(path, default=-1) < cell for path in paths):  # trees can have zero height
            visible += 1

    assert visible == 1546
    assert score == 519064


if __name__ == '__main__':
    main()
