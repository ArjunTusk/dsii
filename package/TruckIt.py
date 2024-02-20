import csv
from datetime import datetime, timedelta


class Truck:
    def __init__(self, file):

        self.currentHaul = []
        self.on_road = datetime(2024, 2, 15, 8, 0)
        self.sizTwo = len(self.currentHaul)
        self.file = file
        self.size = 28
        self.location = 0
        self.matrix = [[-1 for columns in range(self.size)] for rows in range(self.size - 1)]
        self.readPopMatrix()

    def return_current_haul(self):
        return self.currentHaul

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
            if len(package) == 7:
                self.currentHaul.extend([package])
            else:
                self.currentHaul += package
        else:
            print("Sorry! Too full. Deliver or remove some packages first.")

    def set_time(self, time):
        self.on_road = time

    def get_time(self):
        return self.on_road

    # Removes all packages at once
    def removePackage(self):
        for i in range(len(self.currentHaul)):
            self.currentHaul.pop()
            self.size -= 1

    # Returns the amount of packages currently in the hall
    def sizeIt(self):
        return len(self.currentHaul)

    # Prints what items are in the package
    def printHaul(self):
        for i in self.currentHaul:
            print(i)

    def wherenext(self, addresses):
        min_time = datetime.strptime(addresses[0][4], "%I:%M %p")
        time_format = "%I:%M %p"
        final_dest_time = 0
        final_dest = 0
        swap = ""
        fin_miles = 0
        found = False
        addresses.insert(0, ["4001 South 700 East"])

        for i in range(len(addresses) - 2):
            next_dest = addresses[i + 1][0]
            min_time = datetime.strptime(addresses[i + 1][4], "%I:%M %p")
            min_dist = self.find_dist(addresses[i][0], next_dest)
            for j in range(i + 1, len(addresses) - 1):
                if addresses[i][0] == addresses[j][0]:
                    print("Dropping package off in the same location")
                    found = True
                    swap = addresses[i + 1]
                    addresses[i + 1] = addresses[j]
                    addresses[j] = swap
                    break
                tyrit = self.find_dist(addresses[i][0], addresses[j][0])
                new_time = datetime.strptime(addresses[j][4], time_format)
                if new_time <= min_time:
                    min_time = new_time
                    final_dest_time = j
                    fin_miles = tyrit
                if tyrit < min_dist:
                    min_dist = tyrit
                    final_dest = j
            if found:
                found = False
                continue
            if min_time.strftime("%I:%M %p") != "11:59 PM":
                time_hours = fin_miles / 18
                self.on_road += timedelta(hours=time_hours)
                print("From", addresses[i][0], "To", addresses[final_dest_time][0], "which is",
                      fin_miles, "miles away. Expected Delivery:", addresses[final_dest_time][4], "Expected arrival",
                      self.on_road.strftime("%I:%M %p"))
                swap = addresses[i + 1]
                addresses[i + 1] = addresses[final_dest_time]
                addresses[final_dest_time] = swap
            else:
                time_hours = min_dist / 18
                self.on_road += timedelta(hours=time_hours)
                print("From", addresses[i][0], "to", addresses[final_dest][0], "which is",
                      min_dist, addresses[final_dest][4], "miles away. Expected arrival",
                      self.on_road.strftime("%I:%M %p"))
                swap = addresses[i + 1]
                addresses[i + 1] = addresses[final_dest]
                addresses[final_dest] = swap
        print()
        a = self.find_dist("4001 South 700 East", swap[0])
        time_hours = a / 18
        self.on_road += timedelta(hours=time_hours)
        print("We are returning to HUB. Last Stop was",
              swap[0], ". Distance from HUB is",
              a, "miles away. Arrival Time:", self.on_road.strftime("%I:%M %p"))
        print()

    def find_dist(self, start, end):
        column_num = 0
        row_num = 0
        for i in range(len(self.matrix)):
            if self.matrix[i][0] == start:
                column_num = i
            if self.matrix[i][0] == end:
                row_num = i
        return self.matrix[column_num][row_num + 1]
