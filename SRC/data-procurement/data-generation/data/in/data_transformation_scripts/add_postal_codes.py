# add postal codes to NS and NL province data
import csv
import string

# A for NL, B for NS 
first_letter = 'B'

alphabet = list(string.ascii_uppercase)

def last_two_digits(a, h):
    res = a % 10
    if a >= 10 and res == 0:
        h+=1
    return [res, h]

f_name = '../nova-scotia-population-modified.csv'

f = open(f_name)
f_r = csv.reader(f, dialect='unix')
f_li = list(f_r)
f.close()
f_w = open(f_name, 'w')
fw = csv.writer(f_w, dialect="unix")

idx = 0
h = 0
for line in f_li:
    a, h = last_two_digits(idx, h)
    fw.writerow([line[0], line[1], line[2], line[3], f'{first_letter}{a}{alphabet[h]}'])
    idx+=1

f_w.close()