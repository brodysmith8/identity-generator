import names  # random name generator pip package
import random
import csv
import generator_types as gt
import datetime 
import helpers as h

class ContactGenerator:
    def __init__(self, n_employees, company_pay_frequency) -> None:
        self._n = n_employees
        self.cpf = company_pay_frequency
        self.addresses = None  # should really declare all member variables eventually
        self.IdentitiesData = self._generate_identities()

    def __str___(self) -> str:  # toString
        return str(id)

    # generates names and sequential serial #s. They don't have to stay in sequential order in the db though
    def _generate_people(self) -> gt.People:
        people = []
        for x in range(self._n):
            [fname, lname] = names.get_full_name().split(" ")
            people.append([x + 1, fname, lname])

        return people

    # code inspired by wealthsimple's public domain SIN generator:
    # https://github.com/wealthsimple/social-insurance-number/blob/master/social-insurance-number.js
    # also has capability to generate business number (BN), which is like a SIN number for a company
    def _generate_sin(self) -> gt.Sin:
        SIN_LENGTH = 9

        TEMPORARY_RESIDENT_FIRST_DIGIT = 9
        BUSINESS_NUMBER_FIRST_DIGIT = 8
        PROVINCES = {
            "AB": [6],
            "BC": [7],
            "MB": [6],
            "NB": [1],
            "NL": [1],
            "NS": [1],
            "NT": [6],
            "NU": [6],
            "ON": [4, 5],
            "PE": [1],
            "QC": [2, 3],
            "SK": [6],
            "YT": [7]
        }
        PROVINCES_LONG_TO_SHORT = {
            "Alberta": "AB",
            "British Columbia": "BC",
            "Manitoba": "MB",
            "New Brunswick": "NB",
            "Newfoundland and Labrador": "NL",
            "Nova Scotia": "NS",
            "Northwest Territories": "NT",
            "Nunavut": "NU",
            "Ontario": "ON",
            "Prince Edward Island": "PE",
            "Quebec": "QC",
            "Saskatchewan": "SK",
            "Yukon": "YT",
        }

        def intarr_to_strarr(int_arr):
            for num in range(len(int_arr)):
                int_arr[num] = str(int_arr[num])
            return int_arr

        def starts_with(business, temp_res, province):
            prov = PROVINCES_LONG_TO_SHORT[province]
            sin = []

            if business:
                sin.append(BUSINESS_NUMBER_FIRST_DIGIT)
            elif temp_res:
                sin.append(TEMPORARY_RESIDENT_FIRST_DIGIT)
            else:
                sin.append(PROVINCES[prov][0])

            return sin

        def luhn_checksum(sin):
            l = SIN_LENGTH
            mul = 0
            luhn_arr = [
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
            ]
            sum = 0
            l -= 1
            while l > 0:
                # there is a "base 10" arg here for js. Not sure why because it's only one digit?
                sum += luhn_arr[mul][int(sin[l])]
                mul = mul ^ 1
                l -= 1
            return sum % 10

        def check_digit(sin_arr):
            sin_arr = intarr_to_strarr(sin_arr)
            checksum = luhn_checksum("".join(sin_arr) + "0")
            return 0 if checksum % 10 == 0 else (10 - checksum)

        sin_arr = starts_with(False, False, "Newfoundland and Labrador")

        while len(sin_arr) < (SIN_LENGTH - 1):
            sin_arr.append(random.randint(0, 9))

        sin_arr.append(check_digit(sin_arr))
        sin_arr = intarr_to_strarr(sin_arr)

        return "".join(sin_arr)

    def _generate_sins(self) -> gt.Sins:
        sins = []
        for sin in range(self._n):
            sins.append(self._generate_sin())
        return sins

    # definitely can slim this method down + clean it up
    # list[int, int, str, str, str, str, str, int])
    def _generate_addresses(self) -> gt.Addresses:
        # Stage three: post code LDUs (second part 0A0)
        def safe_increment_pcode_number(num):
            num += 1
            m_num = num % 10
            if num == 10 and m_num == 0:
                num = 0
            return num

        # this is sooooo classy
        # X -> Y -> Z -> A -> B
        def safe_increment_pcode_letter(let):
            return chr((ord(let) + 1 - 65) % 26 + 65)

        # I hate this so much
        def generate_ldu(last_ldu):
            f_let, m_let, l_num = list(last_ldu)
            l_num = safe_increment_pcode_number(int(last_ldu[2]))
            if l_num == 0:
                m_let = safe_increment_pcode_letter(last_ldu[1])
                if m_let == 'A':
                    f_let = safe_increment_pcode_number(int(last_ldu[0]))
            return f'{f_let}{m_let}{l_num}'

        def generate_random_ldu():
            # kinda random ldu that isn't too high
            return generate_ldu(f'{random.randint(0,3)}{chr(random.randint(65,90))}0')

        addresses = []

        f = open('data/in/street-names-and-frequency-modified.csv')
        fr = csv.reader(f, dialect="unix")

        f_ss = open('data/in/street-suffixes.csv')
        fr_ss = csv.reader(f_ss, dialect="unix")

        # Stage one: street number, street name
        for x in range(self._n):
            rng = random.random()
            for line in fr_ss:
                street_suffix, _, _, c_sum = line
                if float(c_sum) > rng:
                    f_ss.seek(0)
                    break

            rng = random.random() * 100
            next(f, None)  # skip header
            for line in fr:
                street_name, _, cfreq = line
                if float(cfreq) > rng:
                    addresses.append([random.randint(1, 999),
                                      f'{street_name} {street_suffix}',
                                      None,
                                      None,
                                      None,
                                      'Canada'])  # hardcoded just for example
                    f.seek(0)  # return to beginning
                    break

        f.close()
        f_ss.close()

        # Stage two: city, province, country
        # better way to select these but given that we only have data for these two this is fine
        f_ns = open('data/in/nova-scotia-population-modified.csv')
        fr_ns = csv.reader(f_ns, dialect="unix")

        f_nl = open('data/in/newfoundland-population-modified.csv')
        fr_nl = csv.reader(f_nl, dialect="unix")

        f_p = open('data/in/provinces.csv')
        fr_p = csv.reader(f_p, dialect="unix")

        count_nl = 0
        count_ns = 0
        for x in range(self._n):
            rng = random.random()
            for line in fr_p:
                if float(line[2]) > rng:
                    current_province = line[0]
                    f_p.seek(0)
                    break

            rng = rng * 100  # once again will never reach 100%
            if current_province == 'Nova Scotia':
                count_ns += 1 
                for line in fr_ns:
                    city_name, _, _, cumulative_population, fsa = line
                    if float(cumulative_population) > rng:
                        addresses[x][2] = city_name
                        addresses[x][3] = current_province
                        addresses[x][4] = fsa
                        f_ns.seek(0)
                        break
            else:
                count_nl += 1
                for line in fr_nl:
                    city_name, _, _, cumulative_population, fsa = line
                    if float(cumulative_population) > rng:
                        addresses[x][2] = city_name
                        addresses[x][3] = current_province
                        addresses[x][4] = fsa
                        f_nl.seek(0)
                        break

        f_nl.close()
        f_ns.close()
        f_p.close()
        self.nl_to_ns_ratio = float(count_nl) / float(1 or count_ns)
        fsa_ldu = dict()  # { FSA : [generated LDUs] }

        for address in addresses:
            fsa = address[4]
            if fsa in fsa_ldu:  # at least one generated code
                # (roughly) 1/3 chance of a new code generation
                rng = random.random()
                if rng < 0.3334:
                    l_ldu = fsa_ldu[fsa][-1]  # get last gen'd LDU
                    n_ldu = generate_ldu(l_ldu)
                    fsa_ldu[fsa].append(n_ldu)
                    address[4] = f'{fsa} {n_ldu}'
                else:
                    l_ldu = fsa_ldu[fsa][-1]  # get last gen'd LDU
                    address[4] = f'{fsa} {l_ldu}'
            else:  # generate a random LDU for the FSA
                ldu = generate_random_ldu()
                fsa_ldu[fsa] = [ldu]
                address[4] = f'{fsa} {ldu}'

        # street num, street name, city, province, postal code, country
        return addresses

    def get_addresses(self) -> gt.Addresses:
        return self._generate_addresses()

    def get_nl_to_ns_ratio(self):
        expected = 460993.0 / 969383.0
        return [self.nl_to_ns_ratio, abs(expected - self.nl_to_ns_ratio) / expected * 100]

    # needs addresses to be run first
    # this is terrible
    def _generate_phone_numbers(self) -> gt.PhoneNumbers:
        if self.addresses == None:
            return

        AREA_CODES = {
            "Newfoundland and Labrador": "709",
            "Nova Scotia": "902"
        }
        
        # area code : { first3digits : {last4digits} } constant lookup time baybeeeee
        digits = dict()

        phone_numbers = []
        for address in self.addresses:
            prov = address[3]
            curr_num = ""
            for num in AREA_CODES[prov]:
                curr_num += num

            first = AREA_CODES[prov]
            second = ""
            third = ""

            no_nums = 0

            # first three digits
            if curr_num in digits:
                while (True):  # bad solution
                    if no_nums == 1:
                        break

                    random_first_three = f'{random.randint(1,9)}{random.randint(0,9)}{random.randint(0,9)}'

                    choice = random.choices([True, False], [3, 1])[0] # chance the number is the same (xxx) xxx-
                    if choice or random_first_three in digits[curr_num]:
                        # if the first three aren't already in the dictionary, pick a random one that is in the dictionary
                        if not random_first_three in digits[curr_num]:
                            random_first_three = random.choice(
                                tuple(digits[curr_num]))  # this is a slow line

                        # generate last four
                        random_last_four = f'{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}'
                        if random_last_four in digits[curr_num][random_first_three]:
                            pass
                        else:
                            digits[curr_num][random_first_three].add(
                                random_last_four)
                            second = random_first_three
                            third = random_last_four
                            no_nums += 1

                    else:
                        digits[curr_num][random_first_three] = set()
                        random_last_four = f'{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}'
                        digits[curr_num][random_first_three].add(
                            random_last_four)
                        second = random_first_three
                        third = random_last_four
                        no_nums += 1
                        break
            else:
                # don't make the first one too high
                random_first_three = f'{random.randint(1,2)}{random.randint(0,5)}{random.randint(0,9)}'
                digits[curr_num] = {random_first_three: set()}

                random_last_four = f'{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}'
                digits[curr_num][random_first_three].add(random_last_four)

                second = random_first_three
                third = random_last_four

            phone_numbers.append(f'({first}) {second}-{third}') # 1:1 mapping with addresses
        return phone_numbers

    def _generate_bank_numbers(self):
        nums = []
        nums_all = []
        f = open('data/in/bank-institution-number.csv')
        fr = csv.reader(f, dialect="unix")
        for line in fr:
            nums.append(line[1])
        
        for x in range(self._n):
            institu = f'{random.choice(nums)}'
            transit = f'{random.randint(10000,99999)}'

            account = ""
            for x in range(7):
                account+=f'{random.randint(0,9)}'
            nums_all.append([institu, transit, account])
        return nums_all

    def _generate_start_dates(self):
        dates = []
        gauss = h.get_gauss()
            
        for x in range(self._n):
            year = 0
            rng = random.random()
            for line in gauss:
                if float(line[1]) > rng:
                    year = int(line[0])
                    break
            y = year
            d = random.randint(1, 27)
            m = random.randint(1,12)
            dates.append(datetime.date(y, m, d))
        return dates

    def _generate_identities(self) -> gt.Identities:
        self.people = self._generate_people()
        self.addresses = self._generate_addresses()
        self.phone_numbers = self._generate_phone_numbers()
        self.sins = self._generate_sins()
        self.roles = self._generate_job_titles()
        self.bank_numbers = self._generate_bank_numbers()
        self.start_dates = self._generate_start_dates()
        self.payrolls = self._generate_payrolls()
        self.tax_forms = self._generate_tax_forms()

        gen_e_addr = lambda x, y: f'{x[0].lower()}{y.lower()}{random.randint(0,999)}@nci.ca'
        arr = []
        # Employee_ID, Phone_Number, Branch_ID, Employee_First_Name, Employee_Last_Name, Employee_Start_Date, Employee_SIN, Employee_Bank_Account_Number, Employee_Bank_Transit_Number, Employee_Bank_Institution_Number, Company_Name
        for x in range(self._n):
            arr.append([
                self.people[x][0], #    0. job id
                self.people[x][1], #    1. fname
                self.people[x][2], #    2. lname
                self.roles[x][0], #        3. job
                self.addresses[x][0], # 4. st num
                self.addresses[x][1], # 5. st name
                self.addresses[x][2], # 6. city
                self.addresses[x][3], # 7. province
                self.addresses[x][4], # 8. post code
                self.addresses[x][5], # 9. country
                self.phone_numbers[x],#10. phone number
                gen_e_addr(self.people[x][1], self.people[x][2]), # 11. email_address
                self.sins[x], # 12. sin number
                "New Canada Incorporated", # 13. company_name
                self.bank_numbers[x][0], # 14. institute number
                self.bank_numbers[x][1], # 15. transit numberz
                self.bank_numbers[x][2], # 16. account number
                self.start_dates[x] # 17. start dates 
            ])

        return arr

    def _generate_job_titles(self) -> gt.Roles:
        f = open('data/in/job-positions.csv')
        fr = csv.reader(f, dialect="unix")
        all_roles = []
        roles = []
        for role in fr:
            all_roles.append([role[1], role[2]])
        for line in range(self._n):
            rng = random.randint(0, len(all_roles) - 1)
            roles.append([all_roles[rng][0], all_roles[rng][1]])
        return roles

    def get_identities(self) -> gt.Identities:
        return self.IdentitiesData

    def get_identities_header(self):
        return [ "id", "first_name", "last_name", "role_name", "street_number", "street_name", "city", "province", "postal_code", "country", "phone_number", "email_address", "sin", "company_name", "institution_number", "transit_number", "account_number", "start_date", "salary"] # use sin as seed for employee_number? 

    def get_phone_numbers(self) -> gt.PhoneNumbers:
        return self.phone_numbers

    def _generate_pay_dates(self, start, n, cpf):
        d = start
        d_l = []
        for x in range(n):
            d += datetime.timedelta(days=cpf)
            d_l.append(d)
        return d_l

    # Payroll_ID, Payment_Date, [Employee_ID, Payment_Salary, Payment_Bonus], Payment_Status
    def _generate_payroll(self, e_id, salary, cpf):
        return [e_id, float(salary)/(365.0 / cpf), float(random.randint(0, 4500))] 

    # get employee start date, generate a payroll object every company_pay_frequency, 
    # sort chronologically, assign payroll_ids, return
    def _generate_payrolls(self): 
        company_pay_freq = self.cpf
        status = lambda x, y: "Pending Clearance" if (x - y).days < random.randint(1,4) else "Cleared" # between 1 and 4 business days :^)

        payrolls = []
        idx = 0
        for start_date in self.start_dates:
            e_id = self.people[idx][0]
            e_role = self.roles[idx]
            today = datetime.date.today()
            new_date = datetime.date(2022,8,start_date.day) # hardcoded august 
            n = int((today - new_date).days / company_pay_freq)

            pay_dates = self._generate_pay_dates(new_date, n, company_pay_freq) 

            for pay_date in pay_dates:
                # Payroll_ID, Payment_Date, Employee_ID, Payment_Salary, Payment_Bonus, Payment_Status
                pr = self._generate_payroll(e_id, e_role[1], company_pay_freq)
                payrolls.append([0, pay_date, pr[0], f'{pr[1]:.2f}', f'{pr[2]:.2f}', status(today, pay_date)]) # e_role[1] is salary
            
            idx +=1 

        payrolls.sort()
        for x in range(len(payrolls)):
            payrolls[x][0] = f'{8405283 + x}' 

        return payrolls


    def get_payrolls(self):
        return self.payrolls

    def get_payroll_header(self):
        return ["Payroll_ID", "Payment_Date", "Employee_ID", "Payment_Salary", "Payment_Bonus", "Payment_Status"]

    def _validate_employee(self, idx, start_date):
        return "Valid" if self.start_dates[idx] == start_date else "Invalid"

    # Tax_Form_ID, Employee_ID, Tax_Year, Tax_Form_URL
    def _generate_tax_forms(self):
        # every employee has a tax form on file from the last year,
        # except the people who started working here this year (a tax year is jan1 to dec31)
        tax_forms = []
        idx = 0
        idx_2 = 0
        start_dates = {}
        for start_date in self.start_dates:
            if start_date.year in start_dates:
                start_dates[start_date.year] +=1
            else:
                start_dates[start_date.year] = 1

            if start_date <= datetime.date(2020, 1, 1): 
                #validation = self._validate_employee(idx, start_date)
                tax_forms.append([f'{853948 + idx_2}', idx + 1, 2020, f'https://nci.ca/taxes/{853948 + idx_2}_{2020}'])
                idx_2 +=1
            
            idx+=1
        idx = 0
        for start_date in self.start_dates:
            if start_date <= datetime.date(2021, 1, 1):
                #validation = self._validate_employee(idx, start_date)
                tax_forms.append([f'{853948 + idx_2}', idx + 1, 2021, f'https://nci.ca/taxes/{853948 + idx_2}_{2021}'])
                idx_2 +=1
            idx+=1

        return tax_forms

    def get_tax_forms(self):
        return self.tax_forms

    def get_tax_form_header(self):
        return ["Tax_Form_ID", "Employee_ID", "Tax_Year", "Tax_Form_URL"]

