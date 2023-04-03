from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import mysql.connector
import requests
from PyPDF2 import PdfReader
import re
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

# Experiment
for company in companies:
    company_id = company[0]
    company_name = company[1]
    company_code = company[2]

    print(company_name)

    for year in range(2017, 2022):

        url = 'https://www.malaysiastock.biz/Corporate-Infomation.aspx?securityCode=' + str(company_code)

        # go to the url
        driver.get(url)
        time.sleep(3)

        # Get the link of the annual report
        ar = driver.find_element(By.CSS_SELECTOR, "#divAR_" + str(company_code) + "_" + str(year) + " a:nth-of-type(2)")
        ar_link = ar.get_attribute("href")

        # apply sentiment
        # Extract pdf text part
        url = ar_link

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open('../tmp.pdf', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)

        pdf = PdfReader('../tmp.pdf')

        page_number = 2
        page_object = pdf.pages[page_number - 1]

        page_text = page_object.extract_text()

        # Finsentiment part
        driver.get('https://www.finsentiment.com/default')
        time.sleep(1)

        text_box = driver.find_element(By.XPATH, '//*[@id="MainContentPlaceHolder_TextSearchBox"]')
        text_box.send_keys(page_text)

        button = driver.find_element(By.ID, 'MainContentPlaceHolder_Button2')
        button.click()

        sentiment_score = driver.find_element(By.XPATH, '//*[@id="MainContentPlaceHolder_LabelSentiment"]')
        time.sleep(1)
        print(ar_link)
        print(sentiment_score.text)

    if company_code == '7214':
        break


# Close the chrome driver
driver.quit()