###
### Day 1 - Python
###

def read():
    entries = [cur := []]
    for line in open("inputs/1.txt"):
        if line := line.strip():
            cur.append(int(line))
        else:
            entries.append(cur := [])
    return entries

def main():
    calories = sorted((sum(x) for x in read()), reverse=True)
    print(calories[0], sum(calories[:3]))

main()

