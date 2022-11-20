import names  # random name generator pip package
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

        arr = gt.Identities
        for x in range(self.n):
            arr.append([self.people[x]])

        return arr

    # generates names and sequential serial #s. They don't have to stay in sequential order in the db though
    def generate_people(self) -> gt.People:
        people = gt.People
        for x in range(self.n):
            [fname, lname] = names.get_full_name().split(" ")
            people.append({x + 1, fname, lname})

        return people