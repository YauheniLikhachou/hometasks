# Program to check if a string
#  is palindrome or not

var_str = input("Enter a string: ")
#var_str = "mama"
#var_str = "nagan"

var_str = var_str.casefold()

revers_str = reversed(var_str)

if list(var_str) == list(revers_str):
    print("String is palindrome")
else:
    print("String is NOT palindrome")