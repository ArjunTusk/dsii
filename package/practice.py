import csv

import hasTable

List = []
rows = []
i = 0
n = 0
x = 0
c = ""
no = False
obj = hasTable.HasTable(9)

j = 0
with open('WGUPS Package File.csv') as f:
    for line in f:
        if i > 3:
            # strip whitespace
            line = line.strip()
            # separate the columns
            line = line.split(',')
            # save the line for use later
            if len(line) == 9:
                line[7] = line[7] + line[8]
                line.pop()
            List.append(line)
            obj.insert(line[0], List)
            nokia = line[1] + "," + line[2] + "," + line[3] + "," + line[4]
        else:
            i += 1
w, h = 28, 28
Matrix = [["0" for x in range(w)] for y in range(h)]
# save the line for use later

with open('WGUPS Distance Table.csv') as a:
    spam = csv.reader(a, delimiter=',', quotechar="\"")
    for linee in spam:
        if j > 0:

            x += 1
            for m in range(x):
                Matrix[n][m] = linee[m].replace("\n", "")
            n += 1
        j += 1
