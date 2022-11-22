import sys
import csv
import helpers
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

#t = TimeAnalysis()

f = open('data/out/branches-with-contact.csv', 'w')
fw = csv.writer(f, dialect="unix")

branch_gen = BranchGenerator(10)
branches = branch_gen.get_branches()

fw.writerow(branch_gen.get_branch_header())
for line in branches:
    fw.writerow(line)

f.close()
f = open('data/out/identities.csv', 'w')
fw = csv.writer(f, dialect="unix")

#t.new_stage("Generation")
contact_gen = ContactGenerator(int(sys.argv[1]), int(sys.argv[2])) # second one is company_pay_freq
contacts = contact_gen.get_identities()
#t.end_stage()

contacts = branch_gen.assign_branches(contacts)
#t.new_stage("Writing")
fw.writerow(branch_gen.get_identities_header())
for line in contacts:
    fw.writerow(line)
#t.end_stage()

f= open('data/out/payroll-items.csv', 'w')
fw = csv.writer(f, dialect="unix")
payrolls = contact_gen.get_payrolls()
fw.writerow(contact_gen.get_payroll_header())
for line in payrolls:
    fw.writerow(line)

f.close()
f = open('data/out/tax_forms.csv', 'w')
fw = csv.writer(f, dialect='unix')
fw.writerow(contact_gen.get_tax_form_header())
tax_forms = contact_gen.get_tax_forms()
for line in tax_forms:
    fw.writerow(line)
f.close()
# if len(sys.argv) > 2:
#     if sys.argv[2] == "-v":
#         print("\nStatistics:")
#         stats = t.get_stats()
#         for stat in stats:
#             print(stat)
# nl_to_ns, percent_error = gen.get_nl_to_ns_ratio()
# print(f'NL-to-NS ratio: {nl_to_ns:.2f}\nPercent Error: {percent_error:.2f}%')
