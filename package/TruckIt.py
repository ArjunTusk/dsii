import csv
from datetime import datetime, timedelta

from package.package_items import NewPackage


class Truck:
    def __init__(self, file, truck_num):
        self.truck_num = truck_num
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

    # returns the current haul
    def return_current_haul(self):
        return self.currentHaul

    # reads the double matrix and populates the 2d - array
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
        if len(self.currentHaul) - 1 < 16:
            if isinstance(package, NewPackage):
                self.currentHaul.append(package)
                self.total_packages_delivered += 1

            else:
                self.total_packages_delivered += len(package)
                self.currentHaul += package
        else:
            print("Sorry! Too full. Deliver or remove some packages first.")

        if len(self.currentHaul) - 1 > 16:
            self.overflow = self.currentHaul[17:]
            self.currentHaul = self.currentHaul[:16]
        else:
            self.currentHaul.extend(self.overflow)
        a = self.currentHaul[0]
        self.currentHaul = sorted(self.currentHaul[1:], key=lambda newpackage: newpackage.zipcode)
        if len(self.currentHaul) - 1 >= 2:
            self.mid_zip = self.currentHaul[int(self.sizeIt() / 2)].zipcode
            self.currentHaul.insert(0, a)
        else:
            self.currentHaul.insert(0, a)
            self.mid_zip = self.currentHaul[0].zipcode
        return 1

    # returns the time the truck leaves a destination
    def set_time(self, time):
        self.on_road = time

    # sets the time the truck leaves a destination
    def get_time(self):
        return self.on_road

    # Returns the amount of packages currently in the hall
    def sizeIt(self):
        return len(self.currentHaul) - 1

    # Prints what items are in the package
    def print_haul(self):
        for i in self.currentHaul:
            print(i)

    # adds the amount of time on the road to the current tally
    def time_on_road(self, dist_driven):
        time_hours = dist_driven / self.speed
        self.on_road += timedelta(hours=time_hours)

    # delivers the packages based on distance. Swaps the second array item with the nearest destination. Prints out
    # the start and end times
    def where_next(self):
        aa = []
        j = 0
        print("\nTruck #", self.truck_num, "on the road:")
        if len(self.currentHaul) == 1:
            print("Truck is empty! Please add packages.")
        # checks which truck is closest to the current destination until it gets to the last package
        while len(self.currentHaul) > 1:
            min_dist = self.find_dist(self.currentHaul[0].get_address(), self.currentHaul[1].get_address())
            for i in range(1, len(self.currentHaul)):
                next_dist = self.find_dist(self.currentHaul[0].get_address(), self.currentHaul[i].get_address())
                if self.currentHaul[0].get_address() == self.currentHaul[i].get_address():
                    min_dist = 0
                    j = i
                    break
                elif min_dist >= next_dist:
                    min_dist = next_dist
                    j = i

            # delivers the last package
            self.time_on_road(min_dist)
            print("Start:", self.currentHaul[0].get_address(), "\tEnd:", self.currentHaul[j].get_address(), end="\t")
            print("Delivery Time: ", self.currentHaul[j].get_delivery_time(), "Arrival Time:",
                  self.get_time().strftime("%I:%M %p"))
            self.miles_driven += min_dist
            self.currentHaul[0].set_delivered(self.get_time().strftime("%I:%M %p"))
            aa.append(self.currentHaul[0])
            self.currentHaul.pop(0)
            swap = self.currentHaul[0]
            self.currentHaul[0] = self.currentHaul[j - 1]
            self.currentHaul[j - 1] = swap

        # returns to the HUB
        self.currentHaul.insert(1, NewPackage("0", "4001 South 700 East", "", "", 84107, "", "", ""))
        self.time_on_road(self.find_dist(self.currentHaul[0].get_address(), self.currentHaul[1].get_address()))
        print("Start:", self.currentHaul[0].get_address(), "\tEnd:", self.currentHaul[1].get_address(), end="\t")
        print("Return to HUB", "Arrival Time:", self.get_time().strftime("%I:%M %p"))
        self.currentHaul[0].set_delivered(self.get_time().strftime("%I:%M %p"))
        aa.append(self.currentHaul[0])
        self.currentHaul.pop(0)
        return aa

    # finds the distance between two addresses by searching the 2-d array
    def find_dist(self, start, end):
        column_num = 0
        row_num = 0
        for i in range(len(self.matrix)):
            if self.matrix[i][0] == start:
                column_num = i
            if self.matrix[i][0] == end:
                row_num = i
        return self.matrix[column_num][row_num + 1]
