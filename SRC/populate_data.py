import sys
import csv
import time
from helpers import swap_file_writer
from generator import ContactGenerator

# Order of operations, according to schema precedence order:
# 1. Contact
# 2. Role
# 3. Company
# 4. EmployeeRole
# 5. Branch
# 6. Employee
# 7. Payroll
# 8. TaxForm

f = open('data/out/identities.csv', 'w')
fw = csv.writer(f, dialect="unix")

contact_gen = ContactGenerator(int(sys.argv[1]))

contacts = contact_gen.get_identities()

fw.writerow(contact_gen.get_identities_header())
for line in contacts:
    print(line)
    fw.writerow(line)

# if len(sys.argv) > 2:
#     if sys.argv[2] == "-v":
#         print(f'Statistics:\nTotal time taken: {}')

# nl_to_ns, percent_error = gen.get_nl_to_ns_ratio()
# print(f'NL-to-NS ratio: {nl_to_ns:.2f}\nPercent Error: {percent_error:.2f}%')
