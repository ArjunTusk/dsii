from datetime import datetime, timedelta

import bundle_add
import TruckIt

from datetime import datetime, timedelta

packageTable = bundle_add.Parse()
packageTable.read_files("WGUPS Package File.csv")

oneTruck = TruckIt.Truck("WGUPS Distance Table.csv")
twoTruck = TruckIt.Truck("WGUPS Distance Table.csv")
threeTruck = TruckIt.Truck("WGUPS Distance Table.csv")

oneTruck.add(packageTable.bundle_package())
twoTruck.add(packageTable.bundle_package_string("Can", 6))
threeTruck.add(packageTable.bundle_package_string("Delayed", 6))

packageTable.remove_it()
a = packageTable.size()
threeTruckTime = datetime(2024, 2, 15, 9, 5)
threeTruck.set_time(threeTruckTime)
while a > 10:
    print("Truck 1:")
    while oneTruck.sizeIt() < 10 < packageTable.size():
        oneTruck.add(packageTable.return_line())
    oneTruck.wherenext(oneTruck.currentHaul)
    oneTruck.removePackage()
    print("Truck 2:")
    while twoTruck.sizeIt() < 10:
        twoTruck.add(packageTable.return_line())

    twoTruck.wherenext(twoTruck.currentHaul)

    twoTruck.removePackage()

    if threeTruck.sizeIt() > 0:
        print("Truck 3:")
        threeTruck.set_time(twoTruck.get_time())
        threeTruck.wherenext(threeTruck.currentHaul)
        threeTruck.removePackage()
        oneTruck.add(packageTable.bundle_package_string("Wrong", 6))
    a = packageTable.size()
