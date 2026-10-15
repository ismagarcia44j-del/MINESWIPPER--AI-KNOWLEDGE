l=[69,70,71,72]
"""
print(id(l), id(l[:])) 
l[:]
print(id(l[:]))"""

for num in l:
    print(num)
    if num==71:
        del l[num]
    print(num)
print (l)