DROP TABLE IF EXISTS employee;   
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS schemeapplication;
DROP TABLE IF EXISTS welfarescheme;
DROP TABLE IF EXISTS cultivationrecord;
DROP TABLE IF EXISTS agriculturalland;
DROP TABLE IF EXISTS servicerequests;
DROP TABLE IF EXISTS households;
DROP TABLE IF EXISTS censusdata;
DROP TABLE IF EXISTS vaccinations;
DROP TABLE IF EXISTS citizens;

CREATE TABLE citizens (
    citizenid  SERIAL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    dateofbirth DATE NOT NULL,
    gender VARCHAR(10) CHECK (Gender IN ('Male', 'Female', 'Other')),
    householdid INT,
    contactnumber VARCHAR(15),
    job VARCHAR(50) ,   
    educationalqualification VARCHAR(50) CHECK (educationalqualification IN ('10th', '12th', 'Graduate', 'Post Graduate', 'Diploma', 'PhD', 'Other')),
    fatherid INT NULL,
    motherid INT NULL,
    FOREIGN KEY (fatherid) REFERENCES citizens(citizenid) ON DELETE SET NULL,
    FOREIGN KEY (motherid) REFERENCES citizens(citizenid) ON DELETE SET NULL
);

CREATE TABLE employee (
    employeeid SERIAL PRIMARY KEY,
    citizenid INT UNIQUE,
    role VARCHAR(50) CHECK (Role IN ('Sarpanch', 'Secretary', 'Accountant', 'Clerk', 'Surveyor', 'Health Officer')),
    FOREIGN KEY (citizenid) REFERENCES citizens(citizenid) ON DELETE CASCADE
);

CREATE TABLE users(
    userid SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(50) CHECK (Role IN ('Admin', 'Employee', 'Citizen', 'Monitor')),
    citizenid INT,
    FOREIGN KEY (citizenid) REFERENCES citizens(citizenid) ON DELETE SET NULL
);

CREATE TABLE assets (
    assetid SERIAL PRIMARY KEY,
    type VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    installationdate DATE NOT NULL,
    condition VARCHAR(50) CHECK (condition IN ('Good', 'Needs Repair', 'Damaged', 'Replaced')),
    lastmaintenancedate DATE
);

CREATE TABLE households (
    householdid SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    income DECIMAL(12,2) NOT NULL CHECK (Income >= 0),
    numberOfmembers INT NOT NULL CHECK (NumberOfMembers > 0),
    propertyvalue DECIMAL(12,2) CHECK (PropertyValue >= 0)
);

CREATE TABLE welfarescheme (
    schemeid SERIAL PRIMARY KEY,
    SchemeName VARCHAR(100) UNIQUE NOT NULL,
    Description TEXT NOT NULL,
    EligibilityCriteria VARCHAR(200) NOT NULL,
    Benefits TEXT NOT NULL,
    LaunchDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Department VARCHAR(100) NOT NULL,
    ValidTill TIMESTAMP NOT NULL
);

CREATE TABLE schemeapplication (
    applicationid SERIAL PRIMARY KEY,
    Citizenid INT NOT NULL,
    schemeid INT NOT NULL,
    applicationdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Status BOOLEAN NOT NULL DEFAULT FALSE,
    Remarks TEXT,
    FOREIGN KEY (Citizenid) REFERENCES citizens(citizenid) ON DELETE CASCADE,
    FOREIGN KEY (schemeid) REFERENCES welfarescheme(schemeid) ON DELETE CASCADE
);

CREATE TABLE agriculturalland (
    landid SERIAL PRIMARY KEY,
    citizenid INT NOT NULL,
    area FLOAT NOT NULL,
    address VARCHAR(255) NOT NULL,
    FOREIGN KEY (citizenid) REFERENCES citizens(citizenid) ON DELETE CASCADE
);

CREATE TABLE cultivationrecord (
    cultivationid SERIAL PRIMARY KEY,
    landid INT NOT NULL,
    year INT NOT NULL,
    citizenid INT NOT NULL,
    season VARCHAR(50) NOT NULL,
    croptype VARCHAR(100) NOT NULL,
    cultivatedarea FLOAT NOT NULL,
    productionquantity FLOAT,
    FOREIGN KEY (citizenid) REFERENCES citizens(citizenid) ON DELETE CASCADE,
    FOREIGN KEY (landid) REFERENCES agriculturalland(landid) ON DELETE CASCADE
);

CREATE TABLE servicerequests (
    requestid SERIAL PRIMARY KEY,
    citizenid INTEGER NOT NULL,
    requesttype VARCHAR(50) NOT NULL CHECK (requesttype IN ('Birth Certificate', 'Death Certificate', 'Income Certificate', 'Marriage Certificate', 'Caste Certificate')),
    requestdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    CONSTRAINT fk_citizen FOREIGN KEY (citizenid) REFERENCES citizens(citizenid) ON DELETE CASCADE
);

CREATE TABLE censusdata (
    censuseventid SERIAL PRIMARY KEY,
    citizenid INT NOT NULL,
    eventtype VARCHAR(20) NOT NULL CHECK (eventtype IN ('Birth', 'Death', 'Marriage', 'Divorce')),
    eventdate DATE NOT NULL,
    eventnotes TEXT,
    FOREIGN KEY (citizenid) REFERENCES citizens(citizenid) ON DELETE CASCADE
);

CREATE TABLE vaccinations (
    vaccinationid SERIAL PRIMARY KEY,
    citizenid INT NOT NULL,
    vaccinetype VARCHAR(255) NOT NULL,
    dateadministered DATE NOT NULL,
    FOREIGN KEY (citizenid) REFERENCES citizens(citizenid) ON DELETE CASCADE
);
