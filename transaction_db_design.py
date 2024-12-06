import sqlite3

# establish a connection to SQLite database
conn = sqlite3.connect("transaction_db.db")
cursor = conn.cursor()

# Fact Table: Transactions
# main fact table that records the transactional data.
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions (
    transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    customerID TEXT,
    transactionDate TEXT,
    transactionAmount REAL,
    transactionType TEXT,
    transactionStatus TEXT,
    paymentMethod TEXT,
    serviceType TEXT,
    invoiceNumber TEXT,
    FOREIGN KEY (customerID) REFERENCES CustomerFacts(customerID)
);
""")

# Dimension Table: TransactionDetails
# holds the details of each transaction (e.g., products/services).
cursor.execute("""
CREATE TABLE IF NOT EXISTS TransactionDetails (
    transactionDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
    transactionID INTEGER,
    productID TEXT,
    quantity INTEGER,
    unitPrice REAL,
    totalPrice REAL,
    FOREIGN KEY (transactionID) REFERENCES Transactions(transactionID)
);
""")

# Dimension Table: Refunds
# stores refund-related details for specific transactions.
cursor.execute("""
CREATE TABLE IF NOT EXISTS Refunds (
    refundID INTEGER PRIMARY KEY AUTOINCREMENT,
    transactionID INTEGER,
    refundDate TEXT,
    refundAmount REAL,
    refundReason TEXT,
    refundStatus TEXT,
    FOREIGN KEY (transactionID) REFERENCES Transactions(transactionID)
);
""")

# Dimension Table: Invoices
# tracks invoice details, which are linked to transactions.
cursor.execute("""
CREATE TABLE IF NOT EXISTS Invoices (
    invoiceID INTEGER PRIMARY KEY AUTOINCREMENT,
    customerID TEXT,
    invoiceDate TEXT,
    dueDate TEXT,
    totalAmountDue REAL,
    amountPaid REAL,
    amountOutstanding REAL,
    status TEXT,
    FOREIGN KEY (customerID) REFERENCES CustomerFacts(customerID)
);
""")

# Fact Table: Payments
# This is a fact table that records payments made for invoices, directly linked to financial transactions.
cursor.execute("""
CREATE TABLE IF NOT EXISTS Payments (
    paymentID INTEGER PRIMARY KEY AUTOINCREMENT,
    invoiceID INTEGER,
    paymentDate TEXT,
    paymentAmount REAL,
    paymentMethod TEXT,
    paymentStatus TEXT,
    FOREIGN KEY (invoiceID) REFERENCES Invoices(invoiceID)
);
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("Transaction database schema created successfully.")