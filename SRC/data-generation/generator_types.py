from typing import NewType

# singular types
Person = NewType('Name', "list[int, str]") # Person includes employee number

# address: Street_Number, Street_Name, City, Province, Post_Code,  Country
Address = NewType('Address', "list[int, str, str, str, str, str]")

Sin = NewType('Sin', str)

PhoneNumber = NewType('PhoneNumber', str)
EmailAddress = NewType('EmailAddress', str)
Role = NewType('Role', "list[str, int]")
Bank = NewType('Bank', "list[str, str, str]")

# "id", "first_name", "last_name", "role_name", "street_number", "street_name", "city", "province", "postal_code", "country", "phone_number", "email_address", "sin", "company_name"] # use sin as seed for employee_number? 
Identity = NewType('Identity', "list[Person, PhoneNumber, EmailAddress, Address, Sin, Role]")


# plural types
People = NewType('Names', "list[Person]")
Addresses = NewType('Addresses', "list[Address]")
Sins = NewType('Sins', "list[Sin]")
PhoneNumbers = NewType('PhoneNumber', "list[str]")
EmailAddresses = NewType('EmailAddress', "list[str]")
Roles = NewType('Role', "list[Sin]")
Banks = NewType('Banks', "list[Banks]")
Identities = NewType('Identities', "list[Identity]")