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
company_values_query = "SELECT * FROM Company;"
cursor.execute(company_values_query)

# Fetch the results
results = cursor.fetchall()

# Store the values in a list of tuples
companies = []
for result in results:
    companies.append(result)

# Set up chrome driver
options = Options()
options.add_experimental_option("detach", True)
service = Service("/Users/seowyongtao/Desktop/Chrome_Driver/chromedriver_mac64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Open Chrome
driver.switch_to.window(driver.current_window_handle)
driver.maximize_window()

# Loop the company list and assign the data into an object
for company in companies:
    company_id = company[0]
    company_code = company[2]

    driver.get('https://klse.i3investor.com/web/stock/financial-annual-unaudited/' + str(company_code) + '')
    time.sleep(2)
    search_bar = driver.find_element(By.CSS_SELECTOR, ".dataTables_filter input")

    # Need to edit current year - 5 to current year -1
    for year in range(2017, 2022):

        # Retrieve year id
        company_values_query = "SELECT * FROM TimeDim WHERE year = " + str(year) +";"
        cursor.execute(company_values_query)

        # Get year ID
        result = cursor.fetchall()
        yearID = result[0][0]

        search_bar.clear()
        search_bar.send_keys(year)

        try:
            yoy = driver.find_element(By.CSS_SELECTOR, "tbody .odd a")

            if yoy.text == '-%':
                yoy_text = '0'
            else:
                yoy_text = yoy.text.replace('%', '', 1).replace(',', '', 1)

        except:
            yoy_text = '0'

        add_data = ("INSERT INTO ProfitGrowthFact"
                    "(company_ID, Time_ID, profit_growth)"
                    "VALUES (%s, %s, %s)")

        cursor.execute(add_data, (company_id, yearID, yoy_text))
        # Commit the changes
        conn.commit()

    if company_code == '7131':
        break

# Close the cursor and connection
cursor.close()
conn.close()

# Close the chrome driver
driver.quit()