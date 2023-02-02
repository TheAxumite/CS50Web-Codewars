def move_zeros(lst):
    count = 0
    while 0 in lst:
        lst.remove(0)
        count = count + 1
    for i in range(count):
        lst.append(0)
    return lst


print(move_zeros( [1, 2, 0, 1, 0, 1, 0, 3, 0, 1]))