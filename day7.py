###
### Day 7
###

from collections import defaultdict
from os.path import dirname


def all_parent_dirs(f):
    parents = f.split('/')[:-1]
    for x in range(1 + len(parents)):
        yield '/'.join(parents[:x])


def read():
    files = {}
    dirsizes = defaultdict(int)

    cwd = '/'
    for line in open("inputs/7.txt"):
        match line.strip().split():
            case '$', 'cd', '..':
                cwd = dirname(cwd)
            case '$', 'cd', directory if directory.startswith('/'):
                cwd = directory
            case '$', 'cd', reldir:
                cwd = "%s/%s" % (cwd, reldir)
            case '$', 'ls':
                pass

            # ls output
            case 'dir', name:
                # TBD empty directories don't matter
                pass
            case size, filename:
                files[f"{cwd}/{filename}".lstrip("/")] = int(size)
            case _:
                assert 0

    for f, size in files.items():   # could be simplified, as directories are not listed more than once
        for d in all_parent_dirs(f):
            dirsizes[d] += size
    return dirsizes


def main():
    ds = read()
    print(sum(size for size in ds.values() if size < 100_000))
    needed = 30_000_000 - 70_000_000 + ds['']
    print(next(size for size in sorted(ds.values()) if size >= needed))

if __name__ == '__main__':
    main()
