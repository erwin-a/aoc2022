import string


# a-z -> 1..26, A-Z -> 27..52
PRI = {v:k+1 for k, v in enumerate(string.ascii_lowercase + string.ascii_uppercase)}

def read():
    for line in open("inputs/3.txt"):
        yield [PRI[x] for x in line.strip()]



def common_half():
    for x in read():
        left, right = x[:len(x)//2], x[len(x)//2:]      # note that / yields a float
        common, = set(left) & set(right)                # tuple unpack will error if more than one item
        yield common

def common_triple():
    for group in zip(*[iter(read())] * 3):              # zip up copies of same iterator to bunch things up
        common, = set(group[0]) & set(group[1]) & set(group[2])
        yield common

if __name__ == '__main__':
    print (sum(common_half()))
    print (sum(common_triple()))

