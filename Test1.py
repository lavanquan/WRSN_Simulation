import random


temp = []
nb = 299
for i in range(300):
    r = random.randint(0, nb)
    while r in temp:
        r = random.randint(0, nb)
    temp.append(r)

print(temp)
