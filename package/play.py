

import bundle_add
import TruckIt

packageTable = bundle_add.Parse()
packageTable.read_files("WGUPS Package File.csv")

oneTruck = TruckIt.Truck("WGUPS Distance Table.csv")
twoTruck = TruckIt.Truck("WGUPS Distance Table.csv")
threeTruck = TruckIt.Truck("WGUPS Distance Table.csv")

oneTruck.add(packageTable.bundle_package())
twoTruck.add(packageTable.bundle_package_string("Can"))
threeTruck.add(packageTable.bundle_package_string("Delayed"))
packageTable.remove_it()
a = packageTable.size()
s = 1
while a > 0:
    b = [packageTable.return_line()]
    c = [packageTable.return_line()]
    d = oneTruck.sizeIt() > 10
    e = twoTruck.sizeIt() > 10
    h = oneTruck.sizeIt()
    u = twoTruck.sizeIt()
    oil = threeTruck.sizeIt()
    if not d or not e:
        oneTruck.add(b)
        twoTruck.add(c)
    if d and not e:
        print("Delivery", s)
        twoTruck.add(b)
        v = oneTruck.currentHaul
        oneTruck.findTheAdresses(v)
        oneTruck.removePackage()
        twoTruck.add(b)
    if e:
        print("Delivery 2   ")
        twoTruck.findTheAdresses(twoTruck.currentHaul)
        twoTruck.removePackage()
        threeTruck.add(b)
    if oil :
        threeTruck.removePackage()

    a = packageTable.size()
