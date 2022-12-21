
walk = ['e', 'w', 's', 'n', 'n', 's', 'e', 's', 'e', 'w']

lon = walk.count('n') - walk.count('s')
lat = walk.count('e') - walk.count('w')

if lat < 0:
    lat = (lat + (lat * -2)) 
if lon <  0:
        lon = (lon + (lon * -2))
       
if lat + lon == 0 and len(walk) == 10:
    print(True)
else:
    print(False)

    

print(lat)
