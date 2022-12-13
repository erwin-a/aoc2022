import itertools
import operator

from utils import tokens


def read():
    for line in tokens(10):
        match line:
            case "addx", inc:
                yield 0
                yield int(inc)
            case "noop",:
                yield 0


def main():
    xvals = list(itertools.accumulate(read(), operator.add, initial=1))
    W = 40

    assert 15220 == sum(cycle * x for cycle, x in enumerate(xvals, start=1)
              if (cycle - 20) % W == 0)

    for start in range(0, 240, W):
        print(''.join(
            "#" if (abs(xvals[ip] - (ip % W)) <= 1) else "."  # sprite centered at, before or after our x
            for ip in range(start, start + W)
        ))


if __name__ == '__main__':
    main()
