# ====================================================================
# SCRIPT NAME:  02_Transform_to_ABT.sql
# AUTHOR:       Khoi Tran
# TASK:         (T) Transforms data from the staging table into the final ABT,
#               matching the user's actual data source.
# ====================================================================

# STEP 1: SELECT THE DATABASE
USE loan_audit_db;

# STEP 2: RESET THE FINAL ANALYTICAL TABLE
DROP TABLE IF EXISTS loan_app_analytics_base_table;

# STEP 3: CREATE THE ANALYTICAL BASE TABLE (ABT)
# This query now selects only the available and relevant columns.
CREATE TABLE loan_app_analytics_base_table AS
SELECT
    TRIM(CaseID)                    AS CaseID,
    TRIM(`concept:name`)            AS Activity,
    TRIM(`org:resource`)            AS Resource,
    TRIM(`case:LoanGoal`)           AS LoanGoal,
    TRIM(`case:ApplicationType`)    AS ApplicationType,
    TRIM(`lifecycle:transition`)    AS Lifecycle,

    # Convert numeric columns safely
    CASE
        WHEN TRIM(`CreditScore`) REGEXP '^[0-9]+$' THEN CAST(TRIM(`CreditScore`) AS SIGNED)
        ELSE NULL
    END AS CreditScore,

    CASE
        WHEN TRIM(`OfferedAmount`) REGEXP '^[0-9.]+$' THEN CAST(TRIM(`OfferedAmount`) AS DECIMAL(15,2))
        ELSE NULL
    END AS OfferedAmount
FROM
    bpi2017_events;

# STEP 4: VERIFY THE FINAL TABLE
DESCRIBE loan_app_analytics_base_table;
SELECT * FROM loan_app_analytics_base_table LIMIT 1000;