# FIRST 
INSERT INTO Contact (
	phone_number,
	email_address, 
	street_number, 
    street_name, 
    city, 
    province, 
    post_code, 
    country
) VALUES (
	"519-326-3644",
	"bigChoof@gmail.com",
    64,
    "Road St.",
    "London",
    "Ontario",
    "N6A2N3",
    "Canada"
);

SELECT * FROM Contact;

# SECOND (are these different enough????? these are the only examples in the getting started ppt)
INSERT INTO Company VALUES (
		"CompanyABC",
        14,
        "519-326-3644",
        "company.com"
);

SELECT * FROM Company;

# THIRD (this is a pointless query but it's InTeReStInG)
INSERT INTO Contact (phone_number, email_address)
	SELECT "226-534-3442", CONCAT(Company.company_name, "@yahoo.com")
	FROM Company
	WHERE Company.phone_number = "519-326-3644";
    
SELECT * FROM Contact