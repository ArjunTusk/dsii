import TruckIt

from datetime import datetime

from package import package_items


# main_py
# student_id: 011284767

# Process: Prompts the user for a time. Either prints all packages by delivery deadline or actual delivery time.
# Prints table headers Flow: Method accepts an option. User inputs a time. Program checks if time is valid. If option
# == d then prints by actual delivery time Flow: Else prints by delivery deadline. Prints total packages delivered.
# If no packages found prints error message.
def get_time(time):
    amnt_fnd = 0
    while True:
        user_input = input(" Please enter time:").strip()
        try:
            time_object = datetime.strptime(user_input, "%I:%M %p")
            break
        except ValueError as e:
            print(" Error! Try again!")
    table_headers()
    if time == 'd':
        time_object = datetime.strptime(user_input, "%I:%M %p")
        for x in range(1, 41):
            if datetime.strptime(packageTable.pack_table.search(x).get_delivered(), "%I:%M %p") == time_object:
                packageTable.pack_table.search(x).set_delivery_status("DELIVERED")
                packageTable.return_item(x).return_all_details()
                amnt_fnd += 1
    else:
        time_object = datetime.strptime(user_input, "%I:%M %p")
        for v in range(1, 41):
            if datetime.strptime(packageTable.return_item(v).get_delivery_deadline(), "%I:%M %p") == time_object:
                packageTable.return_item(v).set_delivery_status("DELIVERED")
                packageTable.return_item(v).return_all_details()
                amnt_fnd += 1
    if amnt_fnd == 0:
        print("Sorry! No packages were delivered at the time you inputted.")
    else:
        print("\n# ", amnt_fnd, " were delivered")


# Process: Checks if string is int
# Flow: Accepts string. Prompts suer w/ string Collects user input. Try's to convert string input to int.
# Flow: If it fails it calls the method again
def is_int(user_prompt):
    user_input = input(user_prompt)
    user_int = 0
    try:
        user_int = int(user_input)
    except ValueError as e:
        print("Error. Try again!")
        user_int = is_int(user_prompt)
    return user_int


# Process: Prints headers for table and separation lines
# Flow formats the string args, so they are centered and occupies 25pt cells.
def table_headers():
    print("{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}".format("Address", "Delivery Deadline", "City",
                                                                    "Zipcode", "Weight", "Delivery Status",
                                                                    "Actual or Expected Delivery Time"))
    print((" " * 7) + '-' * 170)


# Process: Prompts for user input with string. Calls option again if input invalid
# Flow : Prompts for user_input using string. If user_input is not a letter then the method is called again
# Flow : Returns the user input
def menu_options():
    user_input = input("Welcome! How can we help?\n A: View All Packages\n"
                       " B: Look Up A Package\n C: Search Packages By Delivery Deadline"
                       "\n D: Search Packages By Actual Or Expected Delivery Time \n E: Exit\n"
                       " F: Search Packages BY Delivery Truck\n")
    while not user_input.isalpha():
        print("Error! Please enter a valid menu option:")
        user_input = menu_options()
    return user_input


# Loads the csv file into the has table
packageTable = package_items.Parse()
packageTable.read_files("WGUPS Package File.csv")
package_history = set()

# Creates the three truck objects, labels them, and adds the distance csv to each
oneTruck = TruckIt.Truck("WGUPS Distance Table.csv", 1)
twoTruck = TruckIt.Truck("WGUPS Distance Table.csv", 2)
threeTruck = TruckIt.Truck("WGUPS Distance Table.csv", 3)

# Segregates the package objects with special constraints
wrong_address = packageTable.bundle_package_string("Wrong", threeTruck.get_time())
threeTruck.add(packageTable.bundle_package_string("Delayed", threeTruck.get_time()))
twoTruck.add(packageTable.bundle_package_string("Can", twoTruck.get_time()))
twoTruck.add(packageTable.bundle_package(twoTruck.get_time()))

# Process: Updates the set package history to contain which packages have been delivered by truck 2
package_history.update(twoTruck.where_next())

# Process: Iterates through packageTable. Removes the first item in packageTable. Stores it in next_package. 
# Process: Adds it to towTruck if it's delivery deadline is 11:59 PM. Else adds it to oneTruck
# Process: Sets each packages' pickup time to when the trucks arrived at the HUB

# Flow: Iterate while twoTruck's current Haul is less than 16 and packageTable still has packages. 
# Flow: Grab first available package. If package deadline == 11:59 PM add to twoTruck. Else add to oneTruck
# Flow: Set each packages pick_up to the time the truck is at the HUB

while twoTruck.sizeIt() < 16 and packageTable.size() > 0:
    next_package = packageTable.return_line()
    if next_package.get_delivery_deadline() == "11:59 PM":
        next_package.set_pickup(twoTruck.get_time())
        twoTruck.add(next_package)
    else:
        next_package.set_pickup(oneTruck.get_time())
        oneTruck.add(next_package)

