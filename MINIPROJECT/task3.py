#!/usr/bin/python3

num = int(input("Enter number:"))
if num % 2 == 0 and num % 5 == 0:
    print("FizzBuzz")
elif num % 2 == 0:
    print("Fizz")
elif num % 5 == 0:
    print("Buzz")
else:
    print(num)
