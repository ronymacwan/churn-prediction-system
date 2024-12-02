import sqlite3
import pandas as pd

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# connection to SQLite database
conn = sqlite3.connect("telecom_churn.db")
cursor = conn.cursor()

# function to convert 'Yes'/'No' to 1/0
def convert_yes_no(value):
    if value == 'Yes':
        return 1
    elif value == 'No':
        return 0
    return value  # edge case for unexpected value, just return it

# iterate over each row and insert it into the database
for _, row in df.iterrows():
    try:
        # convert Yes/No values to 1/0 for the appropriate columns
        row['SeniorCitizen'] = convert_yes_no(row['SeniorCitizen'])
        row['Partner'] = convert_yes_no(row['Partner'])
        row['Dependents'] = convert_yes_no(row['Dependents'])
        row['Churn'] = convert_yes_no(row['Churn'])
        row['PhoneService'] = convert_yes_no(row['PhoneService'])
        row['PaperlessBilling'] = convert_yes_no(row['PaperlessBilling'])

        # insert into CustomerFacts table
        cursor.execute("""
        INSERT INTO CustomerFacts (customerID, tenure, MonthlyCharges, TotalCharges, Churn)
        VALUES (?, ?, ?, ?, ?);
        """, (row['customerID'], row['tenure'], row['MonthlyCharges'], row['TotalCharges'], row['Churn']))

        # insert into CustomerDimension table
        cursor.execute("""
        INSERT INTO CustomerDimension (customerID, gender, SeniorCitizen, Partner, Dependents)
        VALUES (?, ?, ?, ?, ?);
        """, (row['customerID'], row['gender'], row['SeniorCitizen'], row['Partner'], row['Dependents']))

        # insert into ServiceDimension table
        cursor.execute("""
        INSERT INTO ServiceDimension (customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (row['customerID'], row['PhoneService'], row['MultipleLines'], row['InternetService'],
              row['OnlineSecurity'], row['OnlineBackup'], row['DeviceProtection'], row['TechSupport'],
              row['StreamingTV'], row['StreamingMovies']))

        # insert into ContractDimension table
        cursor.execute("""
        INSERT INTO ContractDimension (customerID, Contract, PaperlessBilling, PaymentMethod)
        VALUES (?, ?, ?, ?);
        """, (row['customerID'], row['Contract'], row['PaperlessBilling'], row['PaymentMethod']))

        # commit after each row to avoid large memory consumption
        conn.commit()

    except Exception as e:
        print(f"Error inserting row {row['customerID']}: {e}")

conn.close()

print("Data insertion completed.")