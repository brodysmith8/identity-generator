import names  # random name generator pip package
import random
import csv
import generator_types as gt

class ContactGenerator:
    def __init__(self, n) -> None:
        self._n = n
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
                    addresses.append([0,  # suite number is 0 for people but something for businesses
                                      random.randint(1, 999),
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
                        addresses[x][3] = city_name
                        addresses[x][4] = current_province
                        addresses[x][5] = fsa
                        f_ns.seek(0)
                        break
            else:
                count_nl += 1
                for line in fr_nl:
                    city_name, _, _, cumulative_population, fsa = line
                    if float(cumulative_population) > rng:
                        addresses[x][3] = city_name
                        addresses[x][4] = current_province
                        addresses[x][5] = fsa
                        f_nl.seek(0)
                        break

        f_nl.close()
        f_ns.close()
        f_p.close()
        print(f'{count_nl} {count_ns}')
        self.nl_to_ns_ratio = float(count_nl) / float(count_ns)
        fsa_ldu = dict()  # { FSA : [generated LDUs] }

        for address in addresses:
            fsa = address[5]
            if fsa in fsa_ldu:  # at least one generated code
                # (roughly) 1/3 chance of a new code generation
                rng = random.random()
                if rng < 0.3334:
                    l_ldu = fsa_ldu[fsa][-1]  # get last gen'd LDU
                    n_ldu = generate_ldu(l_ldu)
                    fsa_ldu[fsa].append(n_ldu)
                    address[5] = f'{fsa} {n_ldu}'
                else:
                    l_ldu = fsa_ldu[fsa][-1]  # get last gen'd LDU
                    address[5] = f'{fsa} {l_ldu}'
            else:  # generate a random LDU for the FSA
                ldu = generate_random_ldu()
                fsa_ldu[fsa] = [ldu]
                address[5] = f'{fsa} {ldu}'

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
            prov = address[4]
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

    def _generate_identities(self) -> gt.Identities:
        self.people = self._generate_people()
        self.addresses = self._generate_addresses()
        self.phone_numbers = self._generate_phone_numbers()
        self.sins = self._generate_sins()

        arr = []
        for x in range(self._n):
            arr.append([
                self.people[x][0],
                self.people[x][1],
                self.people[x][2],
                self.phone_numbers[x],
                self.addresses[x][0],
                self.addresses[x][1],
                self.addresses[x][2],
                self.addresses[x][3],
                self.addresses[x][4],
                self.addresses[x][5],
                self.addresses[x][6],
                self.sins[x]])

        return arr

    def get_identities(self) -> gt.Identities:
        return self.IdentitiesData

    def get_identities_header(self) -> list[str]:
        return [ "id", "first_name", "last_name", "phone_number", "suite_number", "street_number", "street_name", "city", "province", "postal_code", "country", "sin"] # use sin as seed for employee_number? 