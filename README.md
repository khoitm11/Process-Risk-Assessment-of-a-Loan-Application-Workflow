# End-to-End Risk & Process Analysis of a Loan Application Workflow

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/) [![Pandas](https://img.shields.io/badge/Pandas-2.0+-blue?style=for-the-badge&logo=pandas)](https://pandas.pydata.org/) [![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql)](https://www.mysql.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 1. Executive Summary

This project simulates a comprehensive technology risk consulting engagement. It deploys a professional, two-stage data pipeline to process, analyze, and derive insights from a complex, real-world event log dataset (**BPI Challenge 2017**, >1.2 million records).

The primary objective is to perform an end-to-end analysis of a loan application workflow to **identify business risks**, **assess internal control effectiveness**, and **propose data-driven process improvements**. This directly addresses the dual mandate of risk advisory: to strengthen internal controls while simultaneously enhancing business performance.

---

## 2. Key Findings & Visual Evidence

This analysis transforms raw data into actionable intelligence, providing quantifiable evidence for strategic decision-making.

### Finding #1: Potential Business Risk in Product Portfolio

A heatmap analysis revealed an **abnormally high rate of cancellation and denial for 'Car' loans** compared to other products, specifically *after* the initial offers were made. This indicates a potential business risk, suggesting underlying issues with product competitiveness, customer experience, or the risk assessment model for this specific segment.

![image](https://github.com/user-attachments/assets/e421dddd-554c-4044-98ec-7cc25ba663d0)


### Finding #2: Internal Control Gap — Segregation of Duties (SoD) Violation

An automated test was designed and executed to validate a critical Segregation of Duties (SoD) control: **"the user who creates an offer cannot be the same user who sends it."** The script successfully identified and quantified instances of violation, providing concrete evidence of a control weakness that requires remediation.

**Evidence of Detected Violations:**
```csv
CaseID,O_Create Offer,O_Sent (mail and online)
Application_1000086665,User_5,User_5
Application_1000158214,User_32,User_32
Application_1000311556,User_71,User_71
...
````

-----

## 3\. Architecture & Methodology

The project is architected in a two-stage pipeline to ensure data integrity, processing efficiency, and analytical clarity.

### Stage 1: SQL-based ETL (Data Engineering)

  * **Objective:** To build a clean, structured, and reliable **Single Source of Truth (SSOT)**.
  * **Process:** A series of SQL scripts (`.sql` files) were executed via MySQL Workbench. This automated pipeline first loads raw data into a staging table, then performs robust cleaning, data type conversion, and transformation steps to produce a final **Analytical Base Table (ABT)**, ready for analysis.

### Stage 2: Python-based Analysis (Data Analysis)

  * **Objective:** To convert the clean data into actionable business insights and risk findings.
  * **Process:** A structured Python script (`.py` file) was developed in PyCharm. The script connects to the MySQL database, ingests the ABT, performs in-depth statistical analysis, and automatically exports the resulting **"audit evidence"** (charts, CSV files) to a dedicated output directory.

-----

## 4\. Technology Stack

| Domain | Tools & Technologies |
| :--- | :--- |
| **Database & ETL** | MySQL 8.0, SQL, MySQL Workbench |
| **Analysis & Visualization**| Python 3.9+, Pandas, Seaborn, Matplotlib, SQLAlchemy |
| **Development Environment** | PyCharm, Virtual Environment (venv) |
| **Process Modeling** | BPMN 2.0 |
| **Version Control** | Git, GitHub |

-----

## 5\. How to Reproduce

This entire project is 100% reproducible. Please follow the steps below.

### Prerequisites

  * MySQL Server (installed and running)
  * Python 3.9+
  * Git

### Step-by-Step Guide

**1. Clone the Repository**

```bash
git clone [https://github.com/](https://github.com/)[Your-GitHub-Username]/[Your-Repo-Name].git
cd [Your-Repo-Name]
```

**2. Set Up the Database**

1.  In your MySQL client, create a new database: `CREATE DATABASE loan_audit_db;`
2.  Download the **BPI Challenge 2017** dataset as a `.csv` file (e.g., from Kaggle).
3.  Place the downloaded `.csv` file into the secure file-priv directory for your MySQL installation (on Windows, this is typically `C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/`).
4.  Open and execute the `2_sql_etl_scripts/01_Load_Raw_Data.sql` script.
      * **Note:** You may need to update the `LOAD DATA INFILE` path within the script to match your file's location.
5.  Execute the `2_sql_etl_scripts/02_Transform_to_ABT.sql` script to build the final analysis table.

**3. Set Up the Python Environment**

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Install the required libraries
pip install -r requirements.txt
```

**4. Run the Analysis Script**

  * **Important:** Open the `3_python_analysis/final_risk_and_process_analysis.py` file and update your database credentials (`DB_USER`, `DB_PASS`, `DB_HOST`, `DB_NAME`) in the **GLOBAL CONFIGURATION** section.
  * Execute the script from the project's root directory:

<!-- end list -->

```bash
python 3_python_analysis/final_risk_and_process_analysis.py
```

**5. Review the Outputs**

  * All generated charts and data files will be automatically saved in the `4_presentation_and_reports/output/` directory.

<!-- end list -->
