from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import mysql.connector
import time

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="FYP"
)

# Create a cursor object
cursor = conn.cursor()

# Retrieve all values from a table
company_values_query = "SELECT * FROM TimeDim WHERE year = 2017;"
cursor.execute(company_values_query)

# Fetch the results
results = cursor.fetchall()

print(results[0][1])

# Close the cursor and connection
cursor.close()
conn.close()