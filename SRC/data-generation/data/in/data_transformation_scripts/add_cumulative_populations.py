# find totals of NL and NS population, convert to %,
# then add cumulative pop

import csv

f = open('../source/nova-scotia-population.csv')
fwrite = open('../nova-scotia-population-modified.csv', 'w')
fw = csv.writer(fwrite, dialect="unix")
copy = []

sum = 0
for line in f: 
    city, pop = line.split(',')
    copy.append([city, pop])
    sum += int(pop)

print(sum)
f.close()
second = lambda l : int(l[1])
copy.sort(key=second, reverse=True) # sort from asc to desc

c_sum = 0.0
for line in copy:
    local_sum = float(line[1]) / float(sum) * 100.0
    c_sum += local_sum
    fw.writerow([line[0], line[1][:-1], local_sum, c_sum])


fwrite.close()