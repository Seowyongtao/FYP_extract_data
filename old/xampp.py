import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="FYP"
)

# Create a cursor object
cursor = conn.cursor()

# Create the "CompanyYearlyProfits" table
table_create_query = """
CREATE TABLE CompanyYearlyProfits (
    ID int NOT NULL AUTO_INCREMENT,
    company_ID int,
    profit_2016 decimal(10,2),
    profit_2017 decimal(10,2),
    profit_2018 decimal(10,2),
    profit_2019 decimal(10,2),
    profit_2020 decimal(10,2),
    profit_2021 decimal(10,2),
    PRIMARY KEY (ID),
    FOREIGN KEY (company_ID) REFERENCES Company(ID)
);
"""
cursor.execute(table_create_query)

# Commit changes and close the connection
conn.commit()
conn.close()