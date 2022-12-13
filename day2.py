##
### Day 2 - Python 3.11
##
# A-Rock B-Paper C-Scissors
scores = (
    (3, 6, 0),
    (0, 3, 6),
    (6, 0, 3)
)


def read():
    for line in open("inputs/2.txt"):
        opp, you = line.strip().split()
        yield "ABC".index(opp), "XYZ".index(you)


def strategy_literal(opp, you):
    "XYZ translate to ABC"
    return you


def strategy_outcome(opp, outcome):
    "XYZ translate to wanted loss/draw/win"
    wanted = [0, 3, 6][outcome]
    return scores[opp].index(wanted)


def main(strategy):
    print(sum(scores[opp][strategy(opp, you)] + 1 + strategy(opp, you) for opp, you in read()))


if __name__ == '__main__':
    main(strategy=strategy_literal)
    main(strategy=strategy_outcome)
