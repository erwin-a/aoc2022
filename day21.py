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
    while "root" not in resolved:
        for name, (op, left, right) in list(func.items()):
            try:
                resolved[name] = op(resolved[left], resolved[right])
                del func[name]
            except KeyError:
                pass


def main():
    resolved, func = read("21")
    simplify(func, resolved)
    print(resolved["root"])


def main2():
    resolved, func = read("21")
    m = Model()

    func["root"] = (operator.eq, *func["root"][1:])
    X = resolved["humn"] = intvar(lb=-2 ** 50, ub=2 ** 50)  # manually chosen bounds for the constraint solver

    simplify(func, resolved)    # help the solver a bit

    m += resolved["root"]
    assert m.solve()

    print(X.value())


if __name__ == '__main__':
    main()
    main2()
