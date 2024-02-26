import csv
from datetime import datetime, timedelta

import hasTable


class NewPackage:
    def __init__(self):
        self.delivered = None

    def __init__(self, id_package, address, city, state, zipcode, delivery_time, weight, notes):
        self.id = id_package
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = int(zipcode)
        self.delivery_time = delivery_time
        self.weight = weight
        self.notes = notes
        self.delivered = datetime(1900, 1, 1, 8, 0)

    def set_delivered(self, delivered):
        self.delivered = delivered

    def get_delivered(self):
        return self.delivered

    def get_delivery_time(self):
        return self.delivery_time.strftime("%I:%M %p")

    def get_address(self):
        return self.address

    def get_id(self):
        return int(self.id)

    def get_notes(self):
        return self.notes

    def return_all_details(self):
        return (self.id, " " + self.address + " " + self.city + " " + self.state + " ", self.zipcode
                , self.delivery_time.strftime("%I:%M %p"), " " + self.weight + " " + self.notes + " ", self.delivered,
                " ")


class Parse:
    def __init__(self):
        self.address2 = set()
        self.myList = set()
        self.mid_zip = 0
        self.pack_table = hasTable.HasTable(40)
        self.ipp = 0
        self.ignore_it = set()
        self.delivery_time = datetime(1900, 12, 12, 12, 30)

    # returns the size of the hashTable
    def size(self):
        return self.pack_table.__len__()

    # Opens the file and splits the list then adds it to the hash table. Ignores "," between quotemarks
    def read_files(self, file):
        i = 1
        high = 0
        real_high = 0
        real_low = 0
        low = 0
        with open(file) as f:
            toParse = csv.reader(f, delimiter=',', quotechar="\"")
            for line in toParse:
                if high == 0:
                    real_low = int(line[4])
                    real_high = int(line[4])
                high = int(line[4])
                low = int(line[4])
                if high > real_high:
                    real_high = high
                if real_low > low:
                    real_low = low
                if line[5] == "EOD":
                    line[5] = "11:59 PM"
                line[5] = datetime.strptime(line[5], "%I:%M %p")
                package = NewPackage(i, line[1], line[2], line[3], int(line[4]), line[5], line[6], line[7])
                self.pack_table.insert(i, package)
                i += 1
            self.mid_zip = (real_low + real_high) / 2

    # checks to see if the package must be delivered with another package
    def bundle_package(self):
        seen_it = set()
        bundle_items = []
        loop_length = self.size()
        for i in range(1, loop_length):
            the_item = self.pack_table.search(i)
            seen_it = self.match_it(the_item, seen_it)

        for m in seen_it:
            bundle_items += [self.pack_table.search(m)]
            self.ignore_it.add(m)

        return bundle_items

    def match_it(self, the_item, seen_it):
        if "Must be " in the_item.notes:
            seen_it.add(int(the_item.get_id()))
            is_num = the_item.notes.replace("Must be delivered with ", "").split(",")
            seen_it.add(int(is_num[0]))
            seen_it.add(int(is_num[1]))
            self.address2.add(the_item.get_address())
        elif (the_item.get_address() in self.address2 and the_item.get_id()
              not in self.ignore_it and the_item.notes == ""):
            seen_it.add(the_item.get_id())

        return seen_it

    def bundle_package_date(self, which_package):
        bundled_package = []
        for i in range(40):
            the_item = self.pack_table.search(i)
            if the_item:
                a = the_item.get_delivery_time()
                if which_package == the_item.get_delivery_time():
                    bundled_package.append(the_item)
                    self.ignore_it.add(i)

        return bundled_package

    def remove_it(self):
        for value in self.ignore_it:
            try:
                self.pack_table.remove(value)
            except KeyError:
                a = ""

    # checks to see if string matches. Adds to bundled_package if true
    def bundle_package_string(self, which_package):
        bungle = []
        loop_length = (40 / 2) + 1
        for i in range(1, int(loop_length)):
            the_item = self.pack_table.search(i)
            the_other_item = self.pack_table.search(40 - i)
            if not the_item:
                break
            if not the_other_item:
                break
            if which_package in the_other_item.notes:
                bungle.append(the_other_item)
                self.address2.add(the_other_item.get_address())
                self.ignore_it.add(the_other_item.get_id())
            if the_other_item.notes == "" and the_other_item.get_id() not in self.ignore_it and the_other_item.get_address() in self.address2:
                bungle.append(the_other_item)
                self.ignore_it.add(the_other_item.get_id())
            if i in self.ignore_it:
                continue
            if which_package in the_item.notes:
                bungle.append(the_item)
                self.ignore_it.add(the_item.get_id())
            if the_item.notes == "" and the_item.get_id() not in self.ignore_it and the_item.get_address() in self.address2:
                bungle.append(the_item)
                self.ignore_it.add(the_item.get_id())

        return bungle

    # returns the first available package
    def return_early_pack(self, delivery):
        aa = set()
        for i in range(41):
            dd = self.pack_table.search(i)
            if dd:
                if dd.get_delivery_time() == delivery:
                    aa.add(dd)
                    self.pack_table.remove(i)

        z = list(self.duplicates(aa))

        return z

    def duplicates(self, aa):
        bb = set()
        for j in aa:
            for i in range(41):
                dd = self.pack_table.search(i)
                if dd:
                    if dd.get_address() == j.get_address():
                        bb.add(dd)
                        self.pack_table.remove(i)
        return aa.union(bb)

    def return_line(self):
        dd = self.pack_table.search(self.ipp)
        while not dd:
            self.ipp += 1
            dd = self.pack_table.search(self.ipp)
        ded = dd
        self.pack_table.remove(self.ipp)
        return ded
