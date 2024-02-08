import csv
import hasTable


class Parse:
    def __init__(self):
        self.myList = []
        self.obj = hasTable.HasTable(40)
        self.ipp = 0

#returns the size of the hashTable
    def size(self):
        return self.obj.__len__()

#Opens the file and splits the list then adds it to the hash table. Ignores "," between quotemarks
    def readfiles(self, file):
        with open(file) as f:
            toParse = csv.reader(f, delimiter=',', quotechar="\"")
            for line in toParse:
                self.obj.insert(int(line[0]), line[1:])

#checks to see if the package must be delivered with another package
    def Bundle(self):
        Bundle = []
        i = 1
        o = 0
        while i in range(40):
            if self.obj.contains(i) and "Must be delivered" in self.obj.search(i)[6]:
                a = self.obj.search(i)[6].replace("Must be delivered with ", "")
                # print(a)
                b = a.split(", ")
                c = int(b[0])
                d = int(b[1])
                Bundle.append(self.obj.search(i))
                self.obj.remove(i)
                if self.obj.contains(c):
                    Bundle.append(self.obj.search(c))
                    self.obj.remove(c)
                    i += 1

                if self.obj.contains(d):
                    Bundle.append(self.obj.search(d))
                    self.obj.remove(d)
                    i += 1

            else:
                i += 1

        return Bundle

#checks to see if the package is delayed
    def Bundle2(self):
        Bundle22 = []
        i = 1
        while i in range(40):
            if self.obj.contains(i) and "Delayed" in self.obj.search(i)[6]:
                Bundle22.append(self.obj.search(i))
                self.obj.remove(i)
                i += 2
            else:
                i += 1
        return Bundle22

#checks to see if the package can only be delivered on a specific truck
    def onlyTruck(self):
        Bundle33 = []

        for i in range(40):
            if self.obj.contains(i) and "Can " in self.obj.search(i)[6]:
                Bundle33.append(self.obj.search(i))
                self.obj.remove(i)
            elif self.obj.contains(self.obj.size - i) and "Can " in self.obj.search(self.obj.size - i)[5]:
                Bundle33.append(self.obj.size - i)
                self.obj.remove(self.obj.size - i)

        return Bundle33

#prints all the packages in the original table
    def printIt(self):
        for i in range(40):
            if self.obj.contains(i):
                print(self.obj.search(i), " ", i)

#returns the first available package
    def returnLine(self):
        dd = self.obj.contains(self.ipp)
        while not dd:
            self.ipp += 1
            dd = self.obj.contains(self.ipp)
        ded=self.obj.search(self.ipp)
        self.obj.remove(self.ipp)
        return ded
