#!/usr/bin/python3

n1 = int(input("Enter number:"))
n2 = int(input("Enter number:"))
n3 = int(input("Enter number:"))
#num = [n1, n2, n3]
#num.sort()
#print(num[0], num[1], num[2])

if n1 <= n2 and n1 <= n3:
    if n2 <= n3:
        print(n1, n2 ,n3)
    else:
        print(n1, n3, n2)
elif n2 <= n1 and n2 <= n3:
    if n1 <= n3:
        print(n2, n1, n3)
    else:
        print(n2, n3, n1)
elif n3 <= n1 and n3 <= n2:
    if n2 <= n1:
        print(n3, n2, n1)
    else:
        print(n3, n1, n2)
    
