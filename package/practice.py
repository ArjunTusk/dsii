class Truck:
    def __init__(self):
        self.currentHaul = []
        self.size = 0

    # Accepts a list and adds each item to the truck contained
    def add(self, package):
        for i in package:
            self.currentHaul.append(package)
            self.size += 1

    # Removes all packages at once
    def removePackage(self):
        for i in range(self.size):
            self.currentHaul.pop()
            self.size -= 1

    # Returns the amount of packages currently in the hall
    def sizeIt(self):
        return self.size

    # Prints what items are in the package
    def printHaul(self):
        for i in self.currentHaul:
            print(i)
