count = [2, 4, 0, 100, 4, 11, 2602, 36]
counter = 0

for i in count:
    if i % 2 == 0:
        counter += 1
        even=i
    if i % 2 != 0:
        counter += -1
        odd = i

if counter > 2:
    print(odd) 
else:
    print(even)
