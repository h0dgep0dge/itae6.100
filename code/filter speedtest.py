import sys
sys.path.insert(1, './lib')
from filter import Filter

f = Filter(10)

for a in range(1,50000):
    for b in range(1,1000):
        f.feed(a/b)

print(f.avg())
