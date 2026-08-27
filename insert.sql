-- Inserting parents
INSERT INTO CITIZENS (FullName, DateOfBirth, Gender, ContactNumber, EducationalQualification, Job, HouseholdID) VALUES
('Ramesh Sharma', '1965-03-10', 'Male', '9876500001', 'Graduate', 'Teacher', 201),
('Sunita Sharma', '1970-07-15', 'Female', '9876500002', 'Post Graduate', 'Doctor', 201),
('Mahesh Verma', '1968-12-20', 'Male', '9876500003', '12th', 'Farmer', 202),
('Anita Verma', '1975-06-05', 'Female', '9876500004', 'Graduate', 'Housewife', 202);

-- Inserting children with parent references
INSERT INTO CITIZENS ( FullName, DateOfBirth, Gender, ContactNumber, EducationalQualification, Job, HouseholdID, FatherID, MotherID) VALUES
('Amit Sharma', '1990-05-12', 'Male', '9876543210', 'Post Graduate', 'Software Engineer', 201, 1, 2),
('Priya Verma', '1995-08-25', 'Female', '9867543211', 'Graduate', 'Bank Manager', 202, 3, 4),
('Rajesh Kumar', '1988-02-17', 'Male', '9856543222', '12th', 'Electrician', 203, NULL, NULL),
('Sanya Mehta', '2000-11-05', 'Female', '9846543233', 'PhD', 'Professor', 204, NULL, NULL);


INSERT INTO EMPLOYEE ( CitizenID, Role) VALUES
(5, 'Sarpanch'),         
(6, 'Secretary'),        
(7, 'Surveyor'),        
(8, 'Health Officer'); 

INSERT INTO USERS ( Username, Password, Role, CitizenID) VALUES
('sunita_sharma', 'motherpass1', 'Citizen', 2),
('ramesh_sharma', 'fatherpass1', 'Citizen', 1),
('mahesh_verma', 'fatherpass2', 'Citizen', 3),
('anita_verma', 'motherpass2', 'Citizen', 4),
('amit_admin', 'password123', 'Employee', 5),
('priya_emp', 'emp456', 'Employee', 6),
('rajesh_mon', 'mon789', 'Employee', 7),
('sanya_citizen', 'citizen101', 'Employee', 8),
('Preetham','Preetham123@','Monitor',NULL);

INSERT INTO ASSETS (Type, Location, InstallationDate, Condition, LastMaintenanceDate) VALUES
('Water Pump', 'Village A', '2018-06-15', 'Good', '2023-07-10'),
('Solar Street Light', 'Village B', '2020-02-20', 'Needs Repair', '2023-10-05'),
('Public Library', 'Village C', '2015-09-12', 'Good', '2022-12-01'),
('Community Hall', 'Village D', '2017-11-25', 'Damaged', NULL);

INSERT INTO HOUSEHOLDS ( Address, Income, NumberOfMembers, PropertyValue) VALUES
('Village A, House 1', 50000, 4, 300000),
('Village B, House 2', 70000, 5, 400000),
('Village C, House 3', 30000, 3, 250000),
('Village D, House 4', 60000, 6, 350000);

-- Insert Sample Data into welfarescheme
INSERT INTO welfarescheme (SchemeName, Description, EligibilityCriteria, Benefits, LaunchDate, Department, ValidTill)
VALUES
('Education Support', 'Financial aid for students', 'Low-income students', 'Up to $5000 per year', '2022-01-15', 'Education Dept', '2030-12-31'),
('Health Insurance', 'Free healthcare for citizens', 'All citizens below poverty line', 'Full medical coverage', '2021-06-10', 'Health Dept', '2029-06-10'),
('Employment Grant', 'Support for unemployed youth', 'Unemployed under 30', '$1000 monthly stipend', '2023-03-20', 'Labour Dept', '2031-03-20'),
('Housing Assistance', 'Affordable housing loans', 'First-time home buyers', 'Up to $50,000 loan subsidy', '2020-08-05', 'Housing Dept', '2028-08-05'),
('Old Age Pension', 'Monthly pension for seniors', 'Age 60 and above', '$200 per month', '2019-11-25', 'Social Welfare Dept', '2040-11-25');

INSERT INTO schemeapplication (Citizenid, schemeid, applicationdate, Status, Remarks)
VALUES
(1, 1, '2024-01-10', TRUE, 'Approved'),
(2, 3, '2024-02-15', FALSE, 'Under review'),
(3, 2, '2024-03-05', TRUE, 'Approved'),
(4, 5, '2024-04-20', FALSE, 'Incomplete documents'),
(5, 4, '2024-05-10', TRUE, 'Pending final approval');


INSERT INTO agriculturalland (citizenid, area, address) VALUES
(1, 10.5, 'Farm A, Village X'),
(1, 5.2, 'Farm B, Village Y'),
(2, 8.0, 'Farm C, Village Z');

INSERT INTO cultivationrecord (landid, year, citizenid, season, croptype, cultivatedarea, productionquantity) VALUES
(1, 2024, 1, 'Kharif', 'Wheat', 8.0, 5000),
(2, 2023, 1, 'Rabi', 'Rice', 4.5, 3000),
(3, 2024, 2, 'Summer', 'Maize', 7.0, 4000);

INSERT INTO censusdata (citizenid, eventtype, eventdate, eventnotes) VALUES
(5, 'Birth', '1990-05-12', 'Birth record of Amit Sharma.'),
(6, 'Marriage', '2020-05-15', 'Priya Verma married Rohit Das.'),
(7, 'Divorce', '2023-11-30', 'Rajesh Kumar and Sanya Mehta got divorced.'),
(3, 'Death', '2023-11-12', 'Mahesh Verma passed away.');

INSERT INTO vaccinations (citizenid, vaccinetype, dateadministered) VALUES
(1, 'Pfizer', '2023-01-15'),
(2, 'Moderna', '2023-02-10'),
(3, 'Johnson & Johnson', '2023-03-05'),
(4, 'AstraZeneca', '2023-04-20'),
(5, 'Pfizer', '2023-05-25'),
(6, 'Moderna', '2023-06-30');