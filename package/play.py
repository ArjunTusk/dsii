import practice1
import practice

oneTruck = practice.Truck()
twoTruck = practice.Truck()
threeTruck = practice.Truck()

packageTable = practice1.Parse()
packageTable.readfiles("WGUPS Package File.csv")

oneTruck.add(packageTable.Bundle())
twoTruck.add(packageTable.onlyTruck())
threeTruck.add(packageTable.Bundle2())


while packageTable.size() > 0:
    a = packageTable.size()
    b = [packageTable.returnLine()]
    c = [packageTable.returnLine()]
    d = oneTruck.sizeIt() < 13
    e = twoTruck.sizeIt() < 13
    if d and e:
        oneTruck.add(b)
        twoTruck.add(c)
    elif not d and  e:
        oneTruck.removePackage()
        twoTruck.add(b)
    elif not e:
        twoTruck.removePackage()
        threeTruck.add(b)

    else:
        threeTruck.removePackage()

print(packageTable.size())
print(oneTruck.sizeIt())
