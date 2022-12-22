import operator
from cpmpy import Model, intvar

from utils import lines, tokens


def my_div(a, b):
    "Workaround cmppy bug"
    if isinstance(a, int) and isinstance(a, int):
        return a // b
    else:
        return a / b


ops = {
    '+': operator.add,
    '*': operator.mul,
    '-': operator.sub,
    '/': my_div
}

def read(n):
    resolved, func = {}, {}
    for x in tokens(n):
        name = x[0].rstrip(':')
        if len(x) == 2:
            resolved[name] = int(x[1])  # constant
        else:
            func[name] = ops[x[2]], x[1], x[3]
    return resolved, func


def simplify(func, resolved):
    reduced = False
    for name, (op, left, right) in list(func.items()):
        try:
            resolved[name] = op(resolved[left], resolved[right])
            del func[name]
            reduced = True
        except KeyError as e:
            pass
    return reduced


def main():
    resolved, func = read("21")
    while "root" not in resolved:
        simplify(func, resolved)
    print(resolved["root"])


def main2():
    resolved, func = read("21")
    m = Model()

    func["root"] = operator.eq, *func["root"][1:]
    X = resolved["humn"] = intvar(lb=-2 ** 50, ub=2 ** 50) # manually chosen bounds for the constraint solver

    while "root" not in resolved:
        simplify(func, resolved)

    # in my test case, the target formula is:
    # (sum([119, 389, 2 * (63484871944429 + (-((317 + (3 * (-708 + ((sum([595, -776, 3 * (84 + ((sum([502, -735, 2 * (874 + (34 * (-551 + ((778 + ((582 + (2 * (-264 + (2 * (106 + ((-598 + ((424 + (2 * (-24 + ((sum([491, -575, 2 * (989 + (9 * (-905 + ((663 + (40 * (-940 + ((588 + (2 * (-916 + ((306 + (5 * (26 + ((-227 + ((930 + (2 * (-581 + ((660 + (9 * (-247 + (16 * (-378 + ((903 + (IV0)) / 5)))))) / 3)))) / 2)) / 2)))) / 7)))) / 12)))) / 11))))])) / 2)))) / 2)) / 3)))))) / 5)) / 5))))])) / 9))])) / 4)))) / 2)))])) / 2 == 30328243757936

    m += resolved["root"]
    assert m.solve()

    print(X.value())


if __name__ == '__main__':
    main()
    main2()
