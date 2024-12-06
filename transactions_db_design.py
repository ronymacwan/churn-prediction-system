import sqlite3

# connection to SQLite database
conn = sqlite3.connect('../Database/transactions.db')
cursor = conn.cursor()

# Dim_ServiceType table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Dim_ServiceType (
    serviceType TEXT PRIMARY KEY
)
''')

# Dim_ServiceSubType table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Dim_ServiceSubType (
    serviceSubType TEXT PRIMARY KEY
)
''')

# Dim_PaymentMethod table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Dim_PaymentMethod (
    PaymentMethod TEXT PRIMARY KEY
)
''')

# Dim_Product table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Dim_Product (
    ProductID TEXT PRIMARY KEY,
    PriceSegment TEXT,
    Brand TEXT
)
''')

# Fact_Transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Fact_Transactions (
    transactionID INTEGER PRIMARY KEY,
    customerId TEXT,
    serviceType TEXT,
    serviceSubType TEXT,
    invoiceID TEXT,
    Date TEXT,
    PaymentMethod TEXT,
    Quantity INTEGER,
    PerUnitPrice REAL,
    ProductID TEXT,
    PriceSegment TEXT,
    Brand TEXT,
    FinalPrice REAL,
    FOREIGN KEY (serviceType) REFERENCES Dim_ServiceType(serviceType),
    FOREIGN KEY (serviceSubType) REFERENCES Dim_ServiceSubType(serviceSubType),
    FOREIGN KEY (PaymentMethod) REFERENCES Dim_PaymentMethod(PaymentMethod),
    FOREIGN KEY (ProductID) REFERENCES Dim_Product(ProductID),
    FOREIGN KEY (PriceSegment) REFERENCES Dim_Product(PriceSegment),
    FOREIGN KEY (Brand) REFERENCES Dim_Product(Brand)
)
''')

conn.commit()

conn.close()

print("Database and tables created successfully!")
