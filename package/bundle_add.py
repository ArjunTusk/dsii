import csv
import hasTable


class Parse:
    def __init__(self):
        self.myList = []
        self.pack_table = hasTable.HasTable(40)
        self.ipp = 0
        self.ignore_it = set()

    # returns the size of the hashTable
    def size(self):
        return self.pack_table.__len__()

    # Opens the file and splits the list then adds it to the hash table. Ignores "," between quotemarks
    def read_files(self, file):
        i = 1
        with open(file) as f:
            toParse = csv.reader(f, delimiter=',', quotechar="\"")
            for line in toParse:
                self.pack_table.insert(i, line[1:])
                i += 1

    # Searches the hash table for the matching key then prints the address
    def find_address(self, key):
        a = ""
        for i in range(26):
            a = self.pack_table.search(i + 1)[0]
            if a == key:
                print(i + 1)

    # checks to see if the package must be delivered with another package
    def bundle_package(self):
        seen_it = set()
        bundle_items = []
        loop_length = self.size()
        for i in range(1, int(loop_length / 2) + 1):
            the_item = self.pack_table.search(i)
            t = loop_length - i
            the_other_item = self.pack_table.search(loop_length - i)
            if "Must be " in the_item[6]:
                seen_it.add(i)
                is_num = the_item[6].replace("Must be delivered with ", "").split(",")
                seen_it.add(int(is_num[0]))
                seen_it.add(int(is_num[1]))
            if "Must be " in the_other_item[6]:
                seen_it.add(loop_length - i)
                is_num = the_other_item[6].replace("Must be delivered with ", "").split(",")
                seen_it.add(int(is_num[0]))
                seen_it.add(int(is_num[1]))

        for m in seen_it:
            bundle_items.append(self.pack_table.search(m))
            self.ignore_it.add(m)

        return bundle_items

    def remove_it(self):
        for value in self.ignore_it:
            self.pack_table.remove(value)

    # checks to see if the package is delayed then puts it into a list. The delayed package is then removed
    def bundle_package_string(self, which_package):
        bundled_package = []
        loop_length = (40 / 2) + 1
        for i in range(1, int(loop_length)):
            the_item = self.pack_table.search(i)
            the_other_item = self.pack_table.search(40 - i)
            if which_package in the_other_item[6]:
                bundled_package.append(the_other_item)
                self.ignore_it.add(40 - i)
            if i in self.ignore_it:
                continue
            if which_package in the_item[6]:
                bundled_package.append(the_item)
                self.ignore_it.add(i)

        return bundled_package

    # prints all the packages in the original table with their keys attached
    def print_it(self):
        for i in range(40):
            if self.pack_table.contains(i):
                print(self.pack_table.search(i), " ", i)

    # returns the first available package
    def return_line(self):
        dd = self.pack_table.search(self.ipp)
        while not dd:
            self.ipp += 1
            dd = self.pack_table.search(self.ipp)
        ded = dd
        self.pack_table.remove(self.ipp)
        return ded
