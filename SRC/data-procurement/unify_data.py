# have: 6 tables
# branches-with-contact("branch_id","company_name","phone_number","email_address","street_number","street_name","city","province","postal_code","country")

#               0               1           2           3           4               5           6         7         8           9           10          11              12       13          14                   15              16              17          18           19                                                            
# identities("employee_id","first_name","last_name","role_name","role_id","street_number","street_name","city","province","postal_code","country","phone_number","email_address","sin","company_name","institution_number","transit_number","account_number","start_date","branch_id")
# payroll-items("payroll_id","payment_date","employee_id","payment_salary","payment_bonus","payment_status")
# tax_forms("tax_form_id","employee_id","tax_year","tax_form_url")
# data/in/companies-with-address(company_name, phone_number, company_pay_frequency, company_domain_name, "email_address", "street_number","street_name","city","province","postal_code","country")
# data/in/job-positions(role_id,role_name,salary)

# need: 8 tables "branch_id","company_name","phone_number","email_address","street_number","street_name","city","province","postal_code","country"
# Contact(Phone_Number, Email_Address, Street_Number, Street_Name, City, Province, Post_Code, Country)
#   -> get all info from branches-with-contact [2][3][4][5][6][7][8][9], identities[10][11][4][5][6][7][8][9], companies-with-address[1][4][5][6][7][8][9][10]. These are the only things that have contact info. 
# Role(Role_ID, Role_Name, Salary)
#   -> copy job-positions
# Company(Company_Name, Phone_Number, Company_Pay_Frequency, Company_Domain_Name)
#   -> copy [0][1][2][3] of companies-with-address
# EmployeeRole(Employee_ID, Role_ID)
#   -> copy identities [0][4]
# Branch(Branch_ID, Phone_Number, Company_Name)
#   -> copy branches-with-contact[0][2][1]
# Employee(Employee_ID, Phone_Number, Branch_ID, Employee_First_Name, Employee_Last_Name, Employee_Start_Date, Employee_SIN, Employee_Bank_Institution_Number, Employee_Bank_Transit_Number, Employee_Bank_Account_Number, Company_Name)
#   -> copy identities[0][11][20][1][2][18][13][15][16][17][14]
# Payroll(Payroll_ID, Payment_Date, Employee_ID, Payment_Salary, Payment_Bonus, Payment_Status)
#   -> copy payroll-items
# TaxForm(Tax_Form_ID, Employee_ID, Tax_Year, Tax_Form_URL)
#   -> copy tax_forms

import csv 
import random

f_i_branches = open('data-generation/data/out/raw/branches-with-contact.csv')
f_ir_branches = csv.reader(f_i_branches, dialect='unix')
next(f_ir_branches) # skip header
f_i_identities = open('data-generation/data/out/raw/identities.csv') 
f_ir_identities = csv.reader(f_i_identities, dialect='unix')
next(f_ir_identities)
f_i_companies = open('data-generation/data/in/companies-with-address.csv')
f_ir_companies = csv.reader(f_i_companies, dialect='unix')

# Contact(phone_number, email_address, street_number, street_name, city, province, post_code, country)
f_o = open('../contact.csv', 'w')
f_ow = csv.writer(f_o, dialect="unix")

f_ow.writerow(["phone_number", "email_address", "street_number", "street_name", "city", "province", "post_code", "country"])
lines = []
for line in f_ir_branches:
    lines.append([line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9]])
f_i_branches.seek(0)
next(f_i_branches)

for line in f_ir_identities:
    lines.append([line[11],line[12],line[5],line[6],line[7],line[8],line[9], line[10]])
f_i_identities.seek(0)
next(f_ir_identities)

for line in f_ir_companies:
    lines.append([line[1],line[4],line[5],line[6],line[7],line[8],line[9],line[10]])
f_i_companies.seek(0)

random.shuffle(lines)
f_ow.writerows(lines)
f_o.close()

# Role(Role_ID, Role_Name, Salary)
f_o = open('../role.csv', 'w')
f_ow = csv.writer(f_o, dialect="unix")

f_i_roles = open('data-generation/data/in/job-positions.csv')
f_ir_roles = csv.reader(f_i_roles, dialect='unix')

f_ow.writerow(["role_id", "role_id", "salary"])
for line in f_ir_roles:
    f_ow.writerow([line[0],line[1],line[2]])
f_i_roles.close()

# Company(Company_Name, Phone_Number, Company_Pay_Frequency, Company_Domain_Name)
# already made

# EmployeeRole(employee_id, role_id)
f_o = open('../employee_role.csv', 'w')
f_ow = csv.writer(f_o, dialect="unix")

f_ow.writerow(["employee_id", "role_id"])
for line in f_ir_identities:
    f_ow.writerow([line[0],line[4]])
f_i_identities.seek(0)
next(f_i_identities)
f_o.close()

# Branch(Branch_ID, Phone_Number, Company_Name)
f_o = open('../branch.csv', 'w')
f_ow = csv.writer(f_o, dialect="unix")

f_ow.writerow(["branch_id", "phone_number", "company_name"])
for line in f_ir_branches:
    f_ow.writerow([line[0],line[2], line[1]])
f_i_branches.close()
f_o.close()

# Employee(Employee_ID, Phone_Number, Branch_ID, Employee_First_Name, Employee_Last_Name, Employee_Start_Date, Employee_SIN, Employee_Bank_Institution_Number, Employee_Bank_Transit_Number, Employee_Bank_Account_Number, Company_Name)
f_o = open('../employee.csv', 'w')
f_ow = csv.writer(f_o, dialect="unix")

f_ow.writerow(["employee_id", "phone_number", "branch_id", "employee_first_name", "employee_last_name", "employee_start_date", "employee_sin", "employee_bank_institution_number", "employee_bank_transit_number", "employee_bank_account_number", "company_name"])
for line in f_ir_identities:
    f_ow.writerow([line[0],line[11],line[19],line[1],line[2],line[18],line[13], line[15],line[16],line[17],line[14]])
f_i_identities.close()
f_o.close()

# Payroll(Payroll_ID, Payment_Date, Employee_ID, Payment_Salary, Payment_Bonus, Payment_Status)
f_i_payrolls = open('data-generation/data/out/raw/payroll-items.csv')
f_ir_payrolls = csv.reader(f_i_payrolls, dialect = 'unix')
next(f_ir_payrolls)

f_o = open('../payroll.csv', 'w')
f_ow = csv.writer(f_o, dialect='unix')

f_ow.writerow(["payroll_id", "payment_date", "employee_id", "payment_salary", "payment_bonus", "payment_status"])
for line in f_ir_payrolls:
    f_ow.writerow([line[0],line[1],line[2],line[3],line[4], line[5]])
f_o.close()
f_i_payrolls.close()

# TaxForm(Tax_Form_ID, Employee_ID, Tax_Year, Tax_Form_URL)
f_i_tax_form = open('data-generation/data/out/raw/tax_forms.csv')
f_ir_tax_form = csv.reader(f_i_tax_form, dialect="unix")

f_o = open('../tax_form.csv', 'w')
f_ow = csv.writer(f_o, dialect='unix')

f_ow.writerow(["tax_form_id", "employee_id", "tax_year", "tax_form_url"])
for line in f_ir_tax_form:
    f_ow.writerow([line[0], line[1], line[2], line[3]])
f_i_tax_form.close()