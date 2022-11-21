from typing import NewType

# singular types
Person = NewType('Name', list[int, str]) # Person includes employee number

# address: Suite_Number, Street_Number, Street_Name, City, Province, Post_Code,  Country
Address = NewType('Address', list[int, int, str, str, str, str, str])

Sin = NewType('Sin', int)
Identity = NewType('Identity', list[Person, Address, Sin])

# plural types
People = NewType('Names', list[Person])
Addresses = NewType('Addresses', list[Address])
Sins = NewType('Sins', list[Sin])
Identities = NewType('Identities', list[Identity])