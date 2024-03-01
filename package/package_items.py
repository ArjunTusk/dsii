import csv
from datetime import datetime, timedelta

import hasTable


class NewPackage:
    def __init__(self):
        self.zipcode = None
        self.state = None
        self.city = None
        self.pickup = None
        self.address = None
        self.delivery_status = None
        self.truck_num = None
        self.delivered = None

    def __init__(self, id_package, address, city, state, zipcode, delivery_deadline, weight, notes):
        self.id = id_package
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = int(zipcode)
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.notes = notes
        self.truck_num = 0
        self.delivered = datetime(1900, 1, 1, 8, 0)
        self.pickup = datetime(1900, 1, 1, 8, 0)
        self.delivery_status = "HUB"

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def set_truck_num(self, truck_num):
        self.truck_num = truck_num

    def get_truck_num(self):
        return self.truck_num

    def set_delivery_status(self, delivery_status):
        self.delivery_status = delivery_status

    def get_delivery_status(self):
        return self.delivery_status

    def set_delivered(self, delivered):
        self.delivered = delivered

    def get_delivered(self):
        return self.delivered

    def get_pickup(self):
        return self.pickup

    def set_pickup(self, pickup):
        self.pickup = pickup

    def get_city(self):
        return self.city

    def set_city(self, city):
        self.city = city

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_delivery_deadline(self):
        return self.delivery_deadline.strftime("%I:%M %p")

    def get_zipcode(self):
        return self.zipcode

    def set_zipcode(self, zipcode):
        self.zipcode = zipcode

    def get_id(self):
        return int(self.id)

    def get_notes(self):
        return self.notes

    # Process : Formats the strings into a table then prints it out
    # Flow : Creates cells that are 25px wide where each string will be centered then prints it

    def return_all_details(self):
        if self.delivery_deadline.strftime("%I:%M %p") == "11:59 PM":
            print("{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}".format(self.address,
                                                                            "EOD",
                                                                            self.city,
                                                                            self.zipcode, self.weight,
                                                                            self.delivery_status,
                                                                            self.delivered))
        else:
            print("{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}".format(self.address,
                                                                            self.delivery_deadline.strftime("%I:%M %p"),
                                                                            self.city,
                                                                            self.zipcode, self.weight,
                                                                            self.delivery_status,
                                                                            self.delivered))


class Parse:
    def __init__(self):
        self.address2 = set()
        self.myList = set()
        self.mid_zip = 0
        self.pack_table = hasTable.HasTable(40)
        self.ipp = 0
        self.ignore_it = set()
        self.delivery_deadline = datetime(1900, 12, 12, 12, 30)

    # returns the size of the hashTable
    def size(self):
        return self.pack_table.__len__()

    # Process : Opens the file and splits the list then adds it to the hash table. Ignores "," between quotes
    # Flow : open the file while ignoring any element that has a comma between quotes
    # Flow : For line in the file check if the 5th element is EOD. We convert this to 11:59 PM to make time comparisons
    # Flow : easier for later. Convert line[5] to a datetime object. Insert all elements in the array into a NewPackage
    # Flow : object. Insert package into the pack_table with i being the key. Increase i. Loop to last line in toParse.
    def read_files(self, file):
        i = 1
        with open(file) as f:
            toParse = csv.reader(f, delimiter=',', quotechar="\"")
            for line in toParse:
                if line[5] == "EOD":
                    line[5] = "11:59 PM"
                line[5] = datetime.strptime(line[5], "%I:%M %p")
                package = NewPackage(i, line[1], line[2], line[3], int(line[4]), line[5], line[6], line[7])
                self.pack_table.insert(i, package)
                i += 1

    # Process : checks to see if the package must be delivered with another package
    # Flow : Make the set no_duplicates. Loop through the hash table. If there's an item at that key check if "Must be"
    # Flow : is in the notes. If so, set the pickup time. Grab the two numbers in the notes section, put in array
    # Flow : Search for keys that match either number in the array. Set pickup for both packages then add to the set.
    # Flow : Remove the values at key i. Loop ends then call self.duplicates and convert the final value to an array.
    # Flow : Return the final array.
    def bundle_package(self, time):
        no_duplicates = set()
        for i in range(41):
            search_table = self.pack_table.search(i)
            if search_table:
                if "Must be " in search_table.notes:
                    search_table.set_pickup(time)
                    is_num = search_table.notes.replace("Must be delivered with ", "").split(",")
                    no_duplicates.add(search_table)
                    search_table = self.pack_table.search(int(is_num[0]))
                    search_table.set_pickup(time)
                    no_duplicates.add(search_table)
                    search_table = self.pack_table.search(int(is_num[1]))
                    search_table.set_pickup(time)
                    no_duplicates.add(search_table)
                    self.pack_table.remove(i)

        z = list(self.duplicates(no_duplicates, time))

        return z

    # Process : checks to see if string matches. Adds to bundled_package if true
    # Flow : Declares a set and loop length. Cycles through all the keys in the table. If the string is found
    # Flow : in the notes then the pickup time is set and the  package is added to the no_duplicates set.
    # Flow : The item is then removed from the table
    def bundle_package_string(self, which_package, time):
        no_duplicates = set()
        loop_length = 40
        for i in range(1, loop_length):
            table_hold = self.pack_table.search(i)
            if self.pack_table.search(i):
                if which_package in table_hold.notes:
                    table_hold.set_pickup(time)
                    no_duplicates.add(table_hold)
                    self.pack_table.remove(i)
        bundled_package = list(self.duplicates(no_duplicates, time))

        return bundled_package

    # Process: Finds matching addresses and bundles them together in a set
    # Flow : Set found_match to set()
    # Flow : Search through the original package list for addresses that match the ones in orig_set and have no notes.
    # Flow : Set the pickup time to the time passed to it. Add it to found_match then remove it from the table.
    # Flow : Return the union of orig_set and found_match
    def duplicates(self, orig_set, time):
        found_match = set()
        for j in orig_set:
            for i in range(41):
                search_table = self.pack_table.search(i)
                if search_table:
                    if search_table.get_address() == j.get_address() and search_table.notes == "":
                        search_table.set_pickup(time)
                        found_match.add(search_table)
                        self.pack_table.remove(i)
        return orig_set.union(found_match)

    # Process : Returns the package whose id matches the variable passed to the method
    # Flow : searchs the table for the key and returns the value
    def return_item(self, key):
        item_look_up = self.pack_table.search(key)
        return item_look_up

    # Process : Searches the table for the first available item in the table returns false if empty
    # Flow : Searches the table for key self.ipp. If it is found then it is returned.
    # Flow : Otherwise, the while loop will run till it is found then returns the found value
    def return_line(self):
        search_table = self.pack_table.search(self.ipp)
        while not search_table:
            self.ipp += 1
            search_table = self.pack_table.search(self.ipp)
        final_value = search_table
        self.pack_table.remove(self.ipp)
        return final_value
