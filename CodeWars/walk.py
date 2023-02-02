
walk = input("Input coordinates")
print(walk)

lon = walk.count('n') - walk.count('s')
lat = walk.count('e') - walk.count('w')


       
if lat + lon == 0:
    print(True)
else:
    print(False)

    

print(lat)
