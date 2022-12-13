import dataclasses
import operator
import re
from utils import product

MonkeyRx = re.compile('''Monkey (\d):
.*items: (.+)
.*new = (.+)
.*divisible by (\d+)
\s+If true: throw to monkey (\d+)
\s+If false: throw to monkey (\d+)''', re.MULTILINE)

@dataclasses.dataclass
class Monkey:
    id: int
    items: list[int]
    formula: str
    divisible: int
    true: int
    false: int
    inspections: int = 0

    def __post_init__(self):
        assert self.true != self.id     # sanity check -- can monkeys throw to themselves?
        assert self.false != self.id

    def __str__(self):
        return f'<Monkey {self.id}: { " ".join(str(x) for x in self.items)}>'


def read():
    for s in open("inputs/11.txt").read().split("\n\n"):
        m = MonkeyRx.search(s)
        monkey, items, formula, divisible, true, false = m.groups()
        yield Monkey(id=int(monkey), items=[int(x) for x in items.split(",")], formula=formula,
            divisible=int(divisible), true=int(true), false=int(false))

ops = {
    '*' : operator.mul,
    '+' : operator.add
}
def eval_formula(f, old):
    left, op, right = f.split()

    def eval_token(s):
        if s == 'old': return old
        return int(s)

    left, right = eval_token(left), eval_token(right)
    return ops[op](left, right)

def main(worry_divisor, rounds):
    monkeys = list(read())
    # the worry numbers become huge large numbers quickly, but the only operation we
    # are interested in is N % D where D is each divider. Keep the numbers in range 0...Dp where Dp is th product
    # of all divisors  we are interested in
    # data file knowledge: all unique prime numbers
    master_divisor = product(x.divisible for x in monkeys)  # divider must be in this list

    for round in range(rounds):
        for m in monkeys:
            m.inspections += len(m.items)
            for x in m.items:
                x = (eval_formula(m.formula, old=x) // worry_divisor) % master_divisor
                target = m.true if (x % m.divisible) == 0 else m.false
                monkeys[target].items.append(x)
            m.items = []

    t1, t2, *rest = sorted(monkeys, key= lambda x: x.inspections, reverse=True)
    print (t1.inspections * t2.inspections)

if __name__ == '__main__':
    main(worry_divisor=3, rounds=20)
    main(worry_divisor=1, rounds=10_000)
