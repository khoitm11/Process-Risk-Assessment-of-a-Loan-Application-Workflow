#====================================================================
#SCRIPT NAME:  01_Load_Raw_Data.sql
#AUTHOR:       Khoi Tran
#TASK:         Fixes the classic semicolon termination error.
#              This is the definitive, production-ready version.
#====================================================================

#STEP 1: SELECT THE DATABASE
USE loan_audit_db;

#STEP 2: RESET THE STAGING TABLE
DROP TABLE IF EXISTS bpi2017_events;

#STEP 3: CREATE THE STAGING TABLE
CREATE TABLE bpi2017_events (
    `Action`                 TEXT,
    `org:resource`           TEXT,
    `concept:name`           TEXT,
    `EventOrigin`            TEXT,
    `EventID`                TEXT,
    `lifecycle:transition`   TEXT,
    `case:LoanGoal`          TEXT,
    `case:ApplicationType`   TEXT,
    `CaseID`                 TEXT,
    `RequestedAmount`        TEXT,
    `FirstWithdrawalAmount`  TEXT,
    `NumberOfTerms`          TEXT,
    `Accepted`               TEXT,
    `MonthlyCost`            TEXT,
    `Selected`               TEXT,
    `CreditScore`            TEXT,
    `OfferedAmount`          TEXT,
    `OfferID`                TEXT
);

#STEP 4: LOAD THE DATA FROM CSV
#These SET commands should be executed BEFORE the main command.
#They are separate SQL statements, each needing a semicolon.
SET foreign_key_checks = 0;
SET unique_checks = 0;

#Main data loading command.
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/BPI_Challenge_2017.csv'
INTO TABLE bpi2017_events
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

#Re-enable the checks after the load is complete.
SET unique_checks = 1;
SET foreign_key_checks = 1;

#STEP 5: VERIFY THE LOAD
#Check the first 1000 rows from the CORRECT table.
SELECT * FROM bpi2017_events LIMIT 1000;