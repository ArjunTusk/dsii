import csv
import bundle_add


class Truck:
    def __init__(self, file):

        self.currentHaul = []
        self.size = 0
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
                        self.matrix[xx][g] = float(line[g].replace("\n", "").strip(" "))
                    elif line[g].find("(") != -1:
                        a = line[g].replace("\n", "").strip(" ")
                        self.matrix[xx][g] = a[0:a.index("(")]
                    elif line[g] == "":
                        continue
                    else:
                        self.matrix[xx][g] = line[g].replace("\n", "").strip(" ")

                xx += 1

        self.matrix[0][0] = "4001 South 700 East"
        ll = 1
        for i in range(0, 27):
            for j in range(1, 28):
                if self.matrix[i][j] == -1:
                    self.matrix[i][j] = self.matrix[j - 1][ll]
            ll += 1

    # Accepts a list and adds each item to the truck contained
    def add(self, package):
        for i in range(len(package)):
            self.currentHaul.append(package[i])
            self.size += 1

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

    def listofAddresses(self):
        listt = []
        for i in self.currentHaul:
            listt.append(i[0])
        return listt

    # finds and returns indexes of 2 addresses
    def nearest_neighbor_deliver(self, start):
        num_locations = len(self.matrix)
        visited = set()
        path = [start[0]]
        current_location = start
        for _ in range(num_locations - 1):
            nearest_location = self.find_nearest_neighbor(current_location, visited)
            path.append(nearest_location)
            visited.add(nearest_location)
            current_location = nearest_location

    def find_nearest_neighbor(self, current_location, visited):
        pass

    def findTheAdresses(self, addresses):
        print()
        start = addresses[0][0]
        next_stop = addresses[1][0]
        start_miles = 0
        b = len(self.matrix) - 1
        a = 0
        next_stop_miles = 0
        popop = 0
        for j in range(b):
            if self.matrix[j][0] == start and a == 0:
                a = j
            if self.matrix[j][0] == next_stop:
                next_stop_miles = j
            if self.matrix[b - j][0] == next_stop:
                next_stop_miles = b - j
            if self.matrix[b - j][0] == start:
                a = b - j
        last_stop = next_stop_miles
        popop = self.matrix[a][next_stop_miles]
        for z in addresses:
            if z[0] == start:
                continue
            else:
                next_stop = z[0]
                for f in range(int(b / 2) - 2):
                    if self.matrix[f][0] == next_stop:
                        last_stop = f
                        break
                    if self.matrix[b - f][0] == next_stop:
                        last_stop = b - f
                        break
                c = self.matrix[a][last_stop]
                if popop > c:
                    popop = c
                    start_miles = last_stop
        print(self.matrix[start_miles][0], " ", popop)


"""
    def findTheAddresses(self,  adresses):
        poopo = []
        start = adresses[0]
        nearest_location = adresses[1]
        # Grabs the location of the required cell
        for k in range(0, 26):
            if self.matrix[k][0] == start:
                poopo.append(k)
            if self.matrix[k][0] == nearest_location:
                print(self.matrix[k][0] == addressTwo)
                poopo.append(k)
            if len(poopo) > 2:
                break

        return poopo
"""
