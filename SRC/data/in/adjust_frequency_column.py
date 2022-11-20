# converts "frequency" col, currently measured in number of 
# occurrances, to percentages of the sample. 

import csv

f = open('street-names-and-frequency.csv')
fr = csv.reader(f, dialect='unix')
sum = 0

copy = []
header=next(fr,None) # skip csv header
# get sum
for line in fr:
    copy.append([line[0]])
    sum+=int(line[1])    

f.seek(0)
next(fr,None) # skip csv header
sum = float(sum)
# make frequency a % of sum 
idx = 0
for line in fr:
    copy[idx].append(float(line[1]) / sum * 100.0)
    idx+=1

f.close()
f = open('street-names-and-frequency-modified.csv', 'w')
fw = csv.writer(f, dialect='unix')
fw.writerow(header)
for x in copy:
    fw.writerow(x)