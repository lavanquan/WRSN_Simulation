import random


temp = []
for i in range(300):
    r = random.randint(0, 300)
    while r in temp:
        r = random.randint(0, 300)
    temp.append(r)

print(temp)