class BranchGenerator:
    def __init__(self, n) -> None:
        self._n = n
        self._contact_generator = ContactGenerator(n, 14)
        self.identities = self._contact_generator.get_identities()
        self.addresses = self._contact_generator.get_addresses()
        self.phone_nos = self._contact_generator.get_phone_numbers()
        self.branches = self._generate_branches()

    def _generate_branches(self):
        # can edit emails for contact in here
        branches = []
        for x in range(self._n):
            branches.append([
                x + 1, 
                self.phone_nos[x], 
                self.identities[x][13],
                self.addresses[x][0],
                self.addresses[x][1],
                self.addresses[x][2],
                self.addresses[x][3],
                self.addresses[x][4],
                self.addresses[x][5],
                ])
        return branches

    def get_branches(self):
        return self.branches

    def get_branch_header(self):
        # street num, street name, city, province, postal code, country
        return ["id", "company_name", "phone_number", "street_number", "street_name", "city", "province", "postal_code", "country"]

    def assign_branches(self, identities: gt.Identities):
        idx = 0
        branch_ids = []
        for b in self.branches:
            branch_ids.append(b[0])
        for identity in identities:
            identity.append(random.choice(branch_ids))
            idx+=1
        return identities

    def get_identities_header(self) -> list[str]:
        return ["id", "first_name", "last_name", "role_name", "street_number", "street_name", "city", "province", "postal_code", "country", "phone_number", "email_address", "sin", "company_name", "institution_number", "transit_number", "account_number", "start_date", "salary", "branch_id"]