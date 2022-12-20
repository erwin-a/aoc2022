import itertools

from utils import lines, Board

FILE = "17"

# for convenience, we are falling upwards
shapes = [Board.from_str(reversed(x)) for x in [
    [
        "####"
    ],
    [
        ".#.",
        "###",
        ".#"
    ],

    [
        "..#",
        "..#",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#,"
    ],
    [
        "##",
        "##"
    ]
]]

WIDTH = 7


def try_move(prev: set, n: Board, dx, dy):
    # can we move this piece in this direction?
    n2 = n.translate(dx, dy)
    # empty space is at 0..W-1, walls at -1 and +W
    if n2.minx < 0 or n2.maxx >= WIDTH or n2.collides_set(prev):
        return False, n
    return True, n2


def sim_cycle(N):
    state = {(x, 0) for x in range(-1, WIDTH + 1)}
    jets = ['<>'.index(x) * 2 - 1 for x in next(lines(FILE))]

    next_jet = itertools.cycle(range(len(jets))).__next__  # save the index into the jet for state hashing
    rocks = itertools.cycle(shapes).__next__

    previous_state = {}  # hash of last N shapes, wind index -> shape index, height
    shape_xpos = []
    heights = []

    n = top = 0
    while n < N:
        shape: Board = rocks()
        shape = shape.translate(dx=2, dy=3 + top + 1)  # 2 away from left edge, 3 space above bottom

        while 1:
            dx = jets[windex := next_jet()]
            _, shape = try_move(state, shape, dx=dx, dy=0)  # jets, ignore failure
            moved, shape = try_move(state, shape, dx=0, dy=-1)  # can we move down?
            if not moved:
                state.update(shape.d.keys())
                heights.append(max(shape.maxy - top, 0))  # relative height differences
                top = max(top, shape.maxy)
                shape_xpos.append(shape.minx)  # X positions for hashing
                break

        hs = tuple(shape_xpos[-25:])  # only last few meaningful for hashing
        try:
            prev_n, prev_top = previous_state[hs, windex]
            cycle_length = n - prev_n
            cycle_height = top - prev_top
            # we have mave rocks leftover after completing the cycles
            cycles_remaining, leftover = divmod(N - n - 1, cycle_length)
            return top + (cycles_remaining * cycle_height) + sum(heights[-cycle_length:][:leftover])
        except KeyError:
            previous_state[hs, windex] = n, top
        n += 1
    return top


def main():
    assert 3149 == sim_cycle(N=2022)
    assert 1553982300884 == sim_cycle(N=1000000000000)


if __name__ == '__main__':
    main()
