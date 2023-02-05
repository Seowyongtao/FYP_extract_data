from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Experiment
for company in companies:
    company_id = company[0]
    company_name = company[1]
    company_code = company[2]

    print(company_name)

    for year in range(2017, 2022):

        url = 'https://www.google.com/search?q=filetype%3Apdf+' + str(company_name) + '+annual+report+' + str(year) + '+-klse'

        # go to the url
        driver.get(url)

        # Get the first search result link
        first_result = driver.find_element(By.CSS_SELECTOR, "#rcnt a")
        first_result_link = first_result.get_attribute("href")

        # Print the first result link
        print(first_result_link)

    if company_code == '7131':
        break


# Close the chrome driver
driver.quit()