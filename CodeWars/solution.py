number = 200
i = 1
solution = 0

while i < number:
    if (i % 3 == 0) or (i % 5 == 0):
        solution = i + solution
        i += 1
    else:
        i += 1

print(solution)  

