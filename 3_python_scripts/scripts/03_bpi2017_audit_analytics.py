# ====================================================================
# SCRIPT NAME:  3_final_risk_and_process_analysis.py
# AUTHOR:       Khoi Tran
# PROJECT:      Loan Application Risk Analysis
# DESCRIPTION:
# This script connects to a database, loads the transformed loan
# application data, and performs a series of professional-grade
# analyses including frequency plotting, outcome analysis, and a
# Segregation of Duties (SoD) test. All outputs are saved to a
# dedicated directory.
# ====================================================================

# 1. SETUP & IMPORTS
import os
import warnings
from urllib.parse import quote_plus

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

# 2. GLOBAL CONFIGURATION
OUTPUT_DIR = 'output'
DB_USER = 'root'
DB_PASS = 'Khoipioo2356@'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'loan_audit_db'


# 3. ANALYSIS FUNCTIONS

def plot_frequency(df, column, title, filename, top_n=15):
    if column not in df.columns:
        print(f"Warning: Column '{column}' not found. Skipping plot: '{title}'")
        return

    counts = df[column].value_counts().nlargest(top_n)

    plt.figure(figsize=(12, 8))
    sns.barplot(x=counts.values, y=counts.index, palette='viridis')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Frequency (Number of Occurrences)', fontsize=12)
    plt.ylabel(column.replace('_', ' ').title(), fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()


def analyze_process_outcomes(df):
    required_cols = ['Activity', 'LoanGoal']
    if not all(col in df.columns for col in required_cols):
        print("Warning: Required columns for outcome analysis are missing. Skipping.")
        return

    final_activities = ['A_Pending', 'A_Denied', 'A_Cancelled', 'A_Accepted']
    df_final_state = df[df['Activity'].isin(final_activities)]

    if df_final_state.empty:
        print("Info: No final state activities found. Skipping outcome analysis.")
        return

    outcome_summary = pd.crosstab(df_final_state['LoanGoal'], df_final_state['Activity'])

    plt.figure(figsize=(14, 10))
    sns.heatmap(outcome_summary, annot=True, fmt='d', cmap='YlGnBu', linewidths=.5)
    plt.title('Process Outcomes by Loan Goal and Final Activity', fontsize=16, fontweight='bold')
    plt.ylabel('Loan Goal', fontsize=12)
    plt.xlabel('Final Activity / Outcome', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '3_process_outcomes_heatmap.png'))
    plt.close()

    outcome_summary.to_csv(os.path.join(OUTPUT_DIR, '3_process_outcomes_summary.csv'))


def analyze_segregation_of_duties(df):
    required_cols = ['Activity', 'Resource', 'CaseID']
    if not all(col in df.columns for col in required_cols):
        print("Warning: Required columns for SoD analysis are missing. Skipping.")
        return

    # Focus on the two critical activities for the SoD test
    df_sod = df[df['Activity'].isin(['O_Create Offer', 'O_Sent (mail and online)'])]

    # Filter for cases that contain both activities to ensure a valid test
    case_counts = df_sod.groupby('CaseID')['Activity'].nunique()
    valid_cases_for_test = case_counts[case_counts == 2].index
    df_sod = df_sod[df_sod['CaseID'].isin(valid_cases_for_test)]

    if df_sod.empty:
        print("SoD Test Result: No cases found containing both offer creation and sending activities.")
        return

    # Pivot to place 'Creator' and 'Sender' resources on the same row per CaseID
    sod_pivot = df_sod.pivot_table(index='CaseID', columns='Activity', values='Resource', aggfunc='first')

    # A violation occurs if the resource for both activities is the same
    sod_violations = sod_pivot.dropna()[sod_pivot['O_Create Offer'] == sod_pivot['O_Sent (mail and online)']]

    if not sod_violations.empty:
        violation_count = len(sod_violations)
        print(f"SoD Test Result: Found {violation_count} case(s) with potential SoD violations.")
        sod_violations.to_csv(os.path.join(OUTPUT_DIR, '4_sod_violations.csv'))
    else:
        print("SoD Test Result: No violations found. The control appears effective.")


# 4. MAIN WORKFLOW

def main():
    # Configure environment
    sns.set_theme(style="whitegrid")
    warnings.filterwarnings('ignore')
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Establish database connection and load data
    try:
        # URL-encode the password to handle special characters
        encoded_pass = quote_plus(DB_PASS)
        connection_string = f"mysql+mysqlconnector://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string)

        query = "SELECT * FROM loan_app_analytics_base_table"
        df = pd.read_sql(query, engine)

        if df.empty:
            print("Error: DataFrame is empty. Please check the source table 'loan_app_analytics_base_table'.")
            return
    except Exception as e:
        print(f"Error: Could not connect to the database or load data. Details: {e}")
        return

    # Execute Analysis Sequence

    # Analysis 1: Frequency and distribution analysis
    plot_frequency(df, 'Activity', 'Top 15 Most Frequent Activities', '1_activity_frequency.png')
    plot_frequency(df, 'LoanGoal', 'Top 10 Most Common Loan Goals', '2_loangoal_frequency.png', top_n=10)

    # Analysis 2: Process outcome correlation
    analyze_process_outcomes(df)

    # Analysis 3: Critical control test for Segregation of Duties
    analyze_segregation_of_duties(df)

    print(f"\nAnalysis complete. All outputs have been saved to the '{OUTPUT_DIR}' directory.")


if __name__ == '__main__':
    main()