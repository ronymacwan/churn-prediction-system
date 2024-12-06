import sqlite3

# establish a connection to SQLite database
conn = sqlite3.connect("customer.db")
cursor = conn.cursor()

# Fact Table: CustomerFacts
cursor.execute("""
CREATE TABLE IF NOT EXISTS CustomerFacts (
    customerID TEXT PRIMARY KEY,
    tenure INTEGER,
    MonthlyCharges REAL,
    TotalCharges REAL,
    Churn INTEGER
);
""")

# Dimension Table: CustomerDimension
cursor.execute("""
CREATE TABLE IF NOT EXISTS CustomerDimension (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen INTEGER,  -- No need to change, it stores 0 or 1
    Partner INTEGER,         -- 0 for No, 1 for Yes
    Dependents INTEGER,      -- 0 for No, 1 for Yes
    FOREIGN KEY (customerID) REFERENCES CustomerFacts(customerID)
);
""")

# Dimension Table: ServiceDimension
cursor.execute("""
CREATE TABLE IF NOT EXISTS ServiceDimension (
    customerID TEXT PRIMARY KEY,
    PhoneService INTEGER,    -- 0 for No, 1 for Yes
    MultipleLines TEXT,      -- String: 'No phone service', 'No', 'Yes'
    InternetService TEXT,    -- String: 'Fiber optic', 'DSL', 'No'
    OnlineSecurity TEXT,     -- String: 'Yes', 'No internet service', 'No'
    OnlineBackup TEXT,       -- String: 'Yes', 'No internet service', 'No'
    DeviceProtection TEXT,   -- String: 'Yes', 'No internet service', 'No'
    TechSupport TEXT,        -- String: 'Yes', 'No internet service', 'No'
    StreamingTV TEXT,        -- String: 'Yes', 'No internet service', 'No'
    StreamingMovies TEXT,    -- String: 'Yes', 'No internet service', 'No'
    FOREIGN KEY (customerID) REFERENCES CustomerFacts(customerID)
);
""")

# Dimension Table: ContractDimension
cursor.execute("""
CREATE TABLE IF NOT EXISTS ContractDimension (
    customerID TEXT PRIMARY KEY,
    Contract TEXT,           -- 'Month-to-month', 'One year', 'Two year'
    PaperlessBilling INTEGER, -- 0 for No, 1 for Yes
    PaymentMethod TEXT,      -- 'Electronic check', 'Mailed check', 'Bank transfer'
    FOREIGN KEY (customerID) REFERENCES CustomerFacts(customerID)
);
""")

# commit changes and close connection
conn.commit()
conn.close()

print("Customer database schema created successfully.")