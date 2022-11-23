import csv
import random 

ht = {}

for x in range(10000):
    curr = int(random.gauss(2020, 6))
    if curr in ht:
        ht[curr] += 1
    else:
        ht[curr] = 1

li = []
idx = 0
for num in list(ht):
    li.append([num, ht[num]])
li.sort()

li_y = []
sum = 0
for num in li:
    if num[0] <= 2022:
        sum += num[1]
        li_y.append([num[0], num[1]])

f = open('../gauss-lookup-table.csv', 'w')
fw = csv.writer(f, dialect="unix")
cumsum = 0
for line in li_y:
    fraction_of_sum = line[1] / sum
    cumsum += fraction_of_sum
    line.append(fraction_of_sum)
    line.append(cumsum)
    fw.writerow(line)