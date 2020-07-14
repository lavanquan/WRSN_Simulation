import random


temp = []
for i in range(100):
    r = random.randint(0, 200)
    while r in temp:
        r = random.randint(0, 200)
    temp.append(r)

print(temp)
