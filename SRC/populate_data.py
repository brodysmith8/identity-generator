import sys
import csv
from helpers import TimeAnalysis
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

t = TimeAnalysis()

f = open('data/out/identities.csv', 'w')
fw = csv.writer(f, dialect="unix")

t.new_stage("Generation")
contact_gen = ContactGenerator(int(sys.argv[1]))
contacts = contact_gen.get_identities()
t.end_stage()

t.new_stage("Writing")
fw.writerow(contact_gen.get_identities_header())
for line in contacts:
    fw.writerow(line)
t.end_stage()

if len(sys.argv) > 2:
    if sys.argv[2] == "-v":
        print("\nStatistics:")
        stats = t.get_stats()
        for stat in stats:
            print(stat)
# nl_to_ns, percent_error = gen.get_nl_to_ns_ratio()
# print(f'NL-to-NS ratio: {nl_to_ns:.2f}\nPercent Error: {percent_error:.2f}%')
