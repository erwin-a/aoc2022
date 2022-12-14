from itertools import pairwise

from utils import Board, tokens, Pos


def read():
    b = Board()
    for line in tokens("14"):
        pl = [Pos.from_str(t) for t in line if t != "->"]
        for start, end in pairwise(pl):
            b.draw(start, end)
    return b


sand_paths = Pos(0, +1), Pos(-1, +1), Pos(+1, +1)


def sim(b, pos, bottom_y):
    if pos.y >= bottom_y:
        return None

    for d in sand_paths:
        new = pos + d
        if new not in b:
            return sim(b, new, bottom_y)
    return pos


def main():
    b = read()
    bottom_y = b.maxy

    start = Pos(500, 0)
    while (end := sim(b, start, bottom_y)) is not None:  # None -- fallen below bottom
        b[end] = 'o'
    print(sum(1 for _ in b.find_all('o')))

    b = read()
    b.draw(start=Pos(-1000, b.maxy + 2), end=Pos(b.maxx + 1000, b.maxy + 2))  # abritrary +/- inf
    while (end := sim(b, start, bottom_y + 2)) != start:
        assert end is not None
        b[end] = 'o'

    print(sum(1 for _ in b.find_all('o')))


if __name__ == '__main__':
    main()
