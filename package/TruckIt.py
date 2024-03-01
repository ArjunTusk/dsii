import csv
from datetime import datetime, timedelta

from package.package_items import NewPackage


class Truck:
    def __init__(self, file, truck_num):
        self.truck_num = truck_num
        self.first_loc = NewPackage("0", "4001 South 700 East", "", "", 84107, "", "", "")
        self.currentHaul = [self.first_loc]
        self.on_road = datetime(1900, 1, 1, 8, 0)
        self.miles_driven = 0
        self.file = file
        self.size = 28
        self.speed = 18
        self.total_packages_delivered = 0
        self.matrix = [[-1 for columns in range(self.size)] for rows in range(self.size - 1)]
        self.readPopMatrix()

    # returns the current list of packages
    def return_current_haul(self):
        return self.currentHaul

    # Process: reads the double matrix and populates the 2d - array
    # Flow : reads the file. Splits the file while ignoring anything surrounded by quotes
    # Flow : Starts a for loop with the second line in toParse
    # Flow : Starts another for loop that will go from 0 to self.size
    # Flow : check if g doesn't equal 0 and line[g] isn't empty. If satisfied edit line[g] and input it into the matrix[xx][gg]
    # Flow : continue if line [g] == "" is empty.  If there's a ")" in line[g] the remove the parenthesis and insert it into matrix[xx][g]
    # Flow : else strip line[g] and input it into matrix[xx][g].

    def readPopMatrix(self):
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
# Flow swap HUB for "4001 South 700 East" then duplicate the numbers so there are no empty cells in self.matrix
        self.matrix[0][0] = "4001 South 700 East"
        for col2 in range(27):
            for row2 in range(28):
                if self.matrix[col2][row2] == -1:
                    self.matrix[col2][row2] = self.matrix[row2 - 1][col2 + 1]

    # Process: Accepts a list and adds each item to the truck contained
    # Flow : pass package to the method. Check that the len(self.currentHaul)-1 < 16
    # Flow : if yes then check if package is an instance of NewPackage
    # Flow : if yes then append the package to self.currentHaul. Increase self.total_packages_delivered by 1
    # Flow : if not an instance of NewPackage then just add it all to the self.currentHaul
    # Flow : if the len(self.currentHaul)-1 < 16 is false then print("Sorry! Too full. Deliver or remove some packages first.")
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

    # Process: Accepts a list. Iterates through list to determine which address is closest to the 0th element.
    # 0th element is then removed.
    # Flow : prints truck number and departure time
    # Flow : Prints that the truck is empty if len(self.currentHaul) == 1
    #  grabs the distance between the 0th and 1st element and set it as the minimum distance
    # Flow : loops through the 1st to last element. Checking each element against the 0th element.
    # Flow : if any element has the same address as the 0th element then the for loop is broken
    # Flow : else checks if 0 to latest element distance is smaller than 0 to 1st element.
    # Flow : If yes then the latest element will be the next destination for the truck
    # Flow : After self.current_haul is reduced to one package. The truck is returned
    # Flow : Distance traveled is updated as is time on_road. Returns the array package history

    def where_next(self):
        print("\nTruck #", self.truck_num, "left HUB at", self.on_road.strftime("%I:%M %p"))
        package_history = []
        j = 0

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
            self.miles_driven += min_dist
            self.currentHaul[j].set_delivered(self.get_time().strftime("%I:%M %p"))
            self.currentHaul[j].set_truck_num(self.truck_num)
            package_history.append(self.currentHaul[j])
            self.currentHaul.pop(0)
            swap = self.currentHaul[0]
            self.currentHaul[0] = self.currentHaul[j - 1]
            self.currentHaul[j - 1] = swap

        # returns to the HUB
        self.currentHaul.insert(1, NewPackage("0", "4001 South 700 East", "", "", 84107, "", "", ""))
        self.time_on_road(self.find_dist(self.currentHaul[0].get_address(), self.currentHaul[1].get_address()))
        print("Route Complete! Miles driven:", self.miles_driven, "Returned to HUB at", self.on_road.strftime("%I:%M "
                                                                                                              "%p"))
        package_history.append(self.currentHaul[0])
        self.currentHaul.pop(0)
        return package_history

    # Process: finds the distance between two addresses by searching the 2-d array
    # Flow : For loop iterates through the matrix to find the cross-section where the distance between two locations are
    def find_dist(self, start, end):
        column_num = 0
        row_num = 0
        for i in range(len(self.matrix)):
            if self.matrix[i][0] == start:
                column_num = i
            if self.matrix[i][0] == end:
                row_num = i
        return self.matrix[column_num][row_num + 1]