# Process: Send oneTruck and twoTruck back on the road. Update package_history with what has happened to the packages
# Process: Update threeTruck with new datetime.
# Flow: Call where_next() to run the distance calculations and time stamp the packages with their delivery times
# Flow: Add the now updated packages to package_history.
# Flow: Set threeTruck's time to 9:06 AM as threeTruck will be delivering the delayed packages
package_history.update(twoTruck.where_next())
package_history.update(oneTruck.where_next())
threeTruck.set_time(datetime(1900, 1, 1, 9, 6))

# Process: Corrects wrong address packages. Loads all "wrong address" packages onto two truck.
# Process: All other packages onto three truck

# Flow : Iterates through wrong_address. If Wrong in j.notes then update the address and load it onto truck 2
# Flow : Else update pickup time then add it to three truck
for j in wrong_address:
    if "Wrong" in j.notes:
        j.set_pickup(twoTruck.get_time())
        j.set_address("410 S State St")
        j.set_city("Salt Lake City")
        j.set_state("UT")
        j.set_zipcode(84111)
        twoTruck.add(j)
    else:
        j.set_pickup(threeTruck.get_time())
        threeTruck.add(j)

# All Two Truck and Three Truck are sent out. package_history is updated with returns from where_next()
package_history.update(threeTruck.where_next())
package_history.update(twoTruck.where_next())

# All items in package_history are reinserted back into package_table. Also prints the final miles driven

print("\nCombined Miles Driven By All Three Trucks:", twoTruck.miles_driven + oneTruck.miles_driven
      + threeTruck.miles_driven, end="\n\n")

packageTable.pack_table.multi_insert(list(package_history))

# Interface starts. Options printed. User input prompted for.
user_inp = menu_options().lower()

# Process : Loops through offering options that a user can select. Prints out different output based on user choice
# Process : If user chooses option that is not available, the loop will restart.

# Flow : Iterates through options while user_inp is not e.
# Flow :  If b prompts for user to check packages by Time Range(1) or id(2).
# Flow :  If 1 then prompts for earliest and latest time. Loops through packageTable.
#  Delivery status changed based on time range. All package info printed.
# Flow :  If 2 loops through packageTable and prints packages that match the id.
# Flow :  If option a then program prints all package info in packageTable
# Flow : If option c then prompts for Delivery Deadline. Loops through and prints packages with same deadline.
# Flow : if option d then prints by actual delivery time
# Flow : If option e then the loop ends
# Flow : if option f, program prompts for truck num. Checks that the input is valid  then prints only
# packages that match that truck_num
# If e not selected then after each other option the user is prompted for another option
# If user enters an invalid option then loop restarts with a call to menu_options()

while user_inp != "e":
    if user_inp == "b":
        user_inp = is_int("1: By Time Range\n2: By Package Id")
        if user_inp == 2:
            user_inp = is_int(" Please input package id")
            table_headers()
            packageTable.return_item(user_inp).set_delivery_status("DELIVERED")
            packageTable.return_item(user_inp).return_all_details()
        elif user_inp == 1:
            user_inp_early = datetime.strptime(input(" Please enter earliest time:"), "%I:%M %p")
            user_inp_late = datetime.strptime(input(" Please enter latest time:"), "%I:%M %p")
            print("Status Of All Packages from", user_inp_early.strftime("%I:%M %p"), "to",
                  user_inp_late.strftime("%I:%M %p"))
            table_headers()
            for i in range(1, 41):
                package = packageTable.return_item(i)
                time_delivered = datetime.strptime(packageTable.return_item(i).get_delivered(), "%I:%M %p")
                if package:
                    if package.get_pickup() > user_inp_late:
                        package.set_delivery_status("HUB")
                        package.return_all_details()
                    elif user_inp_early < time_delivered > user_inp_late:
                        package.set_delivery_status("EN ROUTE")
                        package.return_all_details()
                    else:
                        package.set_delivery_status("DELIVERED")
                        package.return_all_details()
            print("Total Miles Driven For The Day: ",
                  twoTruck.miles_driven + oneTruck.miles_driven + threeTruck.miles_driven)
        else:
            print("Please input a valid option!   ")
        print("\n")
    elif user_inp == "a":
        table_headers()
        for i in range(1, 41):
            package = packageTable.return_item(i)
            if package:
                package.set_delivery_status("DELIVERED")
                package.return_all_details()
    elif user_inp == "c":
        get_time(user_inp)
    elif user_inp == "d":
        get_time(user_inp)
    elif user_inp == "f":
        truck_ids = [1, 2, 3]
        while user_inp not in truck_ids:
            user_inp = is_int(" Please enter Truck ID:")
        print("Summary Of Packages Delivered By Truck ", user_inp, "\n")
        table_headers()
        total_packages_del = 0
        for i in range(1, 41):
            if packageTable.return_item(i).get_truck_num() == user_inp:
                packageTable.return_item(i).set_delivery_status("DELIVERED")
                packageTable.return_item(i).return_all_details()
                total_packages_del += 1
        print("\n Total Packages Delivered on Truck #", user_inp, " were ", total_packages_del, "\n")
    else:
        print("Error! Please enter a valid menu option:")
    user_inp = menu_options()
