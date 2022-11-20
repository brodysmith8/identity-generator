CREATE TABLE IF NOT EXISTS Contact(
	phone_number VARCHAR(255) NOT NULL,
    email_address VARCHAR(255),
    suite_number INT, 
    street_number INT,
    street_name VARCHAR(255), 
    city VARCHAR(255), 
    province VARCHAR(255),
    post_code VARCHAR(255),
    country VARCHAR(255),
    PRIMARY KEY (phone_number)
);

DESCRIBE Contact;

# Had to rename "Position" table in schema to "Role" because Position is a reserved word
CREATE TABLE IF NOT EXISTS Role(
	role_id INT NOT NULL AUTO_INCREMENT, # Question for TA: do we need to add "UNIQUE" here or is declaring it a PK enough
    role_name VARCHAR(255),
    PRIMARY KEY (role_id)
);

DESCRIBE Role;

CREATE TABLE IF NOT EXISTS Company(
	company_name VARCHAR(255) NOT NULL,
    company_pay_frequency_days INT, # Wrote days in the attribute name for more clarity
    phone_number VARCHAR(255) NOT NULL, # Not null because original is not null
    company_domain_name VARCHAR(255), # this just holds their domain name for emails
	PRIMARY KEY (company_name),
    FOREIGN KEY (phone_number)
		REFERENCES Contact(phone_number)
        ON DELETE CASCADE # need to see if deleting the FK deletes the entire row in the parent. If it does, keep cascade, and change ON DELETE of phone_number in employee to cascade too.
        ON UPDATE CASCADE # Update phone_number in both places
);

DESCRIBE Company;

CREATE TABLE IF NOT EXISTS EmployeeRole( # we have to use PascalCase for table names, but they are stored as lowercase. Can we instead use snake_case?
	employee_id INT NOT NULL AUTO_INCREMENT,
    role_id INT NOT NULL, # should you add NOT NULL to attributes declared not null?
    PRIMARY KEY (employee_id),
    FOREIGN KEY (role_id) 
		REFERENCES Role(role_id)
		ON DELETE NO ACTION # employee and their role can be deleted without changing Roles
        ON UPDATE NO ACTION # similarly, employee can change roles without it being changed in Roles
);

DESCRIBE EmployeeRole;

CREATE TABLE IF NOT EXISTS Branch(
	branch_id INT NOT NULL AUTO_INCREMENT,
    phone_number VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (branch_id),
    FOREIGN KEY (phone_number)
		REFERENCES Contact(phone_number)
        # if phone number gets updated from Contact, update it in the parent too
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
	FOREIGN KEY (company_name)
		REFERENCES Company(company_name)
        ON DELETE NO ACTION # a branch can be disbanded without the company being disbanded
        ON UPDATE NO ACTION # a branch can change the company it belongs to (technically; in practice this wouldn't happen probably)
);

DESCRIBE Branch;

CREATE TABLE IF NOT EXISTS Employee(	
	employee_id	INT NOT NULL AUTO_INCREMENT,
	phone_number VARCHAR (255) NOT NULL,
	branch_id INT NOT NULL,
	employee_first_name VARCHAR (255),
    employee_last_name VARCHAR (255),
	employee_start_date VARCHAR (255), 
    employee_sin VARCHAR (255), # data security needs to happen somehow 
    employee_bank_account_number VARCHAR (255),
    employee_bank_transit_number VARCHAR (255),
    employee_bank_institution_number VARCHAR (255), 
    PRIMARY KEY (employee_id),
    FOREIGN KEY (phone_number) 
		REFERENCES Contact(phone_number)
        # I don't think we should use "SET NULL" here because phone_number is the PK 
        # of Contact, so if there is more than one employee with a null phone_number, 
        # they are no longer uniquely identifiable. Also the phone_number field in 
        # Contact is set as NOT NULL
        ON DELETE NO ACTION
        ON UPDATE CASCADE, # CASCADE will update the phone number in Contact if it's changed in Employee (e.g. when an employee gets a new phone number)
    FOREIGN KEY (branch_id) 
		REFERENCES Branch (branch_id)
		# Do not reflect any Employee branch changes in the Branch table
        ON DELETE NO ACTION 
        ON UPDATE NO ACTION,
    FOREIGN KEY (employee_id) 
		REFERENCES EmployeeRole(employee_id)
        # If employee_id gets changed or deleted, reflect the change or deletion in
        # EmployeeRole
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DESCRIBE Employee;

CREATE TABLE IF NOT EXISTS Payroll(
	payroll_id INT NOT NULL AUTO_INCREMENT, # we'd have to have an obscene amount of employees to get past the 2.147 bn cap on INT. I don't think it's feasible
    payment_date DATE,
    employee_id INT NOT NULL,
    payment_salary DECIMAL(8,2), # max value is 999,999.99
    payment_bonus DECIMAL(8,2),
    payment_status CHAR(1), # can be "t" or "f" depending on whether payment has been disbursed or not. Boolean was not in the slide on datatypes so don't want to risk getting marks deducted for it
	PRIMARY KEY (payroll_id),
    FOREIGN KEY (employee_id) 
		REFERENCES Employee(employee_id)
        # Don't want changes in parent from changes in child
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

DESCRIBE Payroll;

CREATE TABLE IF NOT EXISTS TaxForm(
	tax_form_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    tax_year DATE, # will just be January 1st of the year (e.g. '2022-01-01'). There is a YEAR datatype but it is not in the slides so I don't want to risk getting marks deducted for it
    tax_form_url VARCHAR(255),
	PRIMARY KEY (tax_form_id),
    FOREIGN KEY (employee_id) 
		REFERENCES Employee(employee_id)
        ON DELETE NO ACTION # can delete a tax form without deleting the attached employee
        ON UPDATE NO ACTION # don't want child changes in parent
);

DESCRIBE TaxForm;