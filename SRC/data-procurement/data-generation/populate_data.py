import sys
import csv
from helpers import TimeAnalysis
from generator import ContactGenerator, BranchGenerator

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

f = open('data/out/raw/branches-with-contact.csv', 'w')
fw = csv.writer(f, dialect="unix")

branch_gen = BranchGenerator(300)
branches = branch_gen.get_branches()

fw.writerow(branch_gen.get_branch_header())
for line in branches:
    fw.writerow(line)

f.close()
f = open('data/out/raw/identities.csv', 'w')
fw = csv.writer(f, dialect="unix")

t.new_stage("Generation")
contact_gen = ContactGenerator(int(sys.argv[1]), int(sys.argv[2])) # second one is company_pay_freq
contacts = contact_gen.get_identities()
t.end_stage()
t.add_child(contact_gen.get_time(), "Generation")

contacts = branch_gen.assign_branches(contacts)
t.new_stage("Writing")
fw.writerow(branch_gen.get_identities_header())
for line in contacts:
    fw.writerow(line)
t.end_stage()

f= open('data/out/raw/payroll-items.csv', 'w')
fw = csv.writer(f, dialect="unix")
payrolls = contact_gen.get_payrolls()

t.new_stage("Payroll Writing")
fw.writerow(contact_gen.get_payroll_header())
for line in payrolls:
    fw.writerow(line)
t.end_stage()

f.close()
f = open('data/out/raw/tax_forms.csv', 'w')
fw = csv.writer(f, dialect='unix')

tax_forms = contact_gen.get_tax_forms()

t.new_stage("TaxForm Writing")
fw.writerow(contact_gen.get_tax_form_header())
for line in tax_forms:
    fw.writerow(line)
t.end_stage()
f.close()

if len(sys.argv) > 3:
    if sys.argv[3] == "-v":
        t.print_stats()
# nl_to_ns, percent_error = gen.get_nl_to_ns_ratio()
# print(f'NL-to-NS ratio: {nl_to_ns:.2f}\nPercent Error: {percent_error:.2f}%')
