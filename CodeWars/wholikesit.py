import sys
names = ["Alex", "Jacob", "Mark", "Max"]
if not in names < 1:
    print("no one likes this")
if len(names) == 1:
    print(names[0] + " " + "likes this")
if len(names) == 2:
    print(names[0] + "and" + " " + names[1] + " " + "likes this")
if len(names) == 3:
    print(names[0] + names[1] + " " + "and" + " " + names[1] + " " + "likes this")
if len(names) > 3:
    print(f"{names[0]} , {names[1]}, and {len(names) - 2} likes this ")