#!/usr/bin/python3

num = int(input("Enter a three-digit number:"))
if num >= 100 and num <=999:
    n = num // 100
    n1 = num % 10
    if n > n1:
        print("Yes")
    else:
        print("No")
else:
    print("Enter a THREE-DIGIT number >:(")
