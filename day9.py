from itertools import pairwise
from utils import Pos, sign, tokens

Diff = dict(
    R=Pos(+1, 0),
    U=Pos(0, +1),
    L=Pos(-1, 0),
    D=Pos(0, -1)
)

def tail_move(head, tail):
    if (diff := head - tail).absmax() > 1:  # move only if non-adjacent
        return diff.sign()
    return Pos(0, 0)

def read():
    for dir, steps in tokens(9):
        for _ in range(int(steps)):
            yield Diff[dir]

def main(length):
    rope = [Pos(0, 0) for _ in range(length)]
    visited = {rope[-1]}
    for move in read():
        rope[0] += move
        for i, (head, tail) in enumerate(pairwise(rope)):
            rope[i + 1] += tail_move(head, tail)
        visited.add(rope[-1])

    return len(visited)


if __name__ == '__main__':
    assert main(2) == 6026
    assert main(10) == 2273
