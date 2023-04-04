from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

options = Options()
options.add_experimental_option("detach", True)

service = Service("/Users/seowyongtao/Desktop/Chrome_Driver/chromedriver_mac64/chromedriver")

driver = webdriver.Chrome(service=service, options=options)
driver.switch_to.window(driver.current_window_handle)
driver.maximize_window()
driver.get('http://www.bursamalaysia.com/market/listed-companies/list-of-companies/main-market/')

link_paths = driver.find_elements(By.CSS_SELECTOR, "table tbody .position-relative a")

for link_path in link_paths:
    href_text = link_path.get_attribute('href')
    split_text_array = href_text.split('=')

    if len(split_text_array) > 1:
        # print(split_text_array[-1])
        # print(link_path.get_attribute('innerText'))

        name = link_path.get_attribute('innerText')
        code = split_text_array[-1]

        # Insert the values into the table
        insert_query = "INSERT INTO CompanyDim(name, stock_code) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, code))

        # Commit the changes
        conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

driver.quit()