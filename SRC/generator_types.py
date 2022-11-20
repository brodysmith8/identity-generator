from typing import NewType

# not used in the generator; only used to compose plural types
Person = NewType('Name', list[int, str]) # Person includes employee number
Address = NewType('Address', list[int, int, str, str, str, str, str, int])
Sin = NewType('Sin', int)
Identity = NewType('Identity', list[Person, Address, Sin])

# plural types
People = NewType('Names', list[Person])
Addresses = NewType('Addresses', list[Address])
Sins = NewType('Sins', list[Sin])
Identities = NewType('Identities', list[Identity])