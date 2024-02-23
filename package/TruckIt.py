import csv
from datetime import datetime, timedelta

from package.package_items import NewPackage


class Truck:
    def __init__(self, file):
        self.mid_zip = 0
        self.first_loc = NewPackage("0", "4001 South 700 East", "", "", 84107, "", "", "")
        self.currentHaul = [self.first_loc]
        self.overflow = []
        self.on_road = datetime(1900, 1, 1, 8, 0)
        self.sizTwo = len(self.currentHaul)
        self.miles_driven = 0
        self.file = file
        self.size = 28
        self.speed = 18
        self.total_packages_delivered = 0
        self.matrix = [[-1 for columns in range(self.size)] for rows in range(self.size - 1)]
        self.readPopMatrix()

    def return_current_haul(self):
        return self.currentHaul

    def mid_zip(self):
        return 0

    def readPopMatrix(self):
        a = ""
        xx = 0
        with open(self.file) as f:
            toParse = csv.reader(f, delimiter=',', quotechar="\"")
            next(toParse)
            for line in toParse:
                for g in range(self.size):
                    if g != 0 and line[g] != "":
                        self.matrix[xx][int(g)] = float(line[g].replace("\n", "").strip(" "))
                    elif line[g].find("(") != -1:
                        a = line[g].replace("\n", "").strip(" ")
                        self.matrix[xx][g] = a[0:a.index("(")]
                    elif line[g] == "":
                        continue
                    else:
                        self.matrix[xx][g] = line[g].replace("\n", "").strip(" ")
                xx += 1

        self.matrix[0][0] = "4001 South 700 East"
        for col2 in range(27):
            for row2 in range(28):
                if self.matrix[col2][row2] == -1:
                    self.matrix[col2][row2] = self.matrix[row2 - 1][col2 + 1]

    # Accepts a list and adds each item to the truck contained
    def add(self, package):
        if len(self.currentHaul) < 16:
            if isinstance(package, NewPackage):
                self.currentHaul.append(package)
                self.total_packages_delivered += 1

            else:
                self.total_packages_delivered += len(package)
                self.currentHaul += package
        else:
            print("Sorry! Too full. Deliver or remove some packages first.")

        if len(self.currentHaul) > 16:
            self.overflow = self.currentHaul[17:]
            self.currentHaul = self.currentHaul[:16]
        else:
            self.currentHaul.extend(self.overflow)
        a = self.currentHaul[0]
        self.currentHaul = sorted(self.currentHaul[1:], key=lambda newpackage: newpackage.zipcode)
        if len(self.currentHaul) >= 2:
            self.mid_zip = self.currentHaul[int(self.sizeIt() / 2)].zipcode
            self.currentHaul.insert(0, a)
        else:
            self.currentHaul.insert(0, a)
            self.mid_zip = self.currentHaul[0].zipcode
        return 1

    def set_time(self, time):
        self.on_road = time

    def get_time(self):
        return self.on_road

    # Removes all packages at once

    # Returns the amount of packages currently in the hall
    def sizeIt(self):
        return len(self.currentHaul)

    # Prints what items are in the package
    def printHaul(self):
        for i in self.currentHaul:
            print(i)

    def time_on_road(self, dist_driven):
        time_hours = dist_driven / self.speed
        self.on_road += timedelta(hours=time_hours)

    def where_next(self):
        if self.currentHaul[0].get_address() != "4001 South 700 East":
            self.currentHaul.insert(0, NewPackage(0, "4001 South 700 East", "", "", 84107, "", "", ""))
        self.currentHaul = sorted(self.currentHaul[1:], key=lambda newpackage: newpackage.address)
        self.currentHaul.insert(0, NewPackage(0, "4001 South 700 East", "", "", 84107, "", "", ""))
        aa = self.currentHaul[1]
        min_dist = self.find_dist(self.currentHaul[0].get_address(), aa.get_address())
        length = len(self.currentHaul)
        while len(self.currentHaul) >2:
            found = False
            min_time = self.currentHaul[1].get_delivery_time()
            for j in range(1, len(self.currentHaul)):
                if self.currentHaul[0].get_address() == self.currentHaul[j].get_address():
                    print("We deliver to the same place")
                    self.currentHaul[j].set_delivery_time(self.on_road)
                    self.currentHaul.pop(j)
                    found = True
                    break

                next_dist = self.find_dist(self.currentHaul[0].get_address(), self.currentHaul[j].get_address())
                next_time = self.currentHaul[j].get_delivery_time()
                if min_time >= next_time:
                    min_time = next_time
                    if min_dist > next_dist:
                        min_dist = next_dist
                        swap = self.currentHaul[1]
                        self.currentHaul[1] = self.currentHaul[j]
                        self.currentHaul[j] = swap

            if not found:
                self.miles_driven += min_dist
                self.time_on_road(min_dist)
                print("Start:", self.currentHaul[0].get_address(), "\tEnd:", self.currentHaul[1].get_address(),
                      "\tExp Delivery:",
                      self.currentHaul[1].get_delivery_time().strftime('%I:%M %p'), "\tArrival Time:",
                      self.on_road.strftime('%I:%M %p'))
                self.currentHaul[1].set_delivery_time(self.on_road)
                self.currentHaul[1].set_delivery_time(self.on_road)
                self.currentHaul.pop(0)
                min_dist = self.find_dist(self.currentHaul[0].get_address(), self.currentHaul[1].get_address())
                length = len(self.currentHaul)

        min_dist = self.find_dist(self.currentHaul[0].get_address(), self.currentHaul[1].get_address())
        self.miles_driven += min_dist
        self.time_on_road(min_dist)

        print("Start:", self.currentHaul[0].get_address(), "\t\tEnd:", self.currentHaul[1].get_address(),
              "\tExp Delivery:",
              self.currentHaul[1].get_delivery_time().strftime('%I:%M %p'), "\t\tArrival Time:",
              self.on_road.strftime('%I:%M %p'))

        self.currentHaul[1].set_delivery_time(self.on_road)
        self.miles_driven += min_dist
        self.time_on_road(min_dist)
        self.currentHaul.pop(0)

        min_dist = self.find_dist(self.currentHaul[0].get_address(), "4001 South 700 East")
        self.time_on_road(min_dist)
        print("Start:", self.currentHaul[0].get_address(), "\t\tEnd: 4001 South 700 East",
              "\tReturning to HUB" "\tArrival Time:", self.on_road.strftime('%I:%M %p'), "\n")
        self.currentHaul.pop(0)

    def find_dist(self, start, end):
        column_num = 0
        row_num = 0
        for i in range(len(self.matrix)):
            if self.matrix[i][0] == start:
                column_num = i
            if self.matrix[i][0] == end:
                row_num = i
        return self.matrix[column_num][row_num + 1]
