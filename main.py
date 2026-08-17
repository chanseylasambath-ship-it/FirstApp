# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('David Sambath; welcome to Python World!')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


## The For Loops
## Loop through list
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)

## Loop with range() Function
for x in range(4):        #output will start with 0 value
    print(x)
for x in range(1,4):        #ignore start with 0 value
    print(x)
for x in range(1,10, 2):       #adding 3rd parameter will increment by 2
    print(x)