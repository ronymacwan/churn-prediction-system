import sqlite3
import pandas as pd

# connection to SQLite database
conn = sqlite3.connect('../Database/transactions.db')
cursor = conn.cursor()

df = pd.read_csv('../Dataset/transactions.csv')

# insert data into Dim_ServiceType
service_types = df['serviceType'].unique()
cursor.executemany('''
INSERT OR IGNORE INTO Dim_ServiceType (serviceType) 
VALUES (?)
''', [(service_type,) for service_type in service_types])

# insert data into Dim_ServiceSubType
service_subtypes = df['serviceSubType'].unique()
cursor.executemany('''
INSERT OR IGNORE INTO Dim_ServiceSubType (serviceSubType) 
VALUES (?)
''', [(service_subtype,) for service_subtype in service_subtypes])

# insert data into Dim_PaymentMethod
payment_methods = df['PaymentMethod'].unique()
cursor.executemany('''
INSERT OR IGNORE INTO Dim_PaymentMethod (PaymentMethod) 
VALUES (?)
''', [(payment_method,) for payment_method in payment_methods])

# insert data into Dim_Product
products = df[['ProductID', 'PriceSegment', 'Brand']].drop_duplicates()
cursor.executemany('''
INSERT OR IGNORE INTO Dim_Product (ProductID, PriceSegment, Brand) 
VALUES (?, ?, ?)
''', [(row['ProductID'], row['PriceSegment'], row['Brand']) for _, row in products.iterrows()])

# insert data into Fact_Transactions
transactions = df[['transactionID', 'customerId', 'serviceType', 'serviceSubType', 
                   'invoiceID', 'Date', 'PaymentMethod', 'Quantity', 'PerUnitPrice', 
                   'ProductID', 'PriceSegment', 'Brand', 'FinalPrice']]

cursor.executemany('''
INSERT OR IGNORE INTO Fact_Transactions (transactionID, customerId, serviceType, serviceSubType, 
                                          invoiceID, Date, PaymentMethod, Quantity, PerUnitPrice, 
                                          ProductID, PriceSegment, Brand, FinalPrice) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [(row['transactionID'], row['customerId'], row['serviceType'], row['serviceSubType'], 
       row['invoiceID'], row['Date'], row['PaymentMethod'], row['Quantity'], row['PerUnitPrice'], 
       row['ProductID'], row['PriceSegment'], row['Brand'], row['FinalPrice']) 
      for _, row in transactions.iterrows()])

conn.commit()

conn.close()

print("Data inserted into tables successfully!")