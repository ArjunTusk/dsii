import TruckIt

from datetime import datetime, timedelta

from package import package_items
from package import hasTable

packageTable = package_items.Parse()
recordTable = hasTable.HasTable(40)
packageTable.read_files("WGUPS Package File.csv")

oneTruck = TruckIt.Truck("WGUPS Distance Table.csv", 1)
twoTruck = TruckIt.Truck("WGUPS Distance Table.csv", 2)
threeTruck = TruckIt.Truck("WGUPS Distance Table.csv", 3)

print(packageTable.size())
oneTruck.add(packageTable.bundle_package())
twoTruck.add(packageTable.bundle_package_string("Can"))
threeTruck.add(packageTable.bundle_package_string("Delayed"))
packageTable.remove_it()
a = datetime(1900, 1, 1, 10, 30).strftime("%I:%M %p")
b = []

twoTruck.add(packageTable.return_early_pack(a))

while oneTruck.sizeIt() < 15 and packageTable.size() > 0:
    c = packageTable.return_line()
    if "Wrong address" not in c.get_notes():
        oneTruck.add(c)
    else:
        b.append(c)
gg = []
gg += twoTruck.where_next()
gg += oneTruck.where_next()
threeTruck.set_time(twoTruck.get_time())
gg += threeTruck.where_next()
twoTruck.set_time(threeTruck.get_time())

g = 0

while oneTruck.sizeIt() < 15 and b:
    if "Wrong address" not in b[g].get_notes() and twoTruck.sizeIt() < 16:
        a = twoTruck.add(b[0])
        b.pop(0)
    else:
        oneTruck.add(b[0])
        b.pop(0)

while packageTable.size() > 0:
    oneTruck.add(packageTable.return_line())
gg += oneTruck.where_next()
recordTable.multi_insert(gg)
print("Total miles driven combined:")
print(oneTruck.miles_driven + twoTruck.miles_driven + threeTruck.miles_driven, "\n")

user_inp = input("Welcome! How can we help?\n A: View All Packages\n B:Look Up a Package\n E: Exit")
while user_inp.lower() != "e" :
    if user_inp.lower() == "b":
        user_inp = input(" Please input package id")
        print("Package ID\tAddress\tZipcode\tExpected Delivery Time\tWeight\tActual Delivery Time")
        print(recordTable.search(int(user_inp)).return_all_details())
    elif user_inp.lower() == "a":
        for i in range(1, 40):
            if recordTable.search(i):
                print(recordTable.search(i).return_all_details())
    user_inp = input("Welcome! How can we help?\n A: View All Packages\n B:Look Up a Package\n E: Exit")