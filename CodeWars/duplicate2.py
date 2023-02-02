lst="22222222225dcP1f9KcS8dUQSTldDXypEIeNf1NTri9U3enKAMy name is leul"
list = []
list_2 = []
for l in lst:
    array = {}
    array[l] = lst.count(l)
    list.append(array)
for dic in list:
    for key, value in dic.items():
        if value > 1 and key is not ' ' and dic not in list_2:
            list_2.append(dic)
print(lst)
print(list_2)          
print(len(list_2))
