import names  # random name generator pip package
import random
import csv
import generator_types as gt


class Generator:
    def __init__(self, n):
        self._n = n
        self.IdentitiesData = self.generate_identities()

    def __str___(self) -> str:  # toString
        return str(id)

    def get_identities(self) -> gt.Identities:
        return self.IdentitiesData

    def generate_identities(self) -> gt.Identities:
        self.people = self.generate_people()
        self.addresses = self.generate_addresses()
        self.sins = self.generate_sins()

        arr = gt.Identities
        for x in range(self.n):
            arr.append([
                self.people[x],
                self.addresses[x],
                self.sins[x]])

        return arr

    # generates names and sequential serial #s. They don't have to stay in sequential order in the db though
    def generate_people(self) -> gt.People:
        people = gt.People
        for x in range(self.n):
            [fname, lname] = names.get_full_name().split(" ")
            people.append({x + 1, fname, lname})

        return people

    # definitely can slim this method down
    # list[int, int, str, str, str, str, str, int])
    def generate_addresses(self) -> gt.Addresses:
        addresses = []

        f = open('data/in/street-names-and-frequency-modified.csv')
        fr = csv.reader(f, dialect="unix")

        f_ss = open('data/in/street-suffixes.csv')
        fr_ss = csv.reader(f_ss, dialect="unix")

        # Stage one: street number, street name
        for x in range(self.n):
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

        testSumNL = 0
        testSumNS = 0

        for x in range(self.n):
            # about 0.7% error, n = 5000
            rng = random.random()
            for line in fr_p:
                if float(line[2]) > rng:
                    current_province = line[0]
                    f_p.seek(0)
                    break

            # about 3.6% error, n = 5000
            # current_province = random.choices(population=["Nova Scotia", "Newfoundland and Labrador"], weights=[0.5228, 0.48])[0]

            rng = random.random() * 100  # once again will never reach 100%

            if current_province == 'Nova Scotia':
                testSumNS += 1
                for line in fr_ns:
                    city_name, _, _, cumulative_population = line
                    if float(cumulative_population) > rng:
                        addresses[x][3] = city_name
                        addresses[x][4] = current_province
                        f_ns.seek(0)
                        break
            else:
                testSumNL += 1
                for line in fr_nl:
                    city_name, _, _, cumulative_population = line
                    if float(cumulative_population) > rng:
                        addresses[x][3] = city_name
                        addresses[x][4] = current_province
                        f_nl.seek(0)
                        break

        f_p.close()

        # Stage three: post code LDUs (second part 0A0)
        def safe_increment_pcode_number(num):
            num+=1
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