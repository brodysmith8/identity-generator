import sys
import time
from helpers import swap_file_writer
from generator import Generator

# Order of operations, according to schema precedence order:
# 1. Contact
# 2. Role
# 3. Company
# 4. EmployeeRole
# 5. Branch
# 6. Employee
# 7. Payroll
# 8. TaxForm

# if we first generate a table of people with addresses we are good to do other stuff later

n = int(sys.argv[1])  # how many records we generate
[f, fw] = swap_file_writer('data/out/people.csv')

time_before = time.time()
identities = Generator(n).get_identities()
time_end = time.time()
print(f"total people generation time: {time_end - time_before:.2f} s")

# print people in the CSV to clear reference to people now so program uses less memory
# print('outputting people batch to csv...')
# fw.writerow(["employee_id", "employee_first_name", "employee_last_name"])
# for x in people:
#     [id, fn, ln] = x.split(' ')
#     fw.writerow([int(id), fn, ln])

# f, fw = swap_file_writer('data/out/other.csv', f, fw)
# fw.writerow("abcs")
