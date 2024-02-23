import TruckIt

from datetime import datetime, timedelta

from package import package_items

packageTable = package_items.Parse()
packageTable.read_files("WGUPS Package File.csv")

oneTruck = TruckIt.Truck("WGUPS Distance Table.csv")
twoTruck = TruckIt.Truck("WGUPS Distance Table.csv")
threeTruck = TruckIt.Truck("WGUPS Distance Table.csv")

print(packageTable.size())
oneTruck.add(packageTable.bundle_package())
twoTruck.add(packageTable.bundle_package_string("Can"))
threeTruck.add(packageTable.bundle_package_string("Delayed"))
packageTable.remove_it()
print("Loop 0")
print(packageTable.size())
a = 0
while twoTruck.sizeIt() < 16 and packageTable.size() > 0 and a == 0:
    a = twoTruck.add(packageTable.return_early_pack(datetime(1900, 1, 1, 10, 30)))

print("Loop 0")

while oneTruck.sizeIt() < 16 and packageTable.size() > 0:
    oneTruck.add(packageTable.return_line())

print(twoTruck.sizeIt())
print(oneTruck.sizeIt())
print(threeTruck.sizeIt())
print(packageTable.size())
print("Truck 2:")
twoTruck.where_next()
print("Truck 1:")
oneTruck.where_next()
print("Truck 3:")
threeTruck.set_time(twoTruck.get_time())
threeTruck.where_next()
twoTruck.set_time(threeTruck.get_time())
print(packageTable.size())

while oneTruck.sizeIt() < 16 and packageTable.size() > 0:
    a = oneTruck.add(packageTable.return_line())

oneTruck.where_next()
print(oneTruck.miles_driven + twoTruck.miles_driven + threeTruck.miles_driven)
