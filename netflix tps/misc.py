temperatures = [73,74,75,71,69,72,76,73]
for i,t in enumerate(temperatures[1:]):
    print(t,i)

import heapq

h = [(1, 'one'), (3, 'three'), (2, 'two')]


heapq.heapify(h)

a = sorted(h, key=lambda x: x[1])
b = h.sort(key=lambda x: x[1])


print(a)
print(b)
print(h)

